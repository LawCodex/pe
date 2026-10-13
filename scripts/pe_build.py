#!/usr/bin/env python3
"""Download the official editions (Ediciones Oficiales) published by the Ministerio de
Justicia y Derechos Humanos (MINJUS) on gob.pe and convert the normative part of each
PDF to Markdown. Also renders the Congreso norm index (see pe_index.py).

Usage: python pe_build.py [--index-only]
"""
import csv
import os
import re
import sys
import time
from datetime import date

import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pe_pdfmd as P  # noqa: E402

RAW = os.environ.get("RAW", "/Users/magicaltux/projects/lawcodex/_raw/pe")
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = "LawCodex/1.0 (+https://github.com/LawCodex)"
TODAY = date.today().isoformat()
GOB = "https://www.gob.pe/institucion/minjus/informes-publicaciones/"

# (pdf key, pdf url, publication page, [documents]) ; each document:
# (out path, title, identifier, type, date, last_amended, first page, end page (exclusive), drop patterns)
EDITIONS = [
    ("constitucion", "https://cdn.www.gob.pe/uploads/document/file/9139522/7498785-constitucion-politica_2025-final-dic-2025.pdf",
     "7498785-vigesima-primera-edicion-oficial-de-la-constitucion-politica-del-peru-bolsillo-actualizada-al-05-de-diciembre-de-2025",
     [("constitucion/constitucion-politica-del-peru-1993.md", "Constitución Política del Perú", "Constitución de 1993",
       "constitution", "1993-12-29", "2025-12-05", 21, 181, [r"CONSTITUCIÓN POLÍTICA DEL PERÚ"])]),
    ("cpconst", "https://cdn.www.gob.pe/uploads/document/file/5632117/4989147-cpcp-2023.pdf",
     "4989147-constitucion-politica-del-peru-y-nuevo-codigo-procesal-constitucional-actualizada-al-19-de-julio-de-2023",
     [("codigos/nuevo-codigo-procesal-constitucional-ley-31307.md", "Nuevo Código Procesal Constitucional", "Ley N° 31307",
       "code", "2021-07-23", "2023-07-19", 129, 185, [r"SEGUNDA PARTE\s+NUEVO CÓDIGO PROCESAL CONSTITUCIONAL - LEY N° 31307"]),
      ("leyes/ley-28301-ley-organica-del-tribunal-constitucional.md", "Ley Orgánica del Tribunal Constitucional", "Ley N° 28301",
       "act", "2004-07-23", "2023-07-19", 187, 201, [r"TERCERA PARTE\s+LEY ORGÁNICA DEL TRIBUNAL CONSTITUCIONAL - LEY N° 28301"])]),
    ("cpp", "https://cdn.www.gob.pe/uploads/document/file/7451652/6346160-codigo-procesal-penal-decreto-legislativo-final.pdf",
     "6346160-codigo-procesal-penal-octava-edicion-oficial-actualizada-a-noviembre-de-2024",
     [("codigos/codigo-procesal-penal-decreto-legislativo-957.md", "Código Procesal Penal", "Decreto Legislativo N° 957",
       "code", "2004-07-29", "2024-11", 21, 387, [r"CÓDIGO PROCESAL PENAL - DECRETO LEGISLATIVO Nº 957"])]),
    ("consumidor", "https://cdn.www.gob.pe/uploads/document/file/1837776/C%C3%B3digo%20Protecci%C3%B3n%20Consumidor%202020.pdf",
     "1877837-codigo-de-proteccion-y-defensa-del-consumidor-y-normas-complementarias-tercera-edicion-oficial-actualizada-al-27-de-noviembre-de-2020",
     [("codigos/codigo-de-proteccion-y-defensa-del-consumidor-ley-29571.md", "Código de Protección y Defensa del Consumidor",
       "Ley N° 29571", "code", "2010-09-02", "2020-11-27", 58, 162,
       [r"SEGUNDA PARTE", r"CÓDIGO DE PROTECCIÓN Y DEFENSA DEL CONSUMIDOR LEY Nº 29571"])]),
    ("8441836", "https://cdn.www.gob.pe/uploads/document/file/10399631/8441836-tuo-ley-27444-ley-procedimiento-administrativo-general-julio-2026-ok.pdf",
     "8441836-primera-edicion-oficial-del-texto-unico-ordenado-de-la-ley-n-27444-ley-del-procedimiento-administrativo-general-aprobado-por-el-decreto-supremo-n-006-2026-jus-actualizada-al-8-07-2026",
     [("leyes/tuo-ley-27444-ley-del-procedimiento-administrativo-general.md",
       "Texto Único Ordenado de la Ley N° 27444 – Ley del Procedimiento Administrativo General",
       "Decreto Supremo N° 006-2026-JUS", "act", "2026", "2026-07-08", 30, 236,
       [r"TEXTO ÚNICO ORDENADO DE LA LEY Nº 27444", r"LEY DEL PROCEDIMIENTO ADMINISTRATIVO GENERAL", r"DECRETO SUPREMO Nº 006-2026-JUS\s*\d*"])]),
    ("5060551", "https://cdn.www.gob.pe/uploads/document/file/5700008/5060551-codigo-civil-minjus-bcp_n-3.pdf",
     "5060551-codigo-civil-decreto-legislativo-n-295-decimo-cuarta-edicion-oficial-actualizado-al-1-de-agosto-de-2014",
     [("codigos/codigo-civil-decreto-legislativo-295.md", "Código Civil", "Decreto Legislativo N° 295", "code",
       "1984-07-25", "2014-08-01", 50, 474, [r"CÓDIGO CIVIL", r"DECRETO LEGISLATIVO Nº 295"])]),
    ("1466644", "https://cdn.www.gob.pe/uploads/document/file/1534182/C%C3%B3digo-de-Responsabilidad-Penal-de-Adolescentes-.pdf",
     "1466644-codigo-de-responsabilidad-penal-de-adolescentes-y-su-reglamento-primera-edicion-oficial-actualizado-al-30-de-agosto-de-2018",
     [("codigos/codigo-de-responsabilidad-penal-de-adolescentes-decreto-legislativo-1348.md",
       "Código de Responsabilidad Penal de Adolescentes", "Decreto Legislativo N° 1348", "code", "2017-01-07", "2018-08-30",
       56, 172, [r"DECRETO LEGISLATIVO Nº 1348"])]),
    ("1466669", "https://cdn.www.gob.pe/uploads/document/file/1534208/DGDOJ-Ley-Org%C3%A1nica-Poder-Judicial-y-Ministerio-P%C3%BAblico.pdf",
     "1466669-texto-unico-ordenado-de-la-ley-organica-del-poder-judicial-y-ley-organica-del-ministerio-publico-tercera-edicion-oficial",
     [("leyes/tuo-ley-organica-del-poder-judicial-ds-017-93-jus.md", "Texto Único Ordenado de la Ley Orgánica del Poder Judicial",
       "Decreto Supremo N° 017-93-JUS", "act", "1993-06-02", None, 27, 142, []),
      ("leyes/ley-organica-del-ministerio-publico-decreto-legislativo-52.md", "Ley Orgánica del Ministerio Público",
       "Decreto Legislativo N° 52", "act", "1981-03-18", None, 142, 245, [])]),
    ("1466646", "https://cdn.www.gob.pe/uploads/document/file/1534186/1-Ley-del-Servicio-Civil-sus-Reglamentos-y-precedentes-administrativos-de-observancia-obligatoria.pdf",
     "1466646-ley-del-servicio-civil-sus-reglamentos-y-precedentes-administrativos-de-observancia-obligatoria-primera-edicion-oficial-actualizado-al-7-de-diciembre-de-2017",
     [("leyes/ley-30057-ley-del-servicio-civil.md", "Ley del Servicio Civil", "Ley N° 30057", "act", "2013-07-04", "2017-12-07", 30, 94, [])]),
    ("l26300", "https://cdn.www.gob.pe/uploads/document/file/9120472/7485314-primera-edicion-oficial-de-la-ley-n-26300.pdf",
     "7485314-primera-edicion-oficial-de-la-ley-n-26300-ley-de-los-derechos-de-participacion-y-control-ciudadanos-actualizada-al-4-de-diciembre-de-2025",
     [("leyes/ley-26300-ley-de-los-derechos-de-participacion-y-control-ciudadanos.md",
       "Ley de los Derechos de Participación y Control Ciudadanos", "Ley N° 26300", "act", "1994-05-03", "2025-12-04", 18, 32, [])]),
    ("l30220", "https://cdn.www.gob.pe/uploads/document/file/5639775/4994649-29-12-23_libroleyuniversitaria-final.pdf",
     "4994649-primera-edicion-oficial-de-la-ley-universitaria-ley-n-30220-actualizada-al-28-de-diciembre-de-2023",
     [("leyes/ley-30220-ley-universitaria.md", "Ley Universitaria", "Ley N° 30220", "act", "2014-07-09", "2023-12-28", 14, 96,
       [r"LEY UNIVERSITARIA - LEY Nº 30220"])]),
]

