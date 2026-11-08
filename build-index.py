#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Regenere les pages d'index du site (accueil, niveau, chapitre, galerie de figures).
   Parcourt <niveau>/<matiere>/<chapitre>/ et detecte les chapitres a leur fichier cours-*.html.
   Usage : python3 build-index.py"""
import os, re, html, glob

ROOT = os.path.dirname(os.path.abspath(__file__))
LEVELS = {"S6FR": ("S6 — section française", "Sixième année, programme en français")}
SUBJECTS = {"physique": "Physique", "maths": "Mathématiques", "chimie": "Chimie",
            "biologie": "Biologie", "histoire": "Histoire", "geographie": "Géographie"}

def page(title, depth, breadcrumb, body, sub=""):
    up = "../" * depth
    return """<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
<link rel="stylesheet" href="%sassets/site.css">
</head>
<body>
<header><span class="mark"></span><h1>EELM · ressources</h1><span class="sub">%s</span></header>
<main>
%s
%s
</main>
<footer>Contenu produit à partir des polycopiés de cours · <a href="https://github.com/owulveryck/eelm">code source sur GitHub</a></footer>
</body>
</html>
""" % (html.escape(title), up, html.escape(sub), breadcrumb, body)

def fil(items):
    """fil d'Ariane : [(libelle, href|None)]"""
    out = []
    for lab, href in items:
        out.append('<a href="%s">%s</a>' % (href, html.escape(lab)) if href else html.escape(lab))
    return '<nav class="fil">' + " › ".join(out) + "</nav>"

def md_meta(path):
    t, s = None, None
    if os.path.exists(path):
        head = open(path, encoding="utf-8").read(900)
        m = re.search(r'^title:\s*"?(.+?)"?\s*$', head, re.M)
        if m: t = m.group(1)
        m = re.search(r'^subtitle:\s*"?(.+?)"?\s*$', head, re.M)
        if m: s = m.group(1)
    return t, s

def ko(p):
    n = os.path.getsize(p)
    return "%.0f Ko" % (n / 1024) if n < 1024 * 1024 else "%.1f Mo" % (n / 1048576)

chapters = []          # (level, subject, chap, dir, titre, soustitre, cours_html)
for level in sorted(LEVELS):
    for subject in sorted(os.listdir(os.path.join(ROOT, level))) if os.path.isdir(os.path.join(ROOT, level)) else []:
        sdir = os.path.join(ROOT, level, subject)
        if not os.path.isdir(sdir):
            continue
        for chap in sorted(os.listdir(sdir)):
            cdir = os.path.join(sdir, chap)
            if not os.path.isdir(cdir):
                continue
            cours = sorted(glob.glob(os.path.join(cdir, "cours-*.html")))
            if not cours:
                continue
            mds = sorted(glob.glob(os.path.join(cdir, "*.md")))
            t, s = md_meta(mds[0]) if mds else (None, None)
            chapters.append(dict(level=level, subject=subject, chap=chap, dir=cdir,
                                 titre=t or chap.capitalize(), sous=s or "",
                                 cours=os.path.basename(cours[0]), md=os.path.basename(mds[0]) if mds else None))

# ---------------- page d'accueil
cards = []
for lv in sorted(LEVELS):
    n = len([c for c in chapters if c["level"] == lv])
    cards.append('<a class="card" href="%s/"><b>%s</b><span>%s · %d chapitre%s</span></a>'
                 % (lv, html.escape(LEVELS[lv][0]), html.escape(LEVELS[lv][1]), n, "s" if n > 1 else ""))
body = ("<h2>Ressources de révision</h2>"
        "<p class=\"lead\">Cours remis au propre, figures redessinées et animées, exercices corrigés. "
        "Tout se lit dans le navigateur, hors ligne compris.</p>"
        '<div class="cards">' + "".join(cards) + "</div>")
open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(
    page("EELM — ressources de révision", 0, "", body, "École européenne"))

