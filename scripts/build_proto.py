"""Zeven statische HTML-schermen (mobiel, 390px) voor een Miro-prototype.
Zelfde huisstijl als de app, geen script. Gevuld met het voorbeeld belastingplan -> Inkomen.
Usage: python3 -I scripts/build_proto.py  -> proto/s1.html .. s7.html
"""
import json, os, html
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rd = lambda p: json.load(open(os.path.join(root, p), encoding="utf-8"))
PR = {p["id"]: p for p in rd("data/principes.json")["principes"]}
OP = rd("data/opening.json")["items"]
e = lambda s: html.escape(str(s or ""))

CSS = """
<meta charset="utf-8"><meta name="viewport" content="width=390">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,400;8..60,500&family=Atkinson+Hyperlegible:wght@400;700&display=swap">
<style>
:root{--blue:#154273;--tint:#E6EDF5;--mid:#C4D3E6;--fg:#1B1F26;--muted:#5B6473;--line:#CFD7E2;--surface:#F6F8FB}
*{box-sizing:border-box}body{margin:0;width:390px;min-height:844px;background:#fff;color:var(--fg);font-family:"Atkinson Hyperlegible",Arial,sans-serif;font-size:15px;line-height:1.45}
.band{background:var(--blue);color:#fff;padding:14px 16px 12px}
.brand{font-family:"Source Serif 4",Georgia,serif;font-size:20px;line-height:1.1}.brand small{display:block;font-family:inherit;font-size:10px;letter-spacing:.1em;text-transform:uppercase;opacity:.75;margin-top:4px;font-family:"Atkinson Hyperlegible",Arial,sans-serif}
.rail{display:grid;grid-template-columns:repeat(7,1fr);gap:6px;margin-top:14px}
.rail span{border-top:2px solid rgba(255,255,255,.3);padding-top:5px;font-size:10.5px;color:rgba(255,255,255,.55)}.rail .done{border-top-color:#fff;color:rgba(255,255,255,.8)}.rail .cur{border-top-color:#fff;color:#fff;font-weight:700}
.wrap{padding:22px 16px 90px}
.stepno{font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--blue);font-weight:700;margin-bottom:6px}
h1{font-family:"Source Serif 4",Georgia,serif;font-weight:500;font-size:27px;line-height:1.15;margin:0 0 8px}
.lede{font-family:"Source Serif 4",Georgia,serif;font-size:17px;color:var(--muted);line-height:1.4;margin:0 0 20px}
.grp{font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin:22px 0 6px;display:flex;justify-content:space-between}
.row{border-top:1px solid var(--line);padding:12px 0 12px 16px;position:relative}.row:last-of-type{border-bottom:1px solid var(--line)}
.row::before{content:"";position:absolute;left:0;top:13px;bottom:13px;width:3px;background:transparent}
.row.sel{background:var(--tint)}.row.sel::before{background:var(--blue)}
.row .h{font-family:"Source Serif 4",Georgia,serif;font-size:18px;line-height:1.2;display:flex;justify-content:space-between;gap:10px;align-items:baseline;margin-bottom:3px}
.row .s{font-size:13.5px;color:var(--muted)}.row .z{font-size:14.5px;margin-top:6px;border-left:2px solid var(--mid);padding-left:10px}
.flat{background:var(--surface);border:1px solid var(--line);border-left:3px solid var(--blue);padding:12px 14px;margin-bottom:14px}
.chip{display:inline-block;font-size:10px;letter-spacing:.08em;text-transform:uppercase;padding:2px 6px;border:1px solid var(--line);color:var(--muted);white-space:nowrap}
.chip.meting{border-color:var(--blue);color:var(--blue)}.chip.ruw{background:var(--tint);border-color:var(--mid);color:var(--blue)}
.wait{background:var(--tint);border-left:3px solid var(--blue);padding:10px 12px;font-size:13.5px;margin:12px 0}
.bar{position:absolute;left:0;right:0;bottom:0;display:flex;justify-content:space-between;padding:14px 16px 18px;border-top:2px solid var(--blue);background:#fff}
.btn{background:var(--blue);color:#fff;border:1px solid var(--blue);padding:11px 18px;font-weight:700;font-size:15px}.btn.ghost{background:none;color:var(--blue);border-color:var(--line)}.btn.off{opacity:.35}
.kiz{border-top:1px solid var(--line);margin:12px 0}.kiz div{padding:9px 0 9px 12px;border-bottom:1px solid var(--line);border-left:3px solid var(--blue);font-size:14.5px}.kiz b{display:block;font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:var(--blue);margin-bottom:2px}
.bel{list-style:none;margin:0;padding:0;border-top:1px solid var(--line)}.bel li{padding:8px 0;border-bottom:1px solid var(--line);font-size:14px}
.score{border-top:1px solid var(--line)}.score div{padding:9px 0;border-bottom:1px solid var(--line);font-size:13px}.score .b{font-weight:700;font-size:14.5px;display:flex;align-items:center;gap:8px;margin-bottom:3px}.score .r{color:var(--muted)}
.dot{width:11px;height:11px;border-radius:50%;border:1.5px solid var(--blue);display:inline-block;flex:none}.dot.h{background:linear-gradient(90deg,var(--blue) 50%,transparent 50%)}.dot.f{background:var(--blue)}
.opt{border:1px solid var(--line);padding:11px 14px;margin-bottom:-1px}.opt.sel{border-color:var(--blue);background:var(--tint);position:relative;z-index:1}.opt .h{font-weight:700;margin-bottom:2px}.opt .s{font-size:13px;color:var(--muted)}
label{display:block;font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--blue);font-weight:700;margin:16px 0 6px}
.field{border:1px solid var(--line);border-bottom:2px solid var(--blue);padding:9px 10px;font-size:14.5px;background:#fff;color:var(--fg)}.field.ph{color:var(--muted)}
.sentence{font-family:"Source Serif 4",Georgia,serif;font-size:23px;line-height:1.3;color:var(--blue);border-top:2px solid var(--blue);border-bottom:1px solid var(--line);padding:14px 0;margin:16px 0}
.cmp{border-top:2px solid var(--blue);margin:16px 0}.cmp div{padding:12px 0;border-bottom:1px solid var(--line);font-size:14px}.cmp .lab{font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:var(--blue);font-weight:700;margin-bottom:6px;padding:0;border:0}.cmp .big{font-family:"Source Serif 4",Georgia,serif;font-size:17px;line-height:1.3;padding:0;border:0}
.close{font-family:"Source Serif 4",Georgia,serif;font-size:18.5px;line-height:1.35;margin-top:22px;padding:12px 0 0 14px;border-left:3px solid var(--blue)}
.hint{font-size:13px;color:var(--muted)}.form{border-left:3px solid var(--blue);padding:2px 0 2px 14px;margin:12px 0}.form b{color:var(--blue)}
.note{position:absolute;top:8px;right:8px;background:#FFF4C2;border:1px solid #E6C84A;font-size:11px;padding:4px 7px;max-width:170px;color:#5B4A00}
</style>"""
STAPPEN = ['Opening','Uitzoomen','Geleerde','Afweging','Zelfs als','Mijn deel','Terug']
def band(i):
    rail = "".join(f'<span class="{"done" if k<i else "cur" if k==i else ""}">{k+1}</span>' for k in range(7))
    return f'<div class="band"><div class="brand">Nederland in Dialoog<small>Van nieuws naar principe naar eigen afweging</small></div><div class="rail">{rail}</div></div>'
