import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wireframes import *

# =================== W5 · GATE CARD (G1 risk acceptance) ===================
o=[topbar("Queue")]
o.append(rect(0,64,W,H-64,C["shell"]))
o.append(rect(0,64,W,60,C["orangebg"])); o.append(rect(0,64,6,60,C["orange"]))
o.append(txt(32,101,"This review is waiting on you.  ",14,C["orange"],800))
o.append(txt(276,101,"DataDynamo Logistics has been scored and parked at the risk-acceptance gate since 09:14 today.",13,"#7c2d12"))

o.append(txt(28,166,"DataDynamo Logistics",24,C["ink"],700))
p,w=pill(312,148,"TIER 1",C["mute"],C["shell"],size=10); o.append(p)
p,w=pill(312+w+8,148,"GATED · scope decision",C["orange"],C["orangebg"],size=10); o.append(p)
o.append(txt(28,190,"Freight operations platform · production system access · ~$120k/yr · reviewed over 12 days",12.5,C["mute"]))
o.append(txt(1180,178,"71",40,C["warn"],700,"middle")); o.append(txt(1180,198,"RISK SCORE",9,C["faint"],700,"middle"))
p,w=pill(1246,156,"CONDITIONAL",C["warn"],C["warnbg"],size=11); o.append(p)

# memo panel
o.append(rect(28,220,880,398,"#ffffff",C["line"],rx=12))
o.append(txt(52,252,"RISK MEMO · written by gemini-pro · $0.09 · 7.4s",10,C["faint"],800))
o.append(txt(52,282,"Recommend conditional approval, with two mandatory mitigations.",15,C["ink"],700))
o.append(line(52,298,884,298,C["line"]))
o.append(txt(52,326,"What drove this",11,C["accent"],800))
drivers=[("Their questionnaire claims MFA is enforced org-wide. Their own SOC 2 exception note 3.2 records an","unremediated MFA gap on administrative access — the highest-privilege accounts are the exception."),
         ("Breach notification is answered as 24 hours; the incident history sheet shows a 2024 incident","disclosed to customers after 9 days. The written commitment and the observed behaviour disagree."),
         ("The ISO 27001 certificate attached expired on 14 March 2025 and no renewal was supplied.","")]
yy=350
for a,b in drivers:
    o.append(txt(60,yy,"·",13,C["warn"],800)); o.append(txt(74,yy,a,12.5,C["ink"]))
    if b: o.append(txt(74,yy+18,b,12.5,C["ink"]))
    yy+= 44 if b else 26
o.append(txt(52,yy+10,"Mitigations required before approval",11,C["accent"],800))
for i,m in enumerate(["Written remediation plan for administrative MFA, with a date, countersigned by their CISO.",
                      "Contractual breach-notification SLA of 72 hours maximum, in the DPA, not in an email."]):
    o.append(txt(60,yy+34+i*22,f"{i+1}.",12.5,C["ink"],700)); o.append(txt(82,yy+34+i*22,m,12.5,C["ink"]))
o.append(txt(52,yy+96,"Re-check in 90 days",11,C["accent"],800))
o.append(txt(52,yy+118,"ISO renewal certificate, and evidence the MFA exception is closed.",12.5,C["ink"]))

# score breakdown
o.append(rect(936,220,476,268,"#ffffff",C["line"],rx=12))
o.append(txt(960,252,"SCORE COMPUTATION",10,C["faint"],800))
o.append(txt(1388,252,"rubric.yaml v1",10,C["faint"],600,"end"))
dom=[("Data protection",20,20),("Access control",15,6),("Incident response",15,7),("Compliance posture",15,9),
     ("Business continuity",10,10),("Subprocessors",10,9),("AI-specific",10,10)]
yy=278
for name,mx,got in dom:
    o.append(txt(960,yy+10,name,12,C["ink"]))
    o.append(bar(1150,yy+2,150,8,got/mx,C["warn"] if got<mx else C["ok"]))
    o.append(txt(1388,yy+10,f"{got} / {mx}",11.5,C["mute"],600,"end"))
    yy+=27
o.append(line(960,yy+2,1388,yy+2,C["line"]))
o.append(txt(960,yy+26,"Total",13,C["ink"],700)); o.append(txt(1388,yy+26,"71 / 95",13,C["ink"],700,"end"))
o.append(txt(960,yy+46,"Deterministic arithmetic over model-judged severities.",11,C["faint"],style="italic"))

