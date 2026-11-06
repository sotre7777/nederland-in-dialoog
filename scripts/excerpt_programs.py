"""Haalt uit pdftotext-uitvoer (-layout, met \f paginascheiding) per programma de passages
die doeltaal of afweegtaal bevatten, gegroepeerd per principe, met paginanummer.

Usage: python3 -I excerpt_programs.py <txt-map> <uitvoer-map>
"""
import os, re, sys, glob

src, dst = sys.argv[1], sys.argv[2]
os.makedirs(dst, exist_ok=True)

P = {
 "Inkomen": r"werken (moet|gaat|blijft) (meer )?lonen|werken loont|bestaanszekerheid|minimumloon|koopkracht|armoede|rondkomen|inkomensverschil|loonkloof|toeslag",
 "Vangnet": r"vangnet|sociale zekerheid|bijstand|uitkering|fraude|wie (echt )?niet kan|niet door de bodem|bodem",
 "Pensioen": r"\bAOW|pensioen|oude dag|zware beroep|gepensioneerd",
 "Wonen": r"betaalbare? won|woningnood|woningtekort|wooncrisis|volkshuisvesting|recht op wonen|sociale huur|huurder|starters? ",
 "Zorg": r"\bzorg\b.{0,60}(toegankelijk|betaalbaar|voor iedereen|dichtbij)|(toegankelijk|betaalbaar).{0,40}\bzorg|eigen risico|wachtlijst|ggz|ouderenzorg|verpleeg",
 "Onderwijs": r"onderwijs|basisvaardigh|leraar|lerarentekort|kansengelijkheid|school|leven lang (leren|ontwikkelen)",
 "Veiligheid": r"veilig(heid)?\b.{0,40}(straat|buurt|thuis|online|wijk)|(straat|buurt|thuis|online).{0,40}veilig|criminaliteit|politie|ondermijning|rechtsstaat",
 "Migratie en bevolking": r"migratie|migrant|asiel|vluchteling|integratie|inburgering|bevolkingsgroei|bevolkingsomvang|hoeveel (mensen|inwoners)|vergrijzing|demografi|nederland is vol",
 "Leefomgeving": r"klimaat|stikstof|natuur\b|biodiversiteit|leefbaar|doorgeven aan|volgende generatie|rentmeester|schone? (lucht|energie|land)|landbouw|boer",
 "Defensie": r"defensie|krijgsmacht|navo\b|nato\b|verdedig|internationale rechtsorde|oekra",
}
TRADE = r"zelfs als|ook als|gaat boven|gaan boven|boven (de |het |onze |alle )?\w+ (van|voor)|ten koste van|koste wat (het )?kost|belangrijker dan|prioriteit boven|voorrang (op|boven)|liever .{0,40} dan|niet ten koste|in plaats van .{0,30}(bezuinig|korten)"
GOAL = r"\b(we |wij |ieder|iedereen|niemand|elke? |alle )\w*.{0,80}(moet|moeten|willen|wil|zorgen|garanderen|recht op|kan|kunnen|verdient|hoort|horen)|\b(moet|moeten) (weer |altijd |ook )?(kunnen|lonen|zijn)|is een recht|basisrecht|grondrecht|kernwaarde|uitgangspunt|principe|waar we voor staan"

def paras(text):
    pages = text.split("\f")
    for pno, page in enumerate(pages, 1):
        t = re.sub(r"-\n(?=[a-z])", "", page)
        t = re.sub(r"[ \t]+", " ", t.replace("\n", " ")).strip()
        # zinnen: einde op . ! ? ; of op bullet/koptekens
        sents = [x.strip() for x in re.split(r"(?<=[.!?;])\s+(?=[A-Z\u00c0-\u00dd\u2022\-\u2013\u2014\d])|\s[\u2022\u25cf\u25a0\-\u2013\u2014]\s", t) if x and len(x.strip()) > 20]
        for i, sn in enumerate(sents):
            win = sn if len(sn) > 160 or i + 1 >= len(sents) else sn + " " + sents[i + 1]
            win = win[:700]
            if 40 <= len(win):
                yield pno, win

tr = re.compile(TRADE, re.I); gl = re.compile(GOAL, re.I)
PR = {k: re.compile(v, re.I) for k, v in P.items()}

for f in sorted(glob.glob(os.path.join(src, "*.txt"))):
    name = os.path.basename(f)[:-4]
    text = open(f, encoding="utf-8", errors="replace").read()
    out = {k: [] for k in P}; trades = []
    seen = set()
    for pno, t in paras(text):
        key = t[:80]
        if key in seen: continue
        seen.add(key)
        is_tr = bool(tr.search(t)); is_goal = bool(gl.search(t))
        hits = [k for k, rx in PR.items() if rx.search(t)]
        if is_tr and hits:
            trades.append((pno, hits, t))
        if hits and (is_goal or is_tr):
            for k in hits[:2]:
                if len(out[k]) < 35:
                    out[k].append((pno, t))
    with open(os.path.join(dst, name + ".md"), "w", encoding="utf-8") as w:
        w.write(f"# {name}\n\nBron: pdftotext van het DNPP-PDF; p. = paginanummer in de PDF (kan 1 afwijken van gedrukt nummer).\n\n")
        w.write("## Afweegzinnen (zelfs als / ook als / gaat boven / ten koste van / belangrijker dan)\n\n")
        for pno, hits, t in trades[:60]:
            w.write(f"- p.{pno} [{', '.join(hits)}] {t}\n")
        for k in P:
            w.write(f"\n## {k}\n\n")
            for pno, t in out[k]:
                w.write(f"- p.{pno} {t}\n")
    n = sum(len(v) for v in out.values())
    print(f"{name}: {n} passages, {len(trades)} afweegzinnen")