# documents whose first footnote marker is glued to a number (auto-detection fails)
FN_START = {"leyes/ley-30220-ley-universitaria.md": 1, "codigos/codigo-procesal-penal-decreto-legislativo-957.md": 1,
            "leyes/ley-26300-ley-de-los-derechos-de-participacion-y-control-ciudadanos.md": 1,
            "codigos/codigo-de-proteccion-y-defensa-del-consumidor-ley-29571.md": 1}

s = requests.Session()
s.headers["User-Agent"] = UA


def fetch_pdf(key, url):
    d = os.path.join(RAW, "pdf")
    os.makedirs(d, exist_ok=True)
    path = os.path.join(d, key + ".pdf")
    for k in range(4):
        if os.path.exists(path) and P.pdf_ok(path):
            return path
        r = s.get(url, timeout=600)
        if r.status_code == 200:
            open(path, "wb").write(r.content)
        time.sleep(2 * (k + 1))
    if not P.pdf_ok(path):
        raise RuntimeError("incomplete PDF " + url)
    return path


def build_editions():
    for key, url, page, docs in EDITIONS:
        pages = P.extract_pages(fetch_pdf(key, url))
        clean = P.clean_pages(pages)
        for out, title, ident, typ, dt, amended, a, b, drops in docs:
            body, notes = P.split_footnotes(clean[a:b], start=FN_START.get(out))
            body = P.drop_lines(body, [d + r"(\[\^\d+\])?" for d in drops])
            md = P.lines_to_md(body)
            front = {
                "title": title, "identifier": ident, "type": typ, "jurisdiction": "pe", "language": "es",
                "date": dt, "last_amended": amended, "status": "in_force",
                "source": GOB + page, "source_pdf": url, "retrieved": TODAY,
            }
            pre = ("> Texto tomado de la edición oficial del Ministerio de Justicia y Derechos Humanos"
                   + (f" (texto actualizado al {amended})" if amended else "")
                   + ". Las notas al pie de la edición oficial se reproducen al final.")
            path = os.path.join(REPO, out)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            open(path, "w", encoding="utf-8").write(P.render(front, title, md, notes, pre))
            print(out, len(md), "chars", md.count("\n###### "), "articles", len(notes), "notes")


