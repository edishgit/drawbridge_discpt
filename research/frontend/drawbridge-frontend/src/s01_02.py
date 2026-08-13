import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wireframes import *

# ============ W1 · JUDGE ENTRY (the hosted URL) ============
o=[]
o.append(rect(0,0,W,470,"#0b1220"))
o.append(rect(56,44,26,26,C["accent"],rx=7)); o.append(txt(69,63,"D",14,"#fff",800,"middle"))
o.append(txt(94,64,"Drawbridge",18,"#e2e8f0",700))
p,w=pill(232,45,"Fortified Enterprise Fleet",  "#93c5fd", "#172554", size=11); o.append(p)
o.append(txt(W-56,64,"github.com/ambrstack/drawbridge",13,"#64748b",500,"end"))

o.append(txt(56,168,"Vendor security review, run end to end by a fleet of agents.",34,"#f8fafc",700))
o.append(txt(56,214,"Weeks of elapsed time. Minutes of human time. Every decision traced.",34,"#3b82f6",700))
for i,ln in enumerate(wrap("30% of breaches now involve a third party — double last year. The only gate protecting an enterprise from a risky vendor is a 60-question spreadsheet and a three-week email thread. Drawbridge replaces it — and when a vendor's documents try to prompt-inject the reviewer, it drops their Trust Score 25 points and forces the review to escalate.",108)):
    o.append(txt(56,258+i*24,ln,15,"#94a3b8"))

# three doors
doors=[("WATCH","The 4-minute demo","Injection blocked · runtime killed live · human gate · audit binder.","#1d4ed8"),
       ("EXPLORE","A completed review, read-only","NimbusWrite AI, Tier 1 — the review that caught an injection attempt.","#15803d"),
       ("READ","Architecture & security docs","Trust zones, the permission matrix, the idempotency guard.","#6d28d9")]
for i,(kick,title,sub,col) in enumerate(doors):
    x=56+i*448
    o.append(rect(x,352,424,150,"#111c2e","#1e293b",rx=12))
    o.append(rect(x,352,4,150,col,rx=2))
    o.append(txt(x+26,384,kick,10,"#64748b",800))
    o.append(txt(x+26,412,title,17,"#f1f5f9",700))
    for j,ln in enumerate(wrap(sub,46)):
        o.append(txt(x+26,438+j*19,ln,12.5,"#94a3b8"))
    o.append(txt(x+398,478,"→",20,col,700,"end"))

# live proof strip
o.append(rect(0,470,W,110,"#f8fafc")); o.append(line(0,470,W,470,C["line"]))
o.append(txt(56,506,"LIVE, RIGHT NOW",10,C["faint"],800))
stats=[("Reviews completed","24"),("Injection attempts blocked","3"),("Median model cost / review","$0.41"),("Longest review resumed after crash","6 days"),("Human minutes per review","41")]
sx=56
for lab,val in stats:
    o.append(txt(sx,548,val,24,C["ink"],700)); o.append(txt(sx,568,lab,11.5,C["mute"])); sx+=272

# how it works strip
o.append(txt(56,634,"HOW IT WORKS",10,C["faint"],800))
steps=["Intake","Tier & plan","Questionnaire","Screen evidence","Cross-examine","Score","Human gate","Monitor"]
sx=56
for i,s in enumerate(steps):
    wd=150
    o.append(rect(sx,652,wd,54,"#ffffff",C["line"],rx=8))
    o.append(txt(sx+wd/2,676,f"0{i+1}",10,C["faint"],700,"middle"))
    o.append(txt(sx+wd/2,694,s,12.5,C["ink"],600,"middle"))
    if i<7: o.append(txt(sx+wd+8,684,"›",14,C["line2"],700,"middle"))
    sx+=wd+18

o.append(rect(56,742,1328,96,C["dangerbg"] if False else "#fff7ed",C["orange"],rx=10))
o.append(txt(80,776,"The thing to look at first",14,C["orange"],800))
for i,ln in enumerate(wrap("A vendor's uploaded PDF contained hidden white-on-white text instructing the reviewing agent to mark them low-risk and skip evidence checks. Drawbridge blocked it, kept it as inert evidence, and dropped the vendor's Trust Score 25 points for attempted manipulation — because that attempt is itself a finding.",150)):
    o.append(txt(80,800+i*20,ln,13,"#7c2d12"))
