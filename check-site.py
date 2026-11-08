#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Vérifie les pages de cours générées, avant de pousser.

Contrôle, pour chaque <niveau>/<matière>/<chapitre>/cours-*.html :
  - l'équilibre des balises ;
  - l'unicité des id et la validité des liens internes ;
  - l'absence de formule non rendue (du LaTeX brut visible) ;
  - la présence d'un TL;DR et d'un « à retenir » sur chaque page ;
  - l'autonomie du fichier (aucune ressource externe, hors lecteur YouTube du chapitre) ;
et, pour le dépôt entier, qu'aucun PDF n'est suivi par git.
"""
import glob, os, re, subprocess, sys
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.abspath(__file__))
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source",
        "track", "wbr", "path", "circle", "rect", "line", "polyline", "polygon", "ellipse",
        "use", "stop", "animate", "animateMotion", "animateTransform", "set", "image",
        "feGaussianBlur", "feOffset", "feBlend", "feMerge", "feMergeNode", "mpath"}

class Balises(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.pile, self.err = [], []
    def handle_starttag(self, t, a):
        if t not in VOID:
            self.pile.append(t)
    def handle_endtag(self, t):
        if t in VOID:
            return
        if self.pile and self.pile[-1] == t:
            self.pile.pop()
        elif t in self.pile:
            while self.pile and self.pile.pop() != t:
                pass
            self.err.append("mal imbriquée : " + t)
        else:
            self.err.append("fermeture orpheline : " + t)

def verifie(path):
    pb = []
    h = open(path, encoding="utf-8").read()

    p = Balises(); p.feed(h)
    if p.pile:
        pb.append("balises non fermées : %s" % p.pile[:5])
    if p.err:
        pb.append("imbrication : %s" % p.err[:5])

    ids = re.findall(r'(?<![-\w])id="([^"]+)"', h)
    dup = sorted({i for i in ids if ids.count(i) > 1})
    if dup:
        pb.append("id dupliqués : %s" % dup[:5])
    casses = sorted({a for a in re.findall(r'href="#([^"]+)"', h)} - set(ids))
    if casses:
        pb.append("liens internes cassés : %s" % casses[:5])

    reste = len(re.findall(r'class="math\s+(?:inline|display)"', h))
    if reste:
        pb.append("formules non rendues : %d (pandoc --wrap=none ?)" % reste)

    # du LaTeX brut visible dans le texte de la page ?
    t = re.sub(r"<(svg|script|style|annotation)\b.*?</\1>", "", h, flags=re.S)
    t = re.sub(r"<[^>]+>", "", t)
    brut = sorted(set(re.findall(r"\\[A-Za-z]{2,}", t)))
    if brut:
        pb.append("commandes LaTeX visibles : %s" % brut[:5])

    pages = re.split(r'(?=<section class="pane )', h)[1:]
    sans = [re.search(r'id="([^"]+)"', s).group(1) for s in pages
            if 'class="tldr"' not in s.split("</section>")[0]
            and 'class="pourexos"' not in s.split("</section>")[0]]
    if sans:
        pb.append("pages sans TL;DR ni « à retenir » : %s" % sans[:5])

    ext = re.findall(r'(?:src|href)="(https?:)?//[^"]+"', h)
    ext = [e for e in re.findall(r'(?:src|href)="([^"#]+)"', h)
           if e.startswith("http") or e.startswith("//")]
    # tolérés : les liens de licence et de dépôt, et le seul lecteur vidéo de la page
    tol = ("creativecommons.org", "github.com", "youtube-nocookie.com/embed/")
    ext = [e for e in ext if not any(t in e for t in tol)]
    if ext:
        pb.append("ressources externes : %s" % ext[:3])

    n = len(pages)
    svg = h.count("<svg class=\"figsvg")
    anim = len(re.findall(r"<animate|<set ", h))
    katex = h.count('class="katex')
    return pb, "%d pages · %d figures (%d éléments animés) · %d formules · %d Ko" % (
        n, svg, anim, katex, len(h) // 1024)

ok = True
cours = sorted(glob.glob(os.path.join(ROOT, "*", "*", "*", "cours-*.html")))
if not cours:
    sys.exit("aucun fichier cours-*.html trouvé")
for c in cours:
    pb, info = verifie(c)
    rel = os.path.relpath(c, ROOT)
    print("%s\n  %s" % (rel, info))
    for x in pb:
        ok = False
        print("  ANOMALIE : %s" % x)

try:
    suivis = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True).stdout
    pdf = [l for l in suivis.split("\n") if re.search(r"\.(pdf|epub|djvu)$", l, re.I)]
    if pdf:
        ok = False
        print("ANOMALIE : document sous copyright suivi par git : %s" % pdf)
    else:
        print("aucun PDF suivi par git : OK")
except FileNotFoundError:
    print("git absent : contrôle des PDF ignoré")

print("\n%s" % ("tout est bon." if ok else "des anomalies subsistent (voir ci-dessus)."))
sys.exit(0 if ok else 1)