# decision panel
o.append(rect(936,508,476,356,"#ffffff",C["orange"],rx=12,sw=2))
o.append(txt(960,540,"YOUR DECISION",10,C["faint"],800))
opts=[("Approve","No conditions. Vendor is onboarded.",C["ok"],False),
      ("Approve with conditions","Mitigations tracked; re-review in 90 days.",C["orange"],True),
      ("Reject","Vendor cannot be onboarded.",C["danger"],False)]
yy=552
for label,sub,col,sel in opts:
    o.append(rect(960,yy,428,46,"#ffffff", col if sel else C["line2"], rx=8, sw=2 if sel else 1))
    o.append(f'<circle cx="{984}" cy="{yy+23}" r="8" fill="#ffffff" stroke="{col if sel else C["line2"]}" stroke-width="2"/>')
    if sel: o.append(f'<circle cx="984" cy="{yy+23}" r="4" fill="{col}"/>')
    o.append(txt(1004,yy+20,label,13,C["ink"],700)); o.append(txt(1004,yy+37,sub,11.5,C["mute"]))
    yy+=54
o.append(ph(960,yy+4,428,40,"Conditions — prefilled from the memo's mitigations, editable"))
p,w=btn(960,yy+54,"Sign and record decision",w=284,h=40,bg=C["orange"]); o.append(p)
p,w=btn(1256,yy+54,"Send back",w=132,h=40,outline=True); o.append(p)
o.append(txt(960,yy+116,"You are signing as Elena Torres, CISO. This writes a signed, single-use approval",11,C["mute"]))
o.append(txt(960,yy+132,"token; no code path can set DECIDED without it.",11,C["mute"]))

o.append(pin(884,246,1)); o.append(pin(1388,540,2)); o.append(pin(1388,290,3)); o.append(pin(1388,844,4))
o.append(notes([
 (1,"The memo is the artefact, and it looks like one","One Pro call, four fixed sections: recommendation, what drove it, mitigations, what to re-check. A CISO reads this and nothing else — so it gets the largest panel on the screen."),
 (2,"Three decisions, not two","Approve / conditional / reject mirrors the score bands. Conditional is pre-selected because that is what the score says — the UI defends the fleet's recommendation without removing the human's choice."),
 (3,"Show the arithmetic beside the decision","Per-domain bars answer 'why 71?' before it is asked, and the italic line names who computed it. The same table prints as binder section 5."),
 (4,"Name the signer, state the mechanism","'Signing as Elena Torres' plus the token sentence turns a button into an accountable act — and it is the sentence to read aloud at 2:50."),
]))
save("W5-gate-risk-acceptance", svg("".join(o), "Drawbridge — G1 risk acceptance gate"))

# =================== W6 · P1 FIRST CONTACT + NEEDS_HUMAN ===================
o=[topbar("Queue")]
o.append(rect(0,64,W,H-64,C["shell"]))
o.append(txt(28,116,"Two things need a human",22,C["ink"],700))
o.append(txt(28,140,"The fleet parked both rather than guessing. Neither is an error state.",13.5,C["mute"]))

# P1 card
o.append(rect(28,172,680,420,"#ffffff",C["orange"],rx=12,sw=2))
o.append(rect(28,172,680,52,C["orangebg"]))
o.append(txt(52,204,"P1 · FIRST OUTBOUND CONTACT",11,C["orange"],800))
p,w=pill(560,183,"BLOCKED BY GATEWAY",C["orange"],"#ffffff",size=10); o.append(p)
o.append(txt(52,254,"The Questionnaire agent wants to email a vendor for the first time.",14.5,C["ink"],700))
o.append(txt(52,278,"NimbusWrite AI · leah@nimbuswrite.ai · 60 questions, Tier 1",12.5,C["mute"]))
o.append(rect(52,298,632,180,C["shell"],C["line"],rx=8))
o.append(txt(72,324,"Subject: Security review — Northwind Systems",12.5,C["ink"],700,family=MONO))
o.append(line(72,336,664,336,C["line"]))
for i,ln in enumerate(wrap("Hello Leah — Northwind Systems is beginning a security review of NimbusWrite AI ahead of contracting. Please complete the questionnaire at the secure link below. It has 60 questions across eight domains and asks for supporting evidence; you can save and return.",78)):
    o.append(txt(72,360+i*19,ln,12,C["mute"]))
o.append(txt(72,452,"[secure portal link · token-scoped, expires in 14 days]",11.5,C["accent"],family=MONO))
p,w=btn(52,502,"Authorise this thread",w=240,h=42,bg=C["orange"]); o.append(p)
p,w=btn(304,502,"Edit message",w=150,h=42,outline=True); o.append(p)
p,w=btn(466,502,"Decline",w=120,h=42,outline=True); o.append(p)
o.append(txt(52,568,"One tap authorises the thread; later messages are delegated. Review parked in GATED, scope contact.",11.5,C["mute"]))