def build_index():
    for name, label in (("leyes", "Leyes, resoluciones legislativas y decretos leyes"),
                        ("decretos-legislativos", "Decretos legislativos")):
        tsv = os.path.join(RAW, f"index-{name}.tsv")
        if not os.path.exists(tsv):
            continue
        rows = list(csv.reader(open(tsv, encoding="utf-8"), delimiter="\t"))
        seen = set()
        uniq = []
        for r in rows:
            k = tuple(r[:3])
            if k not in seen:
                seen.add(k)
                uniq.append(r)
        buckets = {}
        for r in uniq:
            n = int(re.sub(r"\D", "", r[1]) or 0)
            buckets.setdefault(n // 1000, []).append(r)
        d = os.path.join(REPO, "indice", name)
        os.makedirs(d, exist_ok=True)
        for kb, rs in sorted(buckets.items()):
            lo, hi = kb * 1000, kb * 1000 + 999
            fn = os.path.join(d, f"{lo:05d}-{hi:05d}.md")
            front = {"title": f"Índice: {label} N° {lo}–{hi}", "type": "index", "jurisdiction": "pe", "language": "es",
                     "source": "https://www.leyes.congreso.gob.pe/", "retrieved": TODAY}
            lines = ["| Tipo | Número | Publicación | Título | Observación |", "|---|---|---|---|---|"]
            for r in sorted(rs, key=lambda r: (int(re.sub(r"\D", "", r[1]) or 0), r[0])):
                cells = [c.replace("|", "\\|").replace("\n", " ") for c in r[:5]]
                lines.append("| " + " | ".join(cells) + " |")
            body = ("Metadatos (sin texto) del Archivo Digital de la Legislación del Perú del Congreso de la "
                    "República.\n\n" + "\n".join(lines))
            open(fn, "w", encoding="utf-8").write(P.render(front, front["title"], body))
        print(name, len(uniq), "entries")


if __name__ == "__main__":
    if "--index-only" not in sys.argv:
        build_editions()
    build_index()
