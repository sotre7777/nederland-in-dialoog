"""Vult app/template.html met de drie datasets en schrijft app/index.html.
Usage: python3 -I scripts/build_app.py
"""
import os
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rd = lambda p: open(os.path.join(root, p), encoding="utf-8").read()
safe = lambda s: s.replace("</", "<\\/")
t = rd("app/template.html")
t = t.replace("__PRINCIPES__", safe(rd("data/principes.json")))
t = t.replace("__AFRUILEN__", safe(rd("data/afruilen.json")))
t = t.replace("__OPENING__", safe(rd("data/opening.json")))
out = os.path.join(root, "app/index.html")
open(out, "w", encoding="utf-8").write(t)
print(out, len(t), "bytes")