def page(i, title, lede, body, back=True, nxt="Verder", off=False, note=""):
    return f'<!doctype html><html lang="nl"><head>{CSS}</head><body>{band(i)}{f"<div class=note>{e(note)}</div>" if note else ""}<div class="wrap"><div class="stepno">Stap {i+1} van 7 · {STAPPEN[i]}</div><h1>{title}</h1><p class="lede">{lede}</p>{body}</div><div class="bar">{"<span class=btn ghost>Terug</span>" if back else "<span></span>"}{f"<span class=\'btn{" off" if off else ""}\'>{nxt}</span>" if nxt else ""}</div></body></html>'

item = next(x for x in OP if "belastingplan" in x["titel"].lower())
P = PR["inkomen"]

def row(x, sel=False):
    return f'<div class="row{" sel" if sel else ""}"><div class="h"><span>{e(x["titel"])}</span><span class="chip {x["soort"]}">{x["soort"]}</span></div><div class="s">{e(x["samenvatting"][:150])}…</div></div>'

metingen = [x for x in OP if x["soort"]=="meting" and x["kandidaten"]][:2]
nieuws = [x for x in OP if x["soort"]!="meting" and x["kandidaten"] and x["datum"]==OP[0]["datum"]][:3]
geen = [x["titel"] for x in OP if x["kandidaten"]==[]][:4]
S1 = page(0,"Wat is er gebeurd?","Kies een onderwerp uit het nieuws. Het raamwerk begint bij het principe, niet bij het incident.",
  f'<div class="grp"><span>Metingen en rapporten</span><span>schoonste ingang</span></div>{"".join(row(x) for x in metingen)}'
  f'<div class="grp"><span>Nieuws van 25 oktober</span><span>incident of besluit</span></div>{"".join(row(x, x is item) for x in nieuws)}'
  f'<div class="grp"><span>Raakt geen van de elf principes ({len([x for x in OP if x["kandidaten"]==[]])})</span></div>{"".join(f"<div class=hint style=padding:5px/0>{e(g)}</div>" for g in geen)}',
  back=False, nxt="", note="Metingen eerst: dat is de schoonste trigger (werkdoc, B-modus). Incident krijgt wachttijd.")