# ---------------- page de niveau
for lv in sorted(LEVELS):
    bysub = {}
    for c in chapters:
        if c["level"] == lv:
            bysub.setdefault(c["subject"], []).append(c)
    blocks = []
    for sub in sorted(bysub):
        cards = []
        for c in bysub[sub]:
            cards.append('<a class="card" href="%s/%s/"><b>%s</b><span>%s</span></a>'
                         % (c["subject"], c["chap"], html.escape(c["titre"]), html.escape(c["sous"])))
        blocks.append("<h3>%s</h3><div class=\"cards\">%s</div>"
                      % (html.escape(SUBJECTS.get(sub, sub.capitalize())), "".join(cards)))
    body = ("<h2>%s</h2><p class=\"lead\">%s</p>%s"
            % (html.escape(LEVELS[lv][0]), html.escape(LEVELS[lv][1]), "".join(blocks)))
    open(os.path.join(ROOT, lv, "index.html"), "w", encoding="utf-8").write(
        page(LEVELS[lv][0] + " — EELM", 1, fil([("Accueil", "../"), (LEVELS[lv][0], None)]), body, LEVELS[lv][0]))

# ---------------- page de chapitre + galerie
for c in chapters:
    figs = sorted(os.path.basename(f) for f in glob.glob(os.path.join(c["dir"], "figures", "*.svg")))
    anim = [f for f in figs if "anim" in f or f.startswith("sol-")]
    files = ['<li><a href="%s">%s</a> <span class="meta">— le cours complet, %s</span></li>'
             % (c["cours"], c["cours"], ko(os.path.join(c["dir"], c["cours"])))]
    if c["md"]:
        files.append('<li><a href="%s">%s</a> <span class="meta">— la source Markdown (LaTeX pour les formules)</span></li>'
                     % (c["md"], c["md"]))
    files.append('<li><a href="figures.html">figures.html</a> <span class="meta">— les %d figures, dont %d animées</span></li>'
                 % (len(figs), len(anim)))
    body = ("<h2>%s</h2><p class=\"lead\">%s</p>"
            "<p><a class=\"btn\" href=\"%s\">Ouvrir le cours →</a></p>"
            "<h3>Contenu du dossier</h3><ul class=\"files\">%s</ul>"
            % (html.escape(c["titre"]), html.escape(c["sous"]), c["cours"], "".join(files)))
    open(os.path.join(c["dir"], "index.html"), "w", encoding="utf-8").write(
        page(c["titre"] + " — EELM", 3,
             fil([("Accueil", "../../../"), (LEVELS[c["level"]][0], "../../"),
                  (SUBJECTS.get(c["subject"], c["subject"]), "../"), (c["titre"], None)]),
             body, c["titre"]))
    gal = []
    for f in figs:
        tag = " · animée" if (("anim" in f) or f.startswith("sol-")) else ""
        gal.append('<figure><img src="figures/%s" alt="%s" loading="lazy">'
                   '<figcaption>%s%s</figcaption></figure>' % (f, html.escape(f), html.escape(f), tag))
    body = ("<h2>Figures</h2><p class=\"lead\">%d figures SVG, dont %d animées. "
            "Clic droit → « enregistrer l'image » pour les réutiliser.</p><div class=\"gal\">%s</div>"
            % (len(figs), len(anim), "".join(gal)))
    open(os.path.join(c["dir"], "figures.html"), "w", encoding="utf-8").write(
        page("Figures — " + c["titre"], 3,
             fil([("Accueil", "../../../"), (LEVELS[c["level"]][0], "../../"),
                  (SUBJECTS.get(c["subject"], c["subject"]), "../"), (c["titre"], "./"), ("Figures", None)]),
             body, c["titre"]))

print("index régénérés : %d chapitre(s)" % len(chapters))
for c in chapters:
    print("  %s/%s/%s — %s" % (c["level"], c["subject"], c["chap"], c["titre"]))
