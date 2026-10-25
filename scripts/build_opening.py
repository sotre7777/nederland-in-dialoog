"""nieuwsoverzicht-archief + classificatie.json -> data/opening.json

Usage: python3 -I scripts/build_opening.py <pad naar nieuwsoverzicht/archief> data/classificatie.json data/opening.json [dagen=3]

Leest de laatste N dagoverzichten (markdown, vast format uit ROUTINE.md van sotre7777/nieuwsoverzicht),
haalt de onderwerpen en de "Recent gepubliceerd"-regels eruit, ontdubbelt op titel en koppelt
elk item aan de kandidaat-principes uit classificatie.json. Items zonder match in de classificatie
krijgen status "ongeclassificeerd" en blijven zichtbaar: dat is werk voor het taalmodel, geen fout.
"""
import json, os, re, sys, glob

archief, cls_path, dst = sys.argv[1], sys.argv[2], sys.argv[3]
dagen = int(sys.argv[4]) if len(sys.argv) > 4 else 3
C = json.load(open(cls_path, encoding="utf-8"))["items"]

files = sorted(glob.glob(os.path.join(archief, "nieuwsoverzicht-*.md")))[-dagen:]

def link_of(cell):
    m = re.search(r"\((https?://[^)]+)\)", cell)
    return m.group(1) if m else ""

def classify(title):
    for c in C:
        if c["sleutel"].lower() in title.lower():
            return c
    return None

items = {}
for f in files:
    datum = re.search(r"(\d{4}-\d{2}-\d{2})", f).group(1)
    t = open(f, encoding="utf-8").read()
    # onderwerpen
    for m in re.finditer(r"^### (\d+)\. (.+?)\n\*\*Samenvatting:\*\* (.+?)\n\*\*Aandacht:\*\* (.+?)\n(.*?)(?=\n\*\*Kans voor eigen item|\n---|\n### )", t, re.M | re.S):
        titel, samen, aandacht, tabel = m.group(2).strip(), m.group(3).strip(), m.group(4).strip(), m.group(5)
        links = []
        for ln in tabel.split("\n"):
            if ln.startswith("| ") and not ln.startswith("| Medium") and not ln.startswith("|---"):
                c = [x.strip() for x in ln.strip().strip("|").split("|")]
                if len(c) >= 4 and link_of(c[3]):
                    links.append({"medium": c[0], "invalshoek": c[2], "url": link_of(c[3])})
        key = re.sub(r"[^a-z0-9]+", "-", titel.lower()).strip("-")[:40]
        cl = classify(titel)
        prev = items.get(key)
        items[key] = {
            "id": key, "titel": titel, "samenvatting": samen, "aandacht": aandacht,
            "datum": datum, "eerst": prev["eerst"] if prev else datum,
            "bron": "onderwerp", "soort": cl["soort"] if cl else "incident",
            "kandidaten": cl["kandidaten"] if cl else None,
            "links": links[:4],
        }
    # recent gepubliceerd (metingen)
    if "## Recent gepubliceerd" in t:
        sec = t.split("## Recent gepubliceerd")[1].split("## Agenda")[0]
        for ln in sec.split("\n"):
            if ln.startswith("| ") and not ln.startswith("| Datum") and not ln.startswith("|---"):
                c = [x.strip() for x in ln.strip().strip("|").split("|")]
                if len(c) < 5:
                    continue
                titel = re.sub(r"\s*\(.*?\)\s*$", "", c[2])
                key = re.sub(r"[^a-z0-9]+", "-", titel.lower()).strip("-")[:40]
                if key in items:
                    continue
                cl = classify(titel)
                items[key] = {
                    "id": key, "titel": titel, "samenvatting": c[3], "aandacht": c[1],
                    "datum": datum, "eerst": datum, "publicatiedatum": c[0],
                    "bron": "publicatie", "soort": cl["soort"] if cl else "meting",
                    "kandidaten": cl["kandidaten"] if cl else None,
                    "links": [{"medium": c[1], "invalshoek": "", "url": link_of(c[4])}] if link_of(c[4]) else [],
                }

out = sorted(items.values(), key=lambda x: (x["datum"], x["bron"] != "onderwerp"), reverse=True)
json.dump({"gegenereerd_uit": [os.path.basename(f) for f in files], "items": out},
          open(dst, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
n_match = sum(1 for x in out if x["kandidaten"])
n_none = sum(1 for x in out if x["kandidaten"] == [])
n_unk = sum(1 for x in out if x["kandidaten"] is None)
print(f"{len(out)} items: {n_match} met principe, {n_none} geen principe, {n_unk} ongeclassificeerd")
for x in out:
    if x["kandidaten"] is None:
        print("  ongeclassificeerd:", x["titel"][:80])