# NEEDS_HUMAN card
o.append(rect(732,172,680,420,"#ffffff",C["danger"],rx=12,sw=2))
o.append(rect(732,172,680,52,C["dangerbg"]))
o.append(txt(756,204,"NEEDS HUMAN · THE FLEET STOPPED",11,C["danger"],800))
p,w=pill(1252,183,"NO GUESSING",C["danger"],"#ffffff",size=10); o.append(p)
o.append(txt(756,254,"Northwind Payroll — three chases, no reply.",14.5,C["ink"],700))
o.append(txt(756,278,"Questionnaire agent · last contact Day 9 · coverage 34%",12.5,C["mute"]))
o.append(rect(756,298,632,150,C["shell"],C["line"],rx=8))
o.append(txt(776,324,"WHAT THE FLEET DID",9,C["faint"],800))
for i,ln in enumerate(["Day 2 · questionnaire sent, delivery confirmed","Day 5 · chase round 1 — reminder","Day 7 · chase round 2 — deadline notice","Day 9 · chase round 3 — escalation. Cap reached; review parked."]):
    o.append(txt(776,348+i*24,ln,12.5,C["ink"]))
o.append(txt(756,478,"WHAT IT WILL NOT DO",9,C["faint"],800))
for i,ln in enumerate(["Score a vendor on 34% coverage.","Infer missing answers from the documents it does have."]):
    o.append(txt(776,500+i*20,"· "+ln,12.5,C["danger"]))
p,w=btn(756,548,"Reassign to a person",w=210,h=40,bg=C["danger"]); o.append(p)
p,w=btn(978,548,"Extend and retry",w=180,h=40,outline=True); o.append(p)

# DLQ strip
o.append(rect(28,620,1384,110,"#ffffff",C["line"],rx=12))
o.append(txt(52,652,"DEAD-LETTER QUEUE · 0 messages",10,C["faint"],800))
o.append(txt(52,682,"No message has failed five delivery attempts. If one does, its review moves to NEEDS_HUMAN and appears here — visible failure handling, not a silent retry loop.",12.5,C["mute"]))
o.append(txt(52,706,"Ack deadline 60s, extended explicitly around long model calls.",11.5,C["faint"]))
p,w=pill(1200,650,"HEALTHY",C["ok"],C["okbg"],size=11); o.append(p)

o.append(pin(688,262,1)); o.append(pin(1392,262,2)); o.append(pin(1392,644,3)); o.append(pin(688,522,4))
o.append(notes([
 (1,"Show the message before it is sent","Autonomy that asks permission is a stronger claim than autonomy that does not. The human reads the actual email, not a summary of it."),
 (2,"A stall is a feature, presented as one","'The fleet stopped' with what it did and what it refuses to do. Framing this as a designed behaviour rather than an error is the difference between mature and broken."),
 (3,"The DLQ panel is visible when empty","An empty failure panel says the mechanism exists and is being watched. A panel that only appears on failure looks like it was added after the failure."),
 (4,"Both cards state the mechanism in small print","'Parked in GATED, scope contact' and 'cap reached' tell an engineer judge that the state machine is real and that these screens are not mock-ups."),
]))
save("W6-human-gates", svg("".join(o), "Drawbridge — P1 gate and NEEDS_HUMAN"))

# =================== W7 · AUDIT BINDER ===================
o=[topbar("Binders")]
o.append(rect(0,64,W,H-64,C["shell"]))
o.append(txt(28,116,"Audit binder",22,C["ink"],700))
o.append(txt(28,140,"Every binder is generated from the reasoning traces and the event ledger. Nothing is written by hand.",13.5,C["mute"]))
p,w=btn(1160,110,"Export binder (PDF)",w=252,h=44); o.append(p)
o.append(txt(1286,168,"renders in under 3 seconds",11,C["faint"],500,"middle"))

