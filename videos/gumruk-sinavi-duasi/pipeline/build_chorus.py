import numpy as np, subprocess, glob, os
SR=44100
rng=np.random.default_rng(7)
def load(p):
    raw=subprocess.run(["ffmpeg","-v","error","-i",p,"-ac","1","-ar",str(SR),"-f","f32le","-"],capture_output=True).stdout
    return np.frombuffer(raw,np.float32).copy()
ids="cCz3gXRTeByy6HXRojnS ElF2zqfT2i84LaiegmZX OszGQWL8MORcIF5RKaeJ l2kIt7X2tQVI8Hj504lK KaiixBR7Md3nzWZOKKjq EChFrdZVQYMsH2bmkFgi 2bHyuhTYKTHzhqKVoh3W o2VVSsAY2gzVg7ZLxfpC 9cs2L7vcpX4QGTWfRZEW LYEu1wZiNzgX2aD6bq7Z 9bxyfO7nHQg93rW8UxVa CEt6TP0NbjGQ7TWcZ7Sc".split()
L=int(2.2*SR); mixL=np.zeros(L); mixR=np.zeros(L)
copies=0
for rep in range(2):          # each take used twice with different pitch/offset -> ~24 voices
    for i in ids:
        x=load(f"../assets/tts/{i}.bin")
        # trim leading silence
        nz=np.where(np.abs(x)>0.02)[0]
        if len(nz)==0: continue
        x=x[max(0,nz[0]-200):nz[-1]+2000]
        x=x/ (np.abs(x).max()+1e-9)
        r=rng.uniform(0.93,1.08) if rep else rng.uniform(0.97,1.03)  # pitch/speed variation
        n=int(len(x)/r); x=np.interp(np.linspace(0,len(x)-1,n),np.arange(len(x)),x)
        off=int(rng.uniform(0,0.14 if rep==0 else 0.22)*SR)
        g=rng.uniform(0.35,0.8)*(0.8 if rep else 1.0)
        pan=rng.uniform(-0.8,0.8)
        e=min(L,off+len(x)); seg=x[:e-off]*g
        mixL[off:e]+=seg*(1-pan)/2*1.4; mixR[off:e]+=seg*(1+pan)/2*1.4
        copies+=1
st=np.stack([mixL,mixR],1); st/=np.abs(st).max()+1e-9; st*=0.9
subprocess.run(["ffmpeg","-v","error","-y","-f","f32le","-ar",str(SR),"-ac","2","-i","-","-af",
 "highpass=f=140,lowpass=f=7000,aecho=0.8:0.7:35|60|95:0.25|0.18|0.12,acompressor=threshold=-14dB:ratio=3,alimiter=limit=0.95",
 "chorus.wav"],input=st.astype(np.float32).tobytes())
print("voices",copies)
