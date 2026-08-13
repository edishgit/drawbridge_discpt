import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wireframes import *

# =================== W8 · VENDOR PORTAL (untrusted zone) ===================
o=[]
o.append(rect(0,0,W,64,"#ffffff")); o.append(line(0,64,W,64,C["line"]))
o.append(rect(28,20,24,24,C["accent"],rx=6)); o.append(txt(40,37,"D",13,"#fff",800,"middle"))
o.append(txt(62,38,"Drawbridge",16,C["ink"],700))
o.append(txt(176,38,"Secure vendor portal",13,C["mute"]))
o.append(txt(W-28,32,"Signed in via one-time link",11.5,C["faint"],anchor="end"))
o.append(txt(W-28,50,"leah@nimbuswrite.ai · expires in 11 days",11.5,C["faint"],anchor="end"))
o.append(rect(0,64,W,H-64,C["shell"]))

o.append(rect(0,64,W,132,"#ffffff")); o.append(line(0,196,W,196,C["line"]))
o.append(txt(28,110,"Security review — requested by Northwind Systems",21,C["ink"],700))
o.append(txt(28,136,"NimbusWrite AI · Tier 1 assessment · 60 questions across 8 domains · due 22 August 2026",13,C["mute"]))
o.append(bar(28,158,900,10,0.40,C["accent"]))
o.append(txt(28,186,"24 of 60 answered · 3 of 5 documents uploaded · you can save and return at any time",12,C["mute"]))
p,w=btn(1180,120,"Save and exit",w=232,h=42,outline=True); o.append(p)

# question card
o.append(rect(28,224,880,300,"#ffffff",C["line"],rx=12))
o.append(txt(52,256,"DOMAIN 2 · ACCESS CONTROL & IDENTITY  ·  QUESTION 14 OF 60",10,C["faint"],800))
for i,ln in enumerate(wrap("Describe how multi-factor authentication is enforced across your environment. State which account types are covered, name any exceptions including administrative access, and attach the policy document that governs it.",84)):
    o.append(txt(52,290+i*22,ln,14.5,C["ink"],600))
o.append(ph(52,364,832,86,"Answer — long form. Evidence-demanding questions, never yes/no."))
o.append(rect(52,464,220,38,"#ffffff",C["line2"],rx=8)); o.append(txt(162,488,"📎  Attach policy",12.5,C["accent"],600,"middle"))
o.append(txt(292,488,"MFA-policy-v3.pdf attached",12,C["ok"],600))
p,w=btn(700,464,"Next question",w=184,h=38); o.append(p)

# upload dropzone
o.append(rect(936,224,476,300,"#ffffff",C["line"],rx=12))
o.append(txt(960,256,"EVIDENCE",10,C["faint"],800))
o.append(ph(960,272,428,110,""))
o.append(txt(1174,314,"Drop files here",14,C["mute"],600,"middle"))
o.append(txt(1174,336,"SOC 2, ISO certificates, policies · PDF, max 25 MB",11.5,C["faint"],anchor="middle"))
ups=[("SOC 2 Type II 2025.pdf","RECEIVED",C["ok"]),("ISO 27001 cert.pdf","RECEIVED",C["ok"]),("Security-Overview.pdf","PROCESSING",C["warn"])]
yy=402
for n,st,col in ups:
    o.append(txt(960,yy+14,n,12.5,C["ink"]))
    p,w=pill(1300,yy,st,col,"#ffffff",size=10); o.append(p)
    o.append(line(960,yy+28,1388,yy+28,C["line"]))
    yy+=40

# why we ask
o.append(rect(28,552,880,150,"#ffffff",C["line"],rx=12))
o.append(txt(52,584,"WHY THIS TAKES 60 QUESTIONS",10,C["faint"],800))
for i,ln in enumerate(wrap("Northwind's reviewers read every answer against the evidence you attach. Specific answers with documents shorten the review; vague answers generate follow-ups. Everything you submit is processed automatically and screened before a reviewer sees it.",108)):
    o.append(txt(52,612+i*20,ln,12.5,C["mute"]))
