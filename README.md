# LawCodex — Perú (pe)

Peruvian legislation as Markdown: the **Constitución Política del Perú de 1993** (current
text) and a set of codes and laws taken from the **official editions** (*Ediciones
Oficiales*) published by the Ministerio de Justicia y Derechos Humanos (MINJUS) on gob.pe,
plus a metadata **index of numbered norms** (leyes, resoluciones legislativas, decretos leyes,
decretos legislativos) from the Congreso's *Archivo Digital de la Legislación del Perú*.

Part of [LawCodex](https://github.com/LawCodex): one public repository per jurisdiction.

Retrieved: **2026-10-13**. Language: Spanish (`es`).

Status: **minimal / partial** — see "What is NOT covered".

## What is covered

| Category | Directory | Files |
|---|---|---|
| Constitución Política del Perú de 1993 (21st official edition, updated to 2025-12-05) | `constitucion/` | 1 |
| Codes (official editions) | `codigos/` | 5 |
| Laws (official editions) | `leyes/` | 7 |
| Index (metadata only) of numbered norms | `indice/` | see below |

### Texts

| File | Norm | Official edition (text updated to) |
|---|---|---|
| [constitucion/constitucion-politica-del-peru-1993.md](constitucion/constitucion-politica-del-peru-1993.md) | Constitución Política del Perú de 1993 | 21st official edition, 2025-12-05 |
| [codigos/codigo-civil-decreto-legislativo-295.md](codigos/codigo-civil-decreto-legislativo-295.md) | Código Civil (Decreto Legislativo N° 295) | 14th official edition, 2014-08-01 (**not updated since**) |
| [codigos/codigo-procesal-penal-decreto-legislativo-957.md](codigos/codigo-procesal-penal-decreto-legislativo-957.md) | Código Procesal Penal (Decreto Legislativo N° 957) | 8th official edition, November 2024 |
| [codigos/nuevo-codigo-procesal-constitucional-ley-31307.md](codigos/nuevo-codigo-procesal-constitucional-ley-31307.md) | Nuevo Código Procesal Constitucional (Ley N° 31307) | 1st official edition, 2023-07-19 |
| [codigos/codigo-de-proteccion-y-defensa-del-consumidor-ley-29571.md](codigos/codigo-de-proteccion-y-defensa-del-consumidor-ley-29571.md) | Código de Protección y Defensa del Consumidor (Ley N° 29571) | 3rd official edition, 2020-11-27 |
| [codigos/codigo-de-responsabilidad-penal-de-adolescentes-decreto-legislativo-1348.md](codigos/codigo-de-responsabilidad-penal-de-adolescentes-decreto-legislativo-1348.md) | Código de Responsabilidad Penal de Adolescentes (Decreto Legislativo N° 1348) | 1st official edition, 2018-08-30 |
| [leyes/tuo-ley-27444-ley-del-procedimiento-administrativo-general.md](leyes/tuo-ley-27444-ley-del-procedimiento-administrativo-general.md) | TUO de la Ley N° 27444, Ley del Procedimiento Administrativo General (D.S. N° 006-2026-JUS) | 1st official edition, 2026-07-08 |
| [leyes/tuo-ley-organica-del-poder-judicial-ds-017-93-jus.md](leyes/tuo-ley-organica-del-poder-judicial-ds-017-93-jus.md) | TUO de la Ley Orgánica del Poder Judicial (D.S. N° 017-93-JUS) | 3rd official edition (undated, c. 2019) |
| [leyes/ley-organica-del-ministerio-publico-decreto-legislativo-52.md](leyes/ley-organica-del-ministerio-publico-decreto-legislativo-52.md) | Ley Orgánica del Ministerio Público (Decreto Legislativo N° 52) | same edition |
| [leyes/ley-28301-ley-organica-del-tribunal-constitucional.md](leyes/ley-28301-ley-organica-del-tribunal-constitucional.md) | Ley Orgánica del Tribunal Constitucional (Ley N° 28301) | 2023-07-19 |
| [leyes/ley-30057-ley-del-servicio-civil.md](leyes/ley-30057-ley-del-servicio-civil.md) | Ley del Servicio Civil (Ley N° 30057) | 1st official edition, 2017-12-07 |
| [leyes/ley-26300-ley-de-los-derechos-de-participacion-y-control-ciudadanos.md](leyes/ley-26300-ley-de-los-derechos-de-participacion-y-control-ciudadanos.md) | Ley de los Derechos de Participación y Control Ciudadanos (Ley N° 26300) | 2025-12-04 |
| [leyes/ley-30220-ley-universitaria.md](leyes/ley-30220-ley-universitaria.md) | Ley Universitaria (Ley N° 30220) | 2023-12-28 |

Notes on the texts:

- Only the normative part of each official edition is converted: MINJUS's presentation,
  reader's guide, lists of concordant norms, explanatory manuals, amendment tables and indexes
  are omitted.
- The official editions carry editorial footnotes (amendment history, interpretation notes).
  They are reproduced at the end of each file under "Notas de la edición"; where the footnote
  marker could be located in the text it is linked as a Markdown footnote.
- Running page headers/footers and page numbers are removed and wrapped lines are re-joined;
  the text is otherwise as extracted from the PDF (some list layout or two-column front matter
  — e.g. the list of members of the Congreso Constituyente — may read imperfectly).
- MINJUS's own *sumillas* (article captions) appear as a separate line above the article
  heading; official *sumillas* that follow the article number are part of the heading.

### Index (`indice/`)

`indice/leyes/<range>.md` and `indice/decretos-legislativos/<range>.md` list, per block of
1,000 numbers, the type, number, publication date and title of each norm as given by the
Congreso's *Archivo Digital de la Legislación del Perú* (https://www.leyes.congreso.gob.pe/,
"Legislación desde 1904", search by number). These are metadata only, without text.

