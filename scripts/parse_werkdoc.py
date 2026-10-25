import re, json, sys

src = open(sys.argv[1], encoding="utf-8").read()
lines = src.split("\n")

# ---- split top-level (##) sections, keeping ### / #### inside ----
sections = {}
order = []
cur = None
buf = []
for ln in lines:
    if ln.startswith("## "):
        if cur is not None:
            sections[cur] = "\n".join(buf).strip()
        cur = ln[3:].strip()
        order.append(cur)
        buf = []
    elif cur is not None:
        buf.append(ln)
sections[cur] = "\n".join(buf).strip()

def take(name):
    for k in order:
        if k.startswith(name):
            return sections[k]
    raise KeyError(name)

# ---- intro / header (before first ##) ----
intro = "\n".join(lines[:lines.index("## Het idee")]).strip()

# ---- principles: the per-principle ### blocks in "Per principe" ----
per = take("Per principe")
per_intro, *blocks = re.split(r"\n(?=### )", per)
principles = []
for b in blocks:
    head, _, body = b.partition("\n")
    title = head[4:].strip()
    key, _, tagline = title.partition(":")
    key = key.strip(); tagline = tagline.strip()
    body = body.strip()
    raw = body.startswith("RUW")
    if raw:
        body = body.split("\n", 1)[1].strip()
    # split #### subsections
    subs = {}
    pre, *parts = re.split(r"\n(?=#### )", "\n" + body)
    for p in parts:
        h, _, t = p.partition("\n")
        subs[h[5:].strip()] = t.strip()
    principles.append({"key": key, "tagline": tagline, "raw": raw,
                       "pre": pre.strip(), "sub": subs})

# the "tweede ronde" note is the last #### of the last principle; pull it out
last = principles[-1]
note = last["sub"].pop("Wat in een tweede ronde beter moet (alle tien)", "")

# ---- grondstof table ----
gs = take("Grondstof")
gs_intro = gs.split("\n| Hoofdprobleem")[0].strip()
rows = []
for ln in gs.split("\n"):
    if ln.startswith("| ") and not ln.startswith("| Hoofdprobleem") and not ln.startswith("| ---"):
        cells = [c.strip() for c in ln.strip().strip("|").split(" | ")]
        if len(cells) == 4:
            rows.append(cells)
gs_after = gs.split("Wat de tabel laat zien:")[1].strip() if "Wat de tabel laat zien:" in gs else ""

# map grondstof rows to principle keys
rowmap = {
    "Minderheden": ["Immigratie"], "Inkomen": ["Inkomen"], "Wonen": ["Wonen"],
    "Gezondheidszorg": ["Zorg"], "Milieu": ["Leefomgeving"], "Criminaliteit": ["Veiligheid"],
    "Onderwijs": ["Onderwijs"], "Sociale zekerheid": ["Pensioen", "Vangnet"],
    "Defensie": ["Defensie"], "Bevolking": ["Bevolking"],
}
dropped = []
for cells in rows:
    hit = None
    for k, v in rowmap.items():
        if cells[0].startswith(k):
            hit = v
    if hit is None:
        dropped.append({"nko": cells[0], "probleem": cells[1], "sterk": cells[2], "oordeel": cells[3]})
        continue
    for pk in hit:
        p = next(x for x in principles if x["key"] == pk)
        p["nko"] = cells[0]; p["probleem"] = cells[1]; p["sterk"] = cells[2]
        f = cells[3]
        if pk in ("Pensioen", "Vangnet"):
            a, _, b = f.partition("**Vangnet**")
            tail = ""
            m = re.search(r"Wat wij zelf doen \(pensioen\):.*$", b)
            if m:
                tail = " " + m.group(0); b = b[:m.start()].rstrip()
            f = (a.strip() + tail) if pk == "Pensioen" else ("**Vangnet**" + b)
        f = re.sub(r"^RUW\.( Twee principes in deze rij\.)?\s*", "", f)
        f = re.sub(r"\*\*Vangnet\*\* \(RUW\)\. ", "", f)
        p["formulering"] = f

# short, positive one-liner per principle (from the ### title)
out = {
    "intro": intro,
    "idee": take("Het idee"),
    "vaststaat": take("Wat vaststaat"),
    "lagen": take("De lagen"),
    "nee": take("Waar we NEE"),
    "bestaat": take("Wat al bestaat"),
    "bronnen": take("Bronnen voor de lijst"),
    "getallen": take("Principes met getallen"),
    "modi": take("Toepassing"),
    "afspraken": take("Twee afspraken"),
    "pad": take("Het pad"),
    "grondstof_intro": gs_intro,
    "grondstof_after": gs_after,
    "dropped": dropped,
    "per_intro": per_intro.strip(),
    "tweede_ronde": note,
    "open": take("Open vragen"),
    "principles": principles,
}
json.dump(out, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(principles), "principles;", [p["key"] for p in principles])
print("dropped:", [d["nko"] for d in dropped])
print("missing formulering:", [p["key"] for p in principles if "formulering" not in p])
print("sub keys:", {p["key"]: list(p["sub"]) for p in principles[:2]})