o.append(txt(52,682,"Questions about the review? Reply to the thread with Northwind — a human reads it.",12,C["accent"],600))

# trust-zone annotation
o.append(rect(936,552,476,150,C["dangerbg"],C["danger"],rx=12,sw=2))
o.append(txt(960,584,"THIS IS THE UNTRUSTED ZONE",10,C["danger"],800))
for i,ln in enumerate(wrap("Everything submitted here is authored by the party under review. Uploads land in a quarantine bucket that no agent can read, are text-extracted locally, PII-scrubbed, and screened by Model Armor before any model sees a word.",52)):
    o.append(txt(960,612+i*18,ln,12,"#7f1d1d"))
o.append(txt(960,690,"Annotation for the reader — not shown to the vendor.",11,C["danger"],style="italic"))

o.append(pin(884,248,1)); o.append(pin(1392,248,2)); o.append(pin(884,576,3)); o.append(pin(936,120,4))
o.append(notes([
 (1,"One question at a time, not a 60-row form","The style rule from the question bank shows up as UI: long-form answers with an attachment slot. A spreadsheet-shaped form produces spreadsheet-shaped answers."),
 (2,"Uploads show a processing state","'Processing' is the screening pipeline, visible to the vendor. It is honest, and on camera it is the fifteen seconds before the injection is caught."),
 (3,"Explain the ask","The vendor is a person doing unpaid work. One short paragraph on why specificity shortens the review buys better answers than any amount of chasing."),
 (4,"Deliberately minimal","This surface earns about fifteen seconds of screen time. Build it, do not polish it — every hour here is an hour not spent on the dashboard."),
]))
save("W8-vendor-portal", svg("".join(o), "Drawbridge — Vendor portal (untrusted zone)"))

# =================== W9 · INBOX SIMULATOR / CRASH PROOF ===================
o=[]
o.append(rect(0,0,W,64,"#0b1220"))
o.append(txt(28,39,"Vendor inbox simulator",16,"#e2e8f0",700))
o.append(txt(276,39,"leah@nimbuswrite.ai",13,"#64748b"))
p,w=pill(W-420,21,"SIMULATED MAIL CHANNEL · SMTP-adapter compatible","#93c5fd","#172554",size=11); o.append(p)
o.append(rect(0,64,W,H-64,C["shell"]))

o.append(rect(28,96,1384,86,"#ffffff",C["ok"],rx=12,sw=2))
o.append(txt(56,132,"1 message.",20,C["ok"],800))
o.append(txt(212,132,"The runtime was killed at 09:14:22 and restarted at 09:14:51, mid-send. The vendor received exactly one questionnaire.",14,C["ink"]))
o.append(txt(56,160,"idem_key  rev_7f3a91:questionnaire_send:v1  ·  status done  ·  claimed 09:14:19  ·  completed 09:14:20  ·  replay at 09:14:53 returned the recorded result",11.5,C["mute"],family=MONO))

# mailbox
o.append(rect(28,204,1384,300,"#ffffff",C["line"],rx=12))
o.append(txt(56,236,"INBOX",10,C["faint"],800))
o.append(rect(56,252,1328,72,C["shell"],C["line"],rx=8))
o.append(txt(80,282,"Northwind Systems",13.5,C["ink"],700))
o.append(txt(80,304,"Security review — Northwind Systems",13,C["mute"]))
o.append(txt(1360,282,"09:14:20",12,C["faint"],anchor="end"))
p,w=pill(1200,296,"DELIVERED ONCE",C["ok"],C["okbg"],size=10); o.append(p)
o.append(txt(56,368,"No other messages. No duplicate. No retry storm.",13,C["mute"],style="italic"))
o.append(txt(56,400,"The gateway attempted the send twice — once before the crash and once during replay after restart.",12.5,C["ink"]))
o.append(txt(56,422,"The second attempt was refused by the idempotency ledger before it reached the mail channel.",12.5,C["ink"]))
o.append(rect(56,446,1328,42,"#0b1220",rx=8))
o.append(txt(76,472,'09:14:53  idempotency  SKIP  rev_7f3a91:questionnaire_send:v1 already done — side effect not re-executed',12,"#86efac",family=MONO))

