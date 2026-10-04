from PIL import Image, ImageDraw, ImageFont
W,H=1650,1000
FONT="../assets/fonts/Carlito-Bold.ttf"
BG=(141,251,203)        # matches projected mint green in plate
BOX=(222,218,190)       # PowerPoint tan text box
TXT=(78,74,46)          # dark olive text
RED=(192,80,77)         # PowerPoint accent red (title)
def words_wrap(draw, tokens, font, maxw):
    # tokens: list of (word,color); returns lines of token lists
    lines=[[]]; cur=0; sp=draw.textlength(" ",font=font)
    for w,c in tokens:
        if w=="\n": lines.append([]); cur=0; continue
        wl=draw.textlength(w,font=font)
        if lines[-1] and cur+sp+wl>maxw: lines.append([]); cur=0
        cur += (sp if lines[-1] else 0)+wl; lines[-1].append((w,c))
    return lines
def toks(text, colors=None):
    colors=colors or {}
    out=[]
    for para in text.split("\n"):
        for w in para.split():
            out.append((w, colors.get(w.strip(',.'), TXT)))
        out.append(("\n",None))
    return out[:-1]
def slide(name, text, colors=None, title=None, size=80, box_cy=None, hide_from=None, boxw=1380):
    im=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(im)
    f=ImageFont.truetype(FONT,size)
    top=90
    if title:
        tf=ImageFont.truetype(FONT,128)
        tw=d.textlength(title,font=tf); d.text(((W-tw)/2,top),title,font=tf,fill=RED); top=top+170
    tk=toks(text,colors)
    maxw=boxw-110
    n=len(words_wrap(d,tk,f,maxw)); lo,hi=300,maxw
    while hi-lo>4:                       # balanced wrap: narrowest width with same line count
        mid=(lo+hi)/2
        if len(words_wrap(d,tk,f,mid))>n: lo=mid
        else: hi=mid
    lines=words_wrap(d,tk,f,hi)
    lh=int(size*1.18); pad=48
    bh=len(lines)*lh+2*pad-int(size*0.18)
    if box_cy is None: by=top
    else: by=int(box_cy-bh/2)
    bx=(W-boxw)//2
    d.rectangle([bx,by,bx+boxw,by+bh],fill=BOX)
    y=by+pad-int(size*0.12); sp=d.textlength(" ",font=f); count=0
    for li,line in enumerate(lines):
        lw=sum(d.textlength(w,font=f) for w,_ in line)+sp*(len(line)-1)
        x=(W-lw)/2
        for w,c in line:
            if hide_from is None or count<hide_from:
                d.text((x,y),w,font=f,fill=c)
            x+=d.textlength(w,font=f)+sp; count+=1
        y+=lh
    im.save(f"slides/{name}.png")
slide("s1","ALLAH’IM GİRECEĞİM SINAVDA DOĞRU GTİP’İ BULDUR, BULAMADIĞIMI ATTIR, ATTIĞIMI DA TUTTUR",title="GÜMRÜK SINAVI DUASI",size=82,boxw=1480)
slide("s2","İKİ ŞIKTA KALDIĞIM SORULARDA FOB İLE CIF’İ KARIŞTIRMAMAMA YARDIM ET",box_cy=560,size=92,boxw=1480)
slide("s3","BEYANNAMELERİMİ KIRMIZI HATTA DEĞİL, YEŞİL HATTA DÜŞÜR YARABBİM",colors={"KIRMIZI":(200,20,20),"YEŞİL":(0,140,60)},box_cy=560,size=92,boxw=1480)
slide("s4","MEVZUAT SORULARININ ÇALIŞTIĞIM MADDEDEN GELMESİNİ NASİP EYLE YARABBİM",box_cy=560,size=92,boxw=1480)
slide("s5","KAMBİYO SORULARINI YAPABİLMEYİ NASİP EYLE YARABBİM",box_cy=560,size=92,boxw=1480)
t6='TARİFEDE ZATEN “DİĞERLERİ”Nİ İŞARETLEYECEĞİM...\nAKSİNİ GÖSTERME YARABBİM'
slide("s6a",t6,box_cy=560,hide_from=4,size=86,boxw=1480)
slide("s6b",t6,box_cy=560,size=86,boxw=1480)
slide("s7","AMİN",size=230,box_cy=520,boxw=820)
print("ok")
