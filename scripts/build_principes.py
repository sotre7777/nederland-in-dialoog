"""Werkdocument (markdown) -> data/principes.json

Usage: python3 -I scripts/build_principes.py content/werkdocument-YYYY-MM-DD.md data/principes.json

Leest het werkdocument via parse_werkdoc.py en legt per principe neer wat de app nodig heeft:
formulering (laag 1), beloften en stand (laag 3), afruilen (laag 2, als zinnen),
en de "wat wij zelf doen"-regel (laag 4, voorlopig). Alles is tekst uit het werkdocument;
dit script oordeelt niet.
"""
import json, re, subprocess, sys, tempfile, os

src, dst = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False).name
subprocess.run([sys.executable, "-I", os.path.join(here, "parse_werkdoc.py"), src, tmp],
               check=True, stdout=subprocess.DEVNULL)
D = json.load(open(tmp, encoding="utf-8"))
os.unlink(tmp)

SLUG = lambda k: re.sub(r"[^a-z0-9]+", "-", k.lower())

def table_rows(md):
    """All markdown tables in md -> list of (headers, rows)."""
    out, headers, rows = [], None, []
    for ln in md.split("\n"):
        if ln.startswith("|"):
            cells = [c.strip() for c in ln.strip().strip("|").split(" | ")]
            if headers is None:
                headers = cells
            elif set(cells[0]) <= set("-: "):
                continue
            else:
                rows.append(cells)
        else:
            if headers is not None:
                out.append((headers, rows)); headers, rows = None, []
    if headers is not None:
        out.append((headers, rows))
    return out

def field(text, label):
    """'Label: ...' tot aan het volgende label of einde."""
    m = re.search(label + r"\s*:\s*(.*?)(?=(?:\s(?:Kans|Inhoud|Zodat|Wat wij zelf doen(?: \([^)]*\))?|Cijfers|Afruilen|Prior art|Model|Ontbrandpunt|Open|Voorzet|Erwins basis)\s*:)|$)", text, re.S)
    return m.group(1).strip() if m else ""

principes = []
for p in D["principles"]:
    f = p["formulering"]
    sub = p["sub"]

    # beloften uit "Het principe, uiteengelegd"
    beloften = []
    rand = ""
    for ln in sub.get("Het principe, uiteengelegd", "").split("\n"):
        m = re.match(r"^\d+\.\s+\*\*(.+?)\*\*\s*:?\s*(.*)$", ln)
        if m:
            beloften.append({"titel": m.group(1).rstrip(":"), "tekst": m.group(2).strip()})
        elif ln.lower().startswith("randvoorwaarde") or ln.lower().startswith("en één randvoorwaarde"):
            rand = ln.strip()

    # geleerde per belofte: blokken "**Belofte n: ...**" met tabel en Stand-regel
    gel_md = sub.get("Wat hebben we eerder gedaan en geleerd", "")
    blokken = re.split(r"\n(?=\*\*Belofte \d)", "\n" + gel_md)
    geleerde = []
    for b in blokken:
        h = re.match(r"\*\*Belofte (\d+):\s*(.+?)\*\*", b.strip())
        if not h:
            continue
        tbl = table_rows(b)
        stand = re.search(r"\*\*Stand:\*\*\s*(.*)", b)
        geleerde.append({
            "nr": int(h.group(1)), "belofte": h.group(2).strip(),
            "maatregelen": [dict(zip(["wat", "offer", "waarvoor", "opleverde"], r)) for r in (tbl[0][1] if tbl else [])],
            "stand": stand.group(1).strip() if stand else "",
        })
    door = re.search(r"\*\*Waar schoten we door:\*\*\s*(.*)", gel_md)

    # scorebord
    tbls = table_rows(sub.get("Waar staan we nu", ""))
    scorebord = []
    if tbls:
        hdr, rows = tbls[0]
        for r in rows:
            scorebord.append(dict(zip(hdr, r)))

    principes.append({
        "id": SLUG(p["key"]),
        "naam": p["key"],
        "titel": p["tagline"],
        "ruw": p["raw"],
        "nko": p.get("nko", ""),
        "probleem": p.get("probleem", ""),
        "sterkpunt": p.get("sterk", ""),
        "formulering": f,
        "kans": field(f, "Kans"),
        "inhoud": field(f, "Inhoud"),
        "zodat": field(f, "Zodat"),
        "watwijzelf": field(f, r"Wat wij zelf doen(?: \([^)]*\))?"),
        "cijfers": field(f, "Cijfers"),
        "afruilen": [a.strip() for a in re.split(r";\s*", field(f, "Afruilen")) if a.strip()],
        "beloften": beloften,
        "randvoorwaarde": rand,
        "geleerde": geleerde,
        "doorgeschoten": door.group(1).strip() if door else "",
        "scorebord": scorebord,
        "zelfsals_geschiedenis": sub.get("Wat de geschiedenis zegt over het zelfs-als", ""),
        "bronnen": sub.get("Bronnen", ""),
    })

json.dump({"bron": os.path.basename(src), "principes": principes},
          open(dst, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for p in principes:
    print(f"{p['naam']:12} beloften={len(p['beloften'])} geleerde={len(p['geleerde'])} score={len(p['scorebord'])} afruilen={len(p['afruilen'])} kans={'ja' if p['kans'] else 'NEE'} zelf={'ja' if p['watwijzelf'] else 'NEE'}")