# the two-column proof
o.append(rect(28,528,676,300,"#ffffff",C["line"],rx=12))
o.append(txt(56,560,"WHAT THE OPERATOR SAW",10,C["faint"],800))
ev=[("09:14:19","checkpoint","step questionnaire_send started",C["accent"]),
    ("09:14:19","idempotency","claim taken, status in_progress",C["accent"]),
    ("09:14:20","gateway","send permitted, token spent",C["ok"]),
    ("09:14:22","runtime","SIGKILL — process terminated",C["danger"]),
    ("09:14:22","dashboard","review parked, current_step visible",C["warn"]),
    ("09:14:51","runtime","restarted, replaying plan",C["accent"]),
    ("09:14:53","idempotency","already done — skipped",C["ok"]),
    ("09:14:53","runtime","resumed at evidence_review",C["ok"])]
yy=588
for t,src,msg,col in ev:
    o.append(txt(56,yy,t,11.5,C["faint"],family=MONO))
    o.append(rect(130,yy-11,3,14,col,rx=2))
    o.append(txt(142,yy,src,11.5,col,700)); o.append(txt(246,yy,msg,12,C["ink"]))
    yy+=29

o.append(rect(736,528,676,300,"#ffffff",C["line"],rx=12))
o.append(txt(764,560,"WHAT THE VENDOR SAW",10,C["faint"],800))
o.append(txt(764,606,"One email.",26,C["ink"],700))
for i,ln in enumerate(wrap("That is the entire claim. An enterprise workflow that runs for weeks will be interrupted — by a deploy, a quota, a crash. The question is never whether it stops, it is what the outside world experiences when it starts again.",56)):
    o.append(txt(764,640+i*20,ln,13,C["mute"]))
o.append(rect(764,742,616,58,C["okbg"],C["ok"],rx=8))
o.append(txt(788,768,"For email, the safe default is do not resend and flag for confirmation —",12,"#14532d"))
o.append(txt(788,786,"the conservative choice a security product should make.",12,"#14532d"))

o.append(pin(1392,120,1)); o.append(pin(1392,240,2)); o.append(pin(676,552,3)); o.append(pin(1392,552,4))
o.append(notes([
 (1,"Lead with the number","'1 message' in green, at the top, before any explanation. The proof is a count — everything under it is the audit trail for someone who wants to check."),
 (2,"Show the mailbox, not a claim about the mailbox","At 2:40 in the video the camera cuts here. A single row in an inbox after a live crash is the most convincing thing in the submission."),
 (3,"Operator view and vendor view, side by side","Eight log lines versus one email. That asymmetry is the entire value of idempotency, drawn without a paragraph of explanation."),
 (4,"Name it as a simulated channel, in the header","Honesty about the mail simulator costs nothing and pre-empts the one question that could undermine an otherwise perfect demo beat."),
]))
save("W9-inbox-crash-proof", svg("".join(o), "Drawbridge — Inbox simulator / crash proof"))

# =================== W10 · DOCS SITE ===================
D=dict(bg="#0b1220", panel="#111c2e", line="#1e293b", ink="#e2e8f0", mute="#94a3b8", faint="#64748b", accent="#60a5fa")
o=[rect(0,0,W,H,D["bg"])]
o.append(rect(0,0,W,60,D["panel"])); o.append(line(0,60,W,60,D["line"]))
o.append(rect(28,18,24,24,C["accent"],rx=6)); o.append(txt(40,35,"D",13,"#fff",800,"middle"))
o.append(txt(62,36,"Drawbridge docs",15,D["ink"],700))
x=240
for item,act in [("Overview",False),("Getting started",False),("Architecture",True),("Security",False),("Live demo",False)]:
    wd=len(item)*7.6+24
    if act: o.append(rect(x-6,16,wd,28,"#172554",rx=6))
    o.append(txt(x+wd/2-6,35,item,12.5,D["accent"] if act else D["mute"],600,"middle")); x+=wd+12
o.append(ph(1120,16,180,28,"")); o.append(txt(1210,35,"Search docs  ⌘K",11.5,D["faint"],anchor="middle"))
p,w=pill(1318,18,"v1.2 · GitHub","#93c5fd","#172554",size=11); o.append(p)

