from pathlib import Path

import pypandoc
import typst

MAPA = Path(__file__).parent
PRIVREMENO = MAPA / "izvjestaj.typ"
PDF = MAPA / "Internet_stvari_prvi_programski_zadatak_grupa10.pdf"

UVOD = r"""
#set document(title: "Internet stvari: Prvi programski zadatak", author: "Grupa 10")
#set page(paper: "a4", margin: 2.4cm)
#set text(lang: "hr", size: 11pt)
#set par(justify: true)
#set math.equation(numbering: none)
#show figure.caption: set text(size: 9.5pt)
#show raw.where(block: true): set text(size: 7.5pt)
#show raw.where(block: true): set par(justify: false)
#show heading: set block(above: 1.4em, below: 0.8em)
#show heading.where(level: 1): it => { pagebreak(weak: true); it }
#show figure: set block(above: 1.2em, below: 1.2em)
#set image(width: 90%)

#align(center + horizon)[
  #text(size: 12pt)[Fakultet informatike u Puli] \
  #v(2.5em)
  #text(size: 24pt, weight: "bold")[Internet stvari] \
  #v(0.5em)
  #text(size: 16pt)[Prvi programski zadatak] \
  #v(0.3em)
  #text(size: 12pt, style: "italic")[Odzivi sustava, stabilnost i frekvencijska analiza] \
  #v(2.5em)
  #text(size: 13pt)[Grupa 10]
]

#pagebreak()
#outline(depth: 2)
#pagebreak()
#set page(numbering: "1")
#counter(page).update(1)
"""

PRILOZI = r"""
= Prilog A: Ispis rezultata
#raw(read("rezultati.txt"), block: true)

= Prilog B: Python kod
== analiza.py
#raw(read("analiza.py"), lang: "python", block: true)

== s_plane.py
#raw(read("s_plane.py"), lang: "python", block: true)
"""

tijelo = pypandoc.convert_file(
    str(MAPA / "rjesenje_grupa10.md"), "typst", format="markdown", extra_args=["--wrap=none"]
)
tijelo = tijelo.replace("\r\n", "\n").replace("\\| ", "|").replace(" \\|", "|")
PRIVREMENO.write_text(UVOD + tijelo + PRILOZI, encoding="utf-8")
try:
    typst.compile(PRIVREMENO, output=PDF, root=MAPA)
finally:
    PRIVREMENO.unlink()
print(PDF)