k = item["kandidaten"][0]
S2 = page(1,"Welk principe raakt dit?","De koppeling is de meest politieke stap. Daarom staat bij elke suggestie de zin die haar draagt, en kies jij.",
  f'<div class="flat"><div class="h" style="font-family:\'Source Serif 4\',serif;font-size:17px;margin-bottom:3px">{e(item["titel"])} <span class="chip">besluit</span></div><div class="s">{e(item["samenvatting"][:230])}…</div></div>'
  f'<div class="row sel"><div class="h"><span>Inkomen</span><span class="chip ruw">ruw</span></div><div class="s">{e(P["titel"])}</div><div class="z">{e(k["zin"])}</div></div>'
  f'<div class="row"><div class="h"><span>Vangnet</span><span class="chip ruw">ruw</span></div><div class="s">{e(PR["vangnet"]["titel"])}</div><div class="z">Een belastingplan verschuift ook wie steun krijgt en wie betaalt: vangnet versus loont.</div></div>'
  f'<p class="hint" style="margin-top:14px">Geen van beide? Dan is dit geen principekwestie. Dat is een uitkomst.</p>',
  nxt="Naar het geleerde", note="App kiest nooit. Hoogstens 3 kandidaten, elk met dragende zin. 'Geen' is geldig.")

kiz = f'<div class="kiz"><div><b>Kans</b>{e(P["kans"])}</div><div><b>Inhoud</b>{e(P["inhoud"])}</div><div><b>Zodat</b>{e(P["zodat"])}</div></div>'
bel = "".join(f'<li><b>{i+1}. {e(b["titel"])}</b> {e(b["tekst"])}</li>' for i,b in enumerate(P["beloften"]))
def cls(s): s=s.lower(); return "f" if s.startswith("dichtbij") else "h" if s.startswith(("halverwege","omstreden")) else ""
score = "".join(f'<div><div class="b"><span class="dot {cls(r[list(r)[1]])}"></span>{e(r[list(r)[0]])} <span class="hint">· {e(r[list(r)[1]])}</span></div><div class="r">{e(r[list(r)[2]])}</div><div class="r">Richting: {e(r[list(r)[-1]])}</div></div>' for r in P["scorebord"])
S3 = page(2,"Inkomen <span class='chip ruw'>ruw</span>",e(P["titel"]),
  kiz+f'<div class="grp"><span>De beloften</span></div><ul class="bel">{bel}</ul><div class="grp"><span>Waar staan we nu</span><span>objectief · richting</span></div><div class="score">{score}</div>'
  f'<div class="grp"><span>Waar schoten we door</span></div><p style="font-size:14px">{e(P["doorgeschoten"])}</p><p class="hint">Geen kabinetten, geen partijen.</p>',
  nxt="Naar de afweging", off=True, note="Leesdrempel: knop pas actief als je onderaan bent geweest. Tijd tussen nieuws en oordeel is het product.")