p,w=pill(1180,772,"See it in the review →",C["orange"],"#ffedd5",size=12); o.append(p)

o.append(pin(500,382,1)); o.append(pin(56+272*2-24,540,2)); o.append(pin(1160,760,3)); o.append(pin(206,676,4))
o.append(notes([
 (1,"Three doors, no login","The hosted URL must load logged-out (§9). A judge with eight minutes should never hit an auth wall or an empty dashboard. Video, live review, docs — one click each."),
 (2,"Numbers no one else can show","Per-review model cost, blocked attempts, resumed-after-crash. These come from real fields (cost_usd, screenings) so they are claims you can defend, not marketing."),
 (3,"Lead with the differentiator","The injection-as-risk-signal story is the one thing a judge will retell to a colleague. It goes above the fold, in plain language, with a link straight into the evidence."),
 (4,"The pipeline in eight words","Someone who reads nothing else still learns what the fleet does. This strip is the only 'marketing' element on the page."),
]))
save("W1-judge-entry", svg("".join(o), "Drawbridge — Judge entry / hosted URL"))

# ============ W2 · QUEUE ============
o=[topbar("Queue")]
o.append(rect(0,64,W,H-64,C["shell"]))
o.append(txt(28,110,"Review queue",22,C["ink"],700))
o.append(txt(28,134,"Everything the fleet is carrying right now. Two reviews are waiting on you.",13.5,C["mute"]))
p,w=btn(W-200,98,"+ New vendor review"); o.append(p)

chips=[("All",12,False),("Needs you",2,True),("In flight",7,False),("Decided",3,False)]
cx=28
for lab,n,active in chips:
    label=f"{lab} · {n}"
    wd=len(label)*7.4+30
    o.append(rect(cx,158,wd,32,"#ffffff" if not active else C["orangebg"], C["orange"] if active else C["line2"],rx=16))
    o.append(txt(cx+wd/2,179,label,12.5,C["orange"] if active else C["mute"],700 if active else 500,"middle"))
    cx+=wd+10

rows=[
 dict(name="NimbusWrite AI",cat="AI writing SaaS · processes customer text",tier="TIER 1",state="ESCALATE",
      statefg=C["danger"],statebg=C["dangerbg"],score="31",days="Day 15",agent="Risk Scorer · memo written",
      flag="ADVERSARIAL CONDUCT",cost="$0.44",prog=1.0),
 dict(name="DataDynamo Logistics",cat="Freight ops platform · production access",tier="TIER 1",state="GATED · needs you",
      statefg=C["orange"],statebg=C["orangebg"],score="71",days="Day 12",agent="Waiting on Elena Torres, CISO",
      flag="2 CONTRADICTIONS",cost="$0.39",prog=0.85),
 dict(name="Northwind Payroll",cat="Payroll processor · employee PII",tier="TIER 1",state="NEEDS HUMAN",
      statefg=C["danger"],statebg=C["dangerbg"],score="—",days="Day 9",agent="Questionnaire · 3 chases, no reply",
      flag="STALLED",cost="$0.21",prog=0.4),
 dict(name="CleanCloud Analytics",cat="BI dashboards · internal data only",tier="TIER 2",state="DECIDED · approved",
      statefg=C["ok"],statebg=C["okbg"],score="86",days="Closed",agent="Watchdog · monitoring since Aug 8",
      flag="",cost="$0.28",prog=1.0),
]
y=210
for r in rows:
    o.append(rect(28,y,W-56,116,"#ffffff",C["line"],rx=12))
    if r["state"].startswith("ESCALATE") or r["state"].startswith("NEEDS"):
        o.append(rect(28,y,4,116,C["danger"],rx=2))
    elif "GATED" in r["state"]:
        o.append(rect(28,y,4,116,C["orange"],rx=2))
    o.append(txt(56,y+38,r["name"],17,C["ink"],700))
    p,w=pill(56+len(r["name"])*9.6+14,y+22,r["tier"],C["mute"],C["shell"],size=10); o.append(p)
    o.append(txt(56,y+60,r["cat"],12.5,C["mute"]))
    o.append(txt(56,y+90,r["agent"],12,C["accent"],600))
    # state
    p,w=pill(560,y+26,r["state"],r["statefg"],r["statebg"],size=11.5); o.append(p)
    if r["flag"]:
        p,w2=pill(560,y+58,r["flag"],C["danger"] if r["flag"]!="2 CONTRADICTIONS" else C["warn"],
                  C["dangerbg"] if r["flag"]!="2 CONTRADICTIONS" else C["warnbg"],size=10); o.append(p)
    # score
    o.append(txt(900,y+46,r["score"],28,C["ink"],700,"middle"))
    o.append(txt(900,y+64,"SCORE",9,C["faint"],700,"middle"))
    o.append(txt(1010,y+46,r["days"],14,C["ink"],600,"middle"))
    o.append(txt(1010,y+64,"ELAPSED",9,C["faint"],700,"middle"))
    o.append(txt(1120,y+46,r["cost"],14,C["ink"],600,"middle"))
    o.append(txt(1120,y+64,"MODEL COST",9,C["faint"],700,"middle"))
    o.append(bar(1200,y+52,120,6,r["prog"],C["accent"]))
    if "GATED" in r["state"]:
        p,w=btn(1200,y+72,"Open gate",w=120,h=32,size=12.5,bg=C["orange"]); o.append(p)
    else:
        p,w=btn(1200,y+72,"Open",w=120,h=32,size=12.5,outline=True); o.append(p)
    y+=132