# document preview
o.append(rect(28,190,560,640,"#ffffff",C["line2"],rx=6))
o.append(rect(28,190,560,10,C["accent"]))
o.append(txt(64,262,"VENDOR SECURITY REVIEW",10,C["faint"],800))
o.append(txt(64,300,"NimbusWrite AI",30,C["ink"],700))
o.append(txt(64,326,"Review rev_7f3a91 · Tier 1 · opened 1 Aug 2026 · decided 16 Aug 2026",12,C["mute"]))
o.append(line(64,348,552,348,C["line"]))
for i,(k,v) in enumerate([("Outcome","Escalated — not approved"),("Approver","Elena Torres, CISO · 16 Aug 2026 09:41 UTC"),
                          ("Risk score","31 / 95 · band escalate"),("Adversarial conduct","Yes — attempt recorded, section 3")]):
    o.append(txt(64,382+i*30,k,11,C["faint"],700)); o.append(txt(200,382+i*30,v,12.5,C["ink"],600))
o.append(line(64,512,552,512,C["line"]))
o.append(txt(64,540,"EVIDENCE OF DUE DILIGENCE FOR",10,C["faint"],800))
for i,f in enumerate(["SOC 2 · CC9.2 vendor management","ISO 27001 · A.5.19 – A.5.23","DORA · ICT third-party register","NIS2 · Article 21(2)(d) supply chain"]):
    o.append(txt(64,566+i*24,"· "+f,12.5,C["ink"]))
o.append(txt(64,690,"Generated automatically from OpenTelemetry reasoning traces and the",11.5,C["mute"],style="italic"))
o.append(txt(64,708,"immutable event ledger. 41 pages.",11.5,C["mute"],style="italic"))
o.append(txt(64,790,"drawbridge · binder v1.0",10,C["faint"],family=MONO))

# section list
o.append(rect(620,190,792,410,"#ffffff",C["line"],rx=12))
o.append(txt(648,222,"CONTENTS",10,C["faint"],800))
secs=[("1","Review timeline","every event, in order, with timestamps","4 pp"),
      ("2","Questionnaire answers","with parse provenance and confidence","11 pp"),
      ("3","Evidence inventory","screening verdicts, incl. the blocked payload verbatim","5 pp"),
      ("4","Findings and contradictions","each linked to its source passage","6 pp"),
      ("5","Score computation","the arithmetic, per domain, against rubric.yaml","2 pp"),
      ("6","Human decisions","identity, timestamp, conditions","1 p"),
      ("7","Reasoning-trace appendix","goal and decision per agent step","9 pp"),
      ("8","Post-approval monitoring","watchdog sweeps and signals","3 pp")]
yy=250
for n,title,sub,pp in secs:
    o.append(txt(648,yy+16,n,12,C["accent"],800))
    o.append(txt(676,yy+16,title,13,C["ink"],700))
    o.append(txt(940,yy+16,sub,12,C["mute"]))
    o.append(txt(1388,yy+16,pp,11.5,C["faint"],600,"end"))
    o.append(line(648,yy+28,1388,yy+28,C["line"]))
    yy+=42

o.append(rect(620,624,792,206,"#ffffff",C["line"],rx=12))
o.append(txt(648,656,"PREVIOUS BINDERS",10,C["faint"],800))
prev=[("CleanCloud Analytics","rev_2b81c4","approved","8 Aug 2026",C["ok"]),
      ("DataDynamo Logistics","rev_5c02af","conditional","14 Aug 2026",C["warn"]),
      ("Vertex Freight (2025 review)","rev_91ee30","approved","3 Nov 2025",C["ok"])]
yy=686
for name,rid,out,date,col in prev:
    o.append(txt(648,yy+14,name,13,C["ink"],600))
    o.append(txt(980,yy+14,rid,12,C["faint"],family=MONO))
    p,w=pill(1130,yy,out,col,"#ffffff",size=10); o.append(p)
    o.append(txt(1388,yy+14,date,11.5,C["mute"],anchor="end"))
    o.append(line(648,yy+28,1388,yy+28,C["line"]))
    yy+=44

o.append(pin(560,214,1)); o.append(pin(1388,236,2)); o.append(pin(1160,548,3)); o.append(pin(560,548,4))
o.append(notes([
 (1,"The cover does the arguing","Vendor, outcome, named approver, and the four frameworks this satisfies. An auditor's first question is 'who decided, and when' — it is answered above the fold of page one."),
 (2,"Eight sections with page counts","Page counts make it a document rather than a screen. Forty-one pages produced in under three seconds is a sentence worth saying on camera."),
 (3,"Section 3 contains the blocked payload","Verbatim, as inert evidence. The one place where showing the attack is not only safe but required — a regulator wants to see what was attempted."),
 (4,"Prior binders are listed on the same screen","Continuity is the claim: this is a register, not a one-off export. It is also where a second review of the same vendor becomes visible."),
]))
save("W7-audit-binder", svg("".join(o), "Drawbridge — Audit binder"))