## What is NOT covered

- **Full texts of the ~32,000 numbered laws, decretos legislativos, decretos de urgencia, and
  the Código Civil, Código Penal, Código Procesal Civil, Código Tributario, etc.** The
  authoritative consolidated source is **SPIJ** (Sistema Peruano de Información Jurídica,
  https://spij.minjus.gob.pe/, free since 2020), but it was **unreachable** from our network
  (connection timeouts on every attempt, also for www.minjus.gob.pe and diariooficial.elperuano.pe),
  and no archived copy was available (the Internet Archive was offline at retrieval time).
- The Congreso's archive links each law to a PDF (`/Documentos/...pdf`), but its robots.txt
  asks robots not to fetch PDFs (`Disallow: /*.pdf$`), so the texts were not downloaded —
  only the HTML result lists were used for the index.
- Other MINJUS publications (compendia, jurisprudence collections, older editions superseded by
  the ones above). Official editions were located through gob.pe's sitemap (the paginated
  `?sheet=` collection listing is disallowed by robots.txt).
- The Código Civil edition is the latest one MINJUS has published (2014); amendments after
  August 2014 are not reflected.
- Regulations (decretos supremos, resoluciones), regional and municipal norms.

## Sources

- MINJUS — Ediciones Oficiales: https://www.gob.pe/institucion/minjus/colecciones/2135-ediciones-oficiales
  (each file's front matter has the publication page `source` and the PDF `source_pdf`).
- Congreso de la República — Archivo Digital de la Legislación del Perú: https://www.leyes.congreso.gob.pe/

## Copyright

Legislative, administrative and judicial official texts are excluded from copyright protection
in Peru (Decreto Legislativo N° 822, Ley sobre el Derecho de Autor, art. 9). The editorial
footnotes are MINJUS notes from the official editions, published by the State for public
dissemination.

## Structure

```
constitucion/                         Constitution of 1993
codigos/<slug>.md                     codes
leyes/<slug>.md                       laws
indice/leyes/<nnnnn>-<nnnnn>.md       index of leyes / resoluciones legislativas / decretos leyes
indice/decretos-legislativos/...      index of decretos legislativos
```

Front matter: `identifier` is the norm number; `last_amended` is the date to which the official
edition is updated; `source` is the gob.pe publication page and `source_pdf` the PDF.

## Regenerate

```
python3 -m venv .venv && .venv/bin/pip install -r scripts/requirements.txt
RAW=/path/to/scratch .venv/bin/python scripts/pe_index.py   # Congreso index (HTML pages, ~1,700 requests)
RAW=/path/to/scratch .venv/bin/python scripts/pe_build.py   # official editions + index rendering
```

`scripts/pe_pdfmd.py` is the PDF-text → Markdown converter (header/footer removal, footnote
extraction, heading detection). Page ranges of the normative part of each edition are
configured in `pe_build.py`.