# activity ticker
o.append(rect(28,740,W-56,130,"#ffffff",C["line"],rx=12))
o.append(txt(56,772,"FLEET ACTIVITY",10,C["faint"],800))
o.append(txt(W-56,772,"live · streaming from Pub/Sub",11,C["faint"],500,"end"))
acts=[("09:14:02", C["danger"], "gateway", "P2 BLOCKED — unstamped content rejected before model dispatch · NimbusWrite AI"),
      ("09:13:58", C["warn"],  "armor",   "Screening verdict: prompt_injection · Security-Overview.pdf quarantined, excerpt stored inert"),
      ("09:11:20", C["accent"],"evidence","Cross-examination complete — 2 contradictions, 1 gap · DataDynamo Logistics · Pro · $0.11"),
      ("09:07:44", C["ok"],    "watchdog","Sweep complete — 24 approved vendors checked, 0 signals · Flash · $0.004")]
yy=796
for t,col,agent,msg in acts:
    o.append(txt(56,yy,t,11.5,C["faint"],500,family=MONO))
    o.append(rect(126,yy-12,4,16,col,rx=2))
    o.append(txt(140,yy,agent,11.5,col,700))
    o.append(txt(226,yy,msg,12.5,C["ink"] if col!=C["danger"] else C["danger"]))
    yy+=26

o.append(pin(538,222,1)); o.append(pin(852,232,2)); o.append(pin(1178,352,3)); o.append(pin(120,172,4)); o.append(pin(1000,760,5))
o.append(notes([
 (1,"State is the loudest thing on the row","A judge scanning the queue should see what the fleet is doing without reading. One pill, colour-coded to the same language as the architecture diagrams."),
 (2,"Score, elapsed and cost sit together","Elapsed proves the long-running claim; cost proves the economics claim. Putting them beside the score means one glance carries three arguments."),
 (3,"Left border + button colour for the two rows that need a human","Orange for a gate, red for a stall. Anything the fleet cannot resolve alone is visually louder than anything it can."),
 (4,"'Needs you · 2' is the default filter chip","The product's claim is that humans appear only at decision points. The UI should open on exactly those points, not on a firehose."),
 (5,"A live ticker proves it is running","A blocked-by-policy line appearing on screen during the demo is worth more than the code that produced it. This is where it appears, unprompted."),
]))
save("W2-queue", svg("".join(o), "Drawbridge — Review queue"))
