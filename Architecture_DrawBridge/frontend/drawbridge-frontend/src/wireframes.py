# -*- coding: utf-8 -*-
"""Drawbridge UI wireframes -> SVG. Regenerate: python3 src/wireframes.py"""
import os, html

W, H = 1440, 900
NOTE_H = 200
FONT = "Inter, Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, monospace"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "svg")

C = dict(
    bg="#ffffff", shell="#f8fafc", line="#e2e8f0", line2="#cbd5e1",
    ink="#0f172a", mute="#64748b", faint="#94a3b8",
    accent="#1d4ed8", accentbg="#dbeafe",
    danger="#b91c1c", dangerbg="#fee2e2",
    warn="#b45309", warnbg="#fef3c7",
    ok="#15803d", okbg="#dcfce7",
    violet="#6d28d9", violetbg="#ede9fe",
    orange="#c2410c", orangebg="#ffedd5",
)

def e(t): return html.escape(str(t))

def rect(x,y,w,h,fill="none",stroke=None,rx=0,sw=1,dash=None,op=None):
    s=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"'
    if stroke: s+=f' stroke="{stroke}" stroke-width="{sw}"'
    if dash: s+=f' stroke-dasharray="{dash}"'
    if op is not None: s+=f' opacity="{op}"'
    return s+'/>'

def txt(x,y,s,size=14,fill=None,weight=400,anchor="start",family=None,style=None):
    o=f'<text x="{x}" y="{y}" font-family="{family or FONT}" font-size="{size}" fill="{fill or C["ink"]}" font-weight="{weight}" text-anchor="{anchor}"'
    if style: o+=f' font-style="{style}"'
    return o+f'>{e(s)}</text>'

def line(x1,y1,x2,y2,stroke=None,sw=1,dash=None):
    s=f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke or C["line"]}" stroke-width="{sw}"'
    if dash: s+=f' stroke-dasharray="{dash}"'
    return s+'/>'

def pill(x,y,label,fg,bg,size=12,padx=11,h=22,weight=600):
    w=int(len(label)*size*0.60)+padx*2
    return rect(x,y,w,h,bg,fg,rx=h//2)+txt(x+w/2,y+h/2+size*0.36,label,size,fg,weight,"middle"), w

def btn(x,y,label,fg="#ffffff",bg=None,w=None,h=38,size=13.5,outline=False):
    bg = bg or C["accent"]
    w = w or int(len(label)*size*0.62)+40
    if outline:
        s=rect(x,y,w,h,"#ffffff",C["line2"],rx=8)+txt(x+w/2,y+h/2+5,label,size,C["ink"],600,"middle")
    else:
        s=rect(x,y,w,h,bg,rx=8)+txt(x+w/2,y+h/2+5,label,size,fg,700,"middle")
    return s,w

def bar(x,y,w,h,pct,fill,track="#e2e8f0"):
    return rect(x,y,w,h,track,rx=h//2)+rect(x,y,max(2,int(w*pct)),h,fill,rx=h//2)

def pin(x,y,n):
    return (f'<circle cx="{x}" cy="{y}" r="13" fill="{C["accent"]}" stroke="#ffffff" stroke-width="2"/>'
            + txt(x,y+5,str(n),13,"#fff",700,"middle"))

def ph(x,y,w,h,label=""):
    s=rect(x,y,w,h,C["shell"],C["line2"],rx=6,dash="5 4")
    if label: s+=txt(x+w/2,y+h/2+5,label,13,C["faint"],500,"middle")
    return s

def wrap(s,n):
    words,lines,cur=s.split(),[],""
    for w_ in words:
        if len(cur)+len(w_)+1<=n: cur=(cur+" "+w_).strip()
        else: lines.append(cur); cur=w_
    if cur: lines.append(cur)
    return lines

def notes(items,y=H):
    o=[rect(0,y,W,NOTE_H,"#0b1220"), txt(28,y+32,"WHY IT LOOKS LIKE THIS",11,"#64748b",700)]
    colw=(W-56)/len(items)
    for i,(n,title,body) in enumerate(items):
        cx=28+i*colw
        o.append(pin(cx+13,y+62,n))
        for j,ln in enumerate(wrap(title,int(colw/8.6))):
            o.append(txt(cx+36,y+67+j*17,ln,13.5,"#e2e8f0",700))
        yy=y+96+ (17 if len(wrap(title,int(colw/8.6)))>1 else 0)
        for ln in wrap(body,int(colw/6.2)):
            o.append(txt(cx,yy,ln,12,"#94a3b8")); yy+=17
    return "".join(o)

def svg(body,title,height=H+NOTE_H):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {height}" width="{W}" height="{height}">'
            f'<title>{e(title)}</title><rect width="{W}" height="{height}" fill="{C["bg"]}"/>'+body+'</svg>')

def save(name,content):
    open(os.path.join(OUT,name+".svg"),"w").write(content); print("wrote",name)

def topbar(active="Queue",compressed=True):
    o=[rect(0,0,W,64,"#ffffff"),line(0,64,W,64,C["line"])]
    o.append(rect(28,20,24,24,C["accent"],rx=6)); o.append(txt(40,37,"D",13,"#fff",800,"middle"))
    o.append(txt(62,38,"Drawbridge",17,C["ink"],700))
    x=200
    for item in ["Queue","Vendors","Binders","Docs"]:
        w=len(item)*8+26
        if item==active: o.append(rect(x-8,18,w,28,C["accentbg"],rx=6))
        o.append(txt(x+w/2-8,37,item,13.5,C["accent"] if item==active else C["mute"],600,"middle"))
        x+=w+10
    sx=612
    for lab,val in [("Active reviews","3"),("Events processed","1,284"),("Spend today","$2.17"),("Avg / review","$0.41")]:
        o.append(txt(sx,26,lab.upper(),9,C["faint"],700)); o.append(txt(sx,45,val,15,C["ink"],700)); sx+=126
    if compressed:
        p,w=pill(W-300,21,"TIME-COMPRESSED DEMO · 1s = 4 min",C["warn"],C["warnbg"],size=11)
        o.append(p)
    return "".join(o)
