import numpy as np, subprocess, json
SR=44100
TEMPO=1.15
def load(p):
    raw=subprocess.run(["ffmpeg","-v","error","-i",p,"-ac","1","-ar",str(SR),"-f","f32le","-"],capture_output=True).stdout
    return np.frombuffer(raw,np.float32).copy()
def save(p,x):
    subprocess.run(["ffmpeg","-v","error","-y","-f","f32le","-ar",str(SR),"-ac","1","-i","-",p],input=x.astype(np.float32).tobytes())
vo=load("../assets/tts/yo9xMKED25helMkwebzE.wav")
segs=[(1.33,7.14),(8.14,13.27),(14.19,18.73),(19.30,25.50),(26.43,31.83),(32.75,37.87),(38.89,41.75)]
gaps=[0.42,0.42,0.42,0.42,0.42,0.80,0]
lead=0.40
out=[np.zeros(int(lead*SR),np.float32)]
t=lead; times=[]
for (a,b),g in zip(segs,gaps):
    x=vo[int(a*SR):int(b*SR)].copy()
    f=int(0.012*SR); x[:f]*=np.linspace(0,1,f); x[-f:]*=np.linspace(1,0,f)
    times.append([t,t+len(x)/SR]); out.append(x); t+=len(x)/SR
    out.append(np.zeros(int(g*SR),np.float32)); t+=g
y=np.concatenate(out)
save("vo_slow.wav",y)
subprocess.run(["ffmpeg","-v","error","-y","-i","vo_slow.wav","-af",f"atempo={TEMPO}","vo_fast.wav"])
times=[[round(a/TEMPO,3),round(b/TEMPO,3)] for a,b in times]
dur=float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0","vo_fast.wav"],capture_output=True,text=True).stdout)
json.dump({"lines":times,"vo_dur":dur},open("vo_times.json","w"),indent=1)
print(json.dumps({"lines":times,"vo_dur":dur}))