# left nav
o.append(rect(0,60,260,H-60,D["panel"]))
nav=[("ARCHITECTURE",None),("01 System overview",True),("02 The fleet",False),("03 Event backbone",False),
     ("04 Memory hierarchy",False),("05 State machine",False),("06 Idempotency & resume",False),
     ("SECURITY",None),("07 Trust zones",False),("08 Adversarial content",False),("09 Permission matrix",False),
     ("10 Human gates",False),("OPERATIONS",None),("11 Deployment & cost",False),("12 Audit binder",False)]
yy=100
for label,act in nav:
    if act is None:
        o.append(txt(28,yy+14,label,9.5,D["faint"],800)); yy+=34
    else:
        if act: o.append(rect(16,yy-2,228,30,"#172554",rx=6)); o.append(rect(16,yy-2,3,30,C["accent"],rx=2))
        o.append(txt(32,yy+18,label,12.5,D["accent"] if act else D["mute"],600 if act else 400)); yy+=30

# content
o.append(txt(300,120,"01 · System overview",30,D["ink"],700))
o.append(rect(300,146,700,64,"#0f1a2e",D["line"],rx=8)); o.append(rect(300,146,3,64,C["accent"],rx=2))
o.append(txt(320,172,"Canonical · read this first",12,D["accent"],700))
o.append(txt(320,194,"Untrusted content → screening → gateway → fleet → state → governance. Eight zones, two claims.",12,D["mute"]))
o.append(txt(300,254,"The whole system on one page",19,D["ink"],700))
o.append(ph(300,276,1080,300,""))
o.append(txt(840,410,"[ embedded diagram 01 — system architecture ]",13,D["faint"],anchor="middle"))
o.append(txt(840,436,"rendered from the same .mmd source shipped in docs/diagrams/",11.5,D["faint"],anchor="middle"))
p,w=pill(1240,292,"⤢ Expand","#93c5fd","#172554",size=11); o.append(p)
p,w=pill(1240,320,"⧉ Copy source","#93c5fd","#172554",size=11); o.append(p)
for i,ln in enumerate(wrap("Every zone is detailed in its own page (number in parentheses). The fleet knows nothing about vendor risk that is not in the rubric and the question bank — the domain lives in configuration, not in prompts.",120)):
    o.append(txt(300,606+i*22,ln,13.5,D["mute"]))
o.append(rect(300,668,1080,86,"#0f1a2e",D["line"],rx=8))
o.append(txt(324,700,"Try it",11,D["accent"],800))
o.append(txt(324,726,"make bootstrap && make seed && make deploy && make demo --vendor nimbuswrite",13,"#86efac",family=MONO))
o.append(txt(324,746,"Thirty minutes from a clean project to a blocked injection.",11.5,D["faint"]))

# right toc
o.append(txt(1180,120,"ON THIS PAGE",9.5,D["faint"],800))
for i,t in enumerate(["The whole system on one page","Trust zones","The runtime loop","Where state lives","What each agent may do"]):
    o.append(txt(1180,148+i*24,t,11.5,D["accent"] if i==0 else D["mute"]))

o.append(pin(280,180,1)); o.append(pin(1360,292,2)); o.append(pin(1360,682,3)); o.append(pin(240,100,4))
o.append(notes([
 (1,"Every page opens with a one-line summary","Status, priority, and the page in a single sentence. A judge sampling three pages learns the shape of the system without reading any of them fully."),
 (2,"Diagrams are embedded, expandable, and copyable","Same .mmd sources that ship in docs/diagrams/. 'Copy source' signals the diagrams are generated artefacts, not screenshots of a whiteboard."),
 (3,"A runnable command on the canonical page","The README spin-up is a graded item. Repeating the four-command path inside the docs is where a judge decides whether they believe it."),
 (4,"Numbered pages, grouped by concern","Architecture, Security, Operations. The numbering matches the diagram set, so a reference in the video or the article lands somewhere specific."),
]))
save("W10-docs-site", svg("".join(o), "Drawbridge — Docs site"))
