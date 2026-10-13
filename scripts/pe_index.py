#!/usr/bin/env python3
"""Fetch the metadata index (type, number, publication date, title) of numbered norms from
the Congreso's "Archivo Digital de la Legislación del Perú" (leyes.congreso.gob.pe) by
querying number ranges of 20 (the result grid shows 20 rows per page).

Caches each result page under _raw/pe/index/ and writes a TSV _raw/pe/index-<tipo>.tsv.
Only the HTML result pages are requested (robots.txt asks robots not to fetch the PDFs).
"""
import csv
import os
import sys
import time

import requests
from bs4 import BeautifulSoup

RAW = os.environ.get("RAW", "/Users/magicaltux/projects/lawcodex/_raw/pe")
UA = "LawCodex/1.0 (+https://github.com/LawCodex)"
BASE = ("https://www.leyes.congreso.gob.pe/LeyNume_1p.aspx?xEstado=2&xTipoNorma={t}&xTipoBusqueda=4"
        "&xFechaI=&xFechaF=&xTexto=&xOrden=0&xNormaI={a}&xNormaF={b}")
TYPES = {"0": ("leyes", 1, 33000), "3": ("decretos-legislativos", 1, 1800)}
STEP = 20

s = requests.Session()
s.headers["User-Agent"] = UA


def get(url, path):
    if os.path.exists(path) and os.path.getsize(path) > 1000:
        return open(path, encoding="utf-8").read()
    for k in range(5):
        try:
            r = s.get(url, timeout=(20, 120))
            if r.status_code == 200 and "</html>" in r.text.lower():
                open(path, "w", encoding="utf-8").write(r.text)
                time.sleep(1.0)
                return r.text
        except requests.RequestException as e:
            print("retry", url, e, file=sys.stderr)
        time.sleep(5 * (k + 1))
    raise RuntimeError(url)


def parse(html):
    soup = BeautifulSoup(html, "lxml")
    rows = []
    for a in soup.select("a[id$=LinkNumero]"):
        tr = a.find_parent("tr")
        tds = [td.get_text(" ", strip=True) for td in tr.find_all("td")]
        if len(tds) >= 4:
            rows.append(tds[:5] + [""] * (5 - len(tds[:5])))
    return rows


def fetch_range(t, d, a, b):
    """Rows for numbers a..b; a full grid page (20 rows) may be truncated, so split."""
    html = get(BASE.format(t=t, a=a, b=b), os.path.join(d, f"{a:05d}.html" if b - a == STEP - 1 else f"{a:05d}-{b:05d}.html"))
    rows = parse(html)
    if len(rows) < STEP:
        return rows
    if a == b:
        print("WARN >=20 rows for single number", t, a, file=sys.stderr)
        return rows
    step = max(1, (b - a + 1) // 4)
    out = []
    for x in range(a, b + 1, step):
        out += fetch_range(t, d, x, min(b, x + step - 1))
    return out


def main():
    for t, (name, lo, hi) in TYPES.items():
        d = os.path.join(RAW, "index", name)
        os.makedirs(d, exist_ok=True)
        out = []
        empty_run = 0
        for a in range(lo, hi + 1, STEP):
            rows = fetch_range(t, d, a, a + STEP - 1)
            out += rows
            empty_run = 0 if rows else empty_run + 1
            if a > hi - 2000 and empty_run > 40:
                break
        with open(os.path.join(RAW, f"index-{name}.tsv"), "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f, delimiter="\t")
            for r in out:
                w.writerow(r)
        print(name, len(out))


if __name__ == "__main__":
    main()