S4 = page(3,"Waar komt het vandaan?","Je kunt niet alles hebben. Drie eerlijke antwoorden, geen vierde.",
  '<label>Welke belofte van Inkomen raakt dit?</label><div class="field">4. Meer bijdragen loont</div><div class="grp"><span>Het antwoord</span></div>'
  '<div class="opt"><div class="h">Binnen het principe</div><div class="s">Een ander instrument van Inkomen wordt kleiner. Het HOE verandert, de rekening niet.</div></div>'
  '<div class="opt sel"><div class="h">Bij een ander principe</div><div class="s">Het geld komt van een ander gedeeld doel. Dat is het zelfs-als.</div></div>'
  '<div class="opt"><div class="h">Meer belasting</div><div class="s">De contributie voor de elf principes gaat omhoog. Zeg erbij hoeveel en bij wie.</div></div>'
  '<label>Welk ander principe krijgt het voor zijn kiezen?</label><div class="opt sel"><div class="h">Vangnet <span class="chip">in de startset</span></div><div class="s">vangnet versus loont (inkomen)</div></div><div class="opt"><div class="h">Zorg</div><div class="s">Zorg is er als je haar nodig hebt, en je gaat er niet aan failliet</div></div><div class="opt"><div class="h">Wonen</div><div class="s">Er is een passende woning voor iedereen die hier woont</div></div>',
  nxt="Naar de zin", note="'Binnen het principe' alleen kiesbaar als je noemt wat kleiner wordt. En-en is verboden.")

S5 = page(4,"Zeg het hardop","Vaste grammatica, zodat het pijn doet waar het hoort. Alleen de waarom-regel is van jou.",
  '<div class="sentence">Ik wil dat meer bijdragen loont, zelfs als het ten koste gaat van vangnet (“Als het tegenzit, val je niet door de bodem”), voor de komende tien jaar.</div>'
  '<label>Tijdshorizon</label><div class="field">de komende tien jaar ▾</div><label>Waarom (één regel)</label><div class="field">Omdat een voltijdbaan op zichzelf genoeg moet zijn.</div>',
  nxt="Naar mijn deel", note="Open: belofte-titels stikken slecht. Per belofte een zelfs-als-vorm in het werkdoc.")

S6 = page(5,"Wat doe ik zelf?","Niet alles is overheid. Elk principe heeft een regel over wat wij zelf doen.",
  f'<div class="form"><b>Wat wij zelf doen</b> {e(P["watwijzelf"])}</div><label>Jouw deel hierin</label><div class="field" style="min-height:70px">Ik accepteer dat mijn toeslag daalt als mijn loon stijgt, en bouw zelf een buffer op.</div>',
  nxt="Rond de cirkel", note="Laag 4 (WIE) is niet uitgewerkt; v1 gebruikt alleen de 'wat wij zelf doen'-regel. Twee actoren, geen drie.")

S7 = page(6,"De cirkel is rond","Links wat het nieuws zei. Rechts wat jij nu zegt, en bij stap 1 niet zei.",
  f'<div class="cmp"><div><div class="lab">Het nieuws</div><div class="big">{e(item["titel"])}</div></div><div><div class="lab">Jij</div><div class="big">Ik wil dat meer bijdragen loont, zelfs als het ten koste gaat van vangnet, voor de komende tien jaar.</div><p class="hint" style="margin:6px 0 0">Omdat een voltijdbaan op zichzelf genoeg moet zijn. · Mijn deel: ik accepteer dat mijn toeslag daalt. · Inkomen</p></div></div>'
  '<div style="display:flex;gap:10px;justify-content:space-between"><span class="btn ghost">Kopieer tekst</span><span class="btn">Nieuw onderwerp</span></div>'
  '<div class="close">Ga hiermee het gesprek aan met de partij waar jij je thuis voelt. Die koppeling maken wij niet.</div>',
  nxt="", back=False, note="Record (principe, botsend principe, zin, betaler, horizon) is het signaal voor later. Nu alleen lokaal.")

os.makedirs(os.path.join(root,"proto"), exist_ok=True)
for i,s in enumerate([S1,S2,S3,S4,S5,S6,S7],1):
    open(os.path.join(root,f"proto/s{i}.html"),"w",encoding="utf-8").write(s)
print("7 schermen in proto/")
