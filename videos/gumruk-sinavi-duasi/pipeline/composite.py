import cv2, numpy as np, subprocess, sys, json
# usage: composite.py plate.mp4 out.mp4 duration
PLATE, OUT, DUR = sys.argv[1], sys.argv[2], float(sys.argv[3])
OW, OH = 1080, 1920
SCHED = [(0.0,"s1"),(5.60,"s2"),(10.43,"s3"),(14.74,"s4"),(20.50,"s5"),(25.56,"s6a"),(30.72,"s6b"),(33.45,"s7")]
slides = {n: cv2.imread(f"slides/{n}.png") for _,n in SCHED}
SW, SH = 1650, 1000
REF_Y = 0.299*141 + 0.587*251 + 0.114*203

cap = cv2.VideoCapture(PLATE); fps = cap.get(cv2.CAP_PROP_FPS) or 24
frames = []
while True:
    ok, f = cap.read()
    if not ok: break
    if f.shape[1] != OW or f.shape[0] != OH: f = cv2.resize(f, (OW, OH), interpolation=cv2.INTER_AREA)
    frames.append(f)
N = len(frames); print("plate frames", N, "fps", fps, file=sys.stderr)

def order(pts):
    pts = np.array(pts, np.float32); s = pts.sum(1); d = np.diff(pts, axis=1).ravel()
    return np.array([pts[np.argmin(s)], pts[np.argmin(d)], pts[np.argmax(s)], pts[np.argmax(d)]], np.float32)  # tl,tr,br,bl

def green_mask(f):
    hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV)
    m = cv2.inRange(hsv, (40, 45, 120), (95, 255, 255))
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((5,5), np.uint8))
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((9,9), np.uint8))
    return m

def robust_line(a, b):
    # fit b = k*a + c, drop outliers twice
    keep = np.ones(len(a), bool)
    for _ in range(3):
        k, c = np.polyfit(a[keep], b[keep], 1)
        r = np.abs(b - (k*a + c)); thr = max(1.5, np.percentile(r[keep], 80)*2)
        keep = r < thr
    return k, c

def quad(f):
    m = green_mask(f)
    cnts, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    c = max(cnts, key=cv2.contourArea)
    mm = np.zeros_like(m); cv2.drawContours(mm, [c], -1, 255, -1)
    x, y, w, h = cv2.boundingRect(c)
    cols = np.arange(x + int(w*0.2), x + int(w*0.8))
    rows = np.arange(y + int(h*0.2), y + int(h*0.8))
    sub = mm[:, cols] > 0
    top = sub.argmax(0).astype(float); bot = (mm.shape[0]-1 - sub[::-1].argmax(0)).astype(float)
    subr = mm[rows, :] > 0
    lef = subr.argmax(1).astype(float); rig = (mm.shape[1]-1 - subr[:, ::-1].argmax(1)).astype(float)
    kt, ct = robust_line(cols.astype(float), top)   # y = kt*x + ct
    kb, cb = robust_line(cols.astype(float), bot)
    kl, cl = robust_line(rows.astype(float), lef)   # x = kl*y + cl
    kr, cr = robust_line(rows.astype(float), rig)
    def inter(kh, ch, kv, cv):                       # y = kh*x+ch ; x = kv*y+cv
        yy = (kh*cv + ch) / (1 - kh*kv); return [kv*yy + cv, yy]
    q = np.array([inter(kt,ct,kl,cl), inter(kt,ct,kr,cr), inter(kb,cb,kr,cr), inter(kb,cb,kl,cl)], np.float32)
    return q, m

Q = []; masks = []
for f in frames:
    q, m = quad(f); Q.append(q); masks.append(m)
Q = np.array(Q)                      # N x 4 x 2
# temporal smoothing (centered moving average, 7 frames) to kill jitter
k = 7; pad = np.pad(Q, ((k//2, k//2), (0,0), (0,0)), mode="edge")
Qs = np.stack([pad[i:i+N].astype(np.float64) for i in range(k)]).mean(0)
json.dump({"first": Qs[0].tolist(), "spread": float(np.abs(Q-Qs).max())}, sys.stderr); print(file=sys.stderr)

def plate_idx(n):
    p = n % (2*N - 2) if N > 1 else 0
    return p if p < N else 2*N - 2 - p

src = np.float32([[0,0],[SW,0],[SW,SH],[0,SH]])
ff = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s",f"{OW}x{OH}","-r",str(fps),"-i","-",
                       "-c:v","libx264","-preset","medium","-crf","15","-pix_fmt","yuv420p",OUT], stdin=subprocess.PIPE)
total = int(round(DUR*fps))
for n in range(total):
    t = n / fps
    name = [s for st,s in SCHED if st <= t + 1e-6][-1]
    i = plate_idx(n); f = frames[i].copy(); q = Qs[i].astype(np.float32)
    # expand quad 1.5px outward from its centre to avoid green fringe
    c = q.mean(0); qe = c + (q - c) * (1 + 1.5/np.linalg.norm(q - c, axis=1, keepdims=True))
    H = cv2.getPerspectiveTransform(src, qe.astype(np.float32))
    warped = cv2.warpPerspective(slides[name], H, (OW, OH), flags=cv2.INTER_AREA, borderMode=cv2.BORDER_REPLICATE)
    warped = cv2.GaussianBlur(warped, (0,0), 0.7)
    alpha = cv2.warpPerspective(np.full((SH,SW), 255, np.uint8), H, (OW, OH), flags=cv2.INTER_LINEAR)
    alpha = cv2.GaussianBlur(alpha, (0,0), 0.8).astype(np.float32)/255.0
    # projector shading: keep the plate's own brightness falloff / hotspot / flicker
    Y = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY).astype(np.float32)
    Y = cv2.GaussianBlur(Y, (0,0), 6)
    shade = np.clip(Y / REF_Y, 0.55, 1.15)[..., None]
    proj = np.clip(warped.astype(np.float32) * shade, 0, 255)
    out = f.astype(np.float32)*(1-alpha[...,None]) + proj*alpha[...,None]
    ff.stdin.write(out.astype(np.uint8).tobytes())
ff.stdin.close(); ff.wait(); print("done", total, "frames", file=sys.stderr)
