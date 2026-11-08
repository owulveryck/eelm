# -*- coding: utf-8 -*-
"""Composition des formules par LaTeX, inlinées en SVG vectoriel (via dvisvgm)."""
import hashlib, json, os, re, subprocess, sys

SP = os.path.dirname(os.path.abspath(__file__))
# le cache des formules va dans le dossier de travail du chapitre (VIDEO_BUILD)
CACHE = os.path.join(os.environ.get("VIDEO_BUILD", SP), "texcache")
os.makedirs(CACHE, exist_ok=True)
_n = [0]

DOC = r"""\documentclass[preview,border=1pt,12pt]{standalone}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{amsmath,amssymb}
\begin{document}
$\displaystyle %s$
\end{document}
"""

def _render(s):
    h = hashlib.md5(s.encode("utf-8")).hexdigest()[:16]
    meta = os.path.join(CACHE, h + ".json")
    if os.path.exists(meta):
        return json.load(open(meta))
    d = os.path.join(CACHE, h)
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "f.tex"), "w", encoding="utf-8").write(DOC % s)
    r = subprocess.run(["latex", "-interaction=nonstopmode", "-halt-on-error", "f.tex"],
                       cwd=d, capture_output=True, text=True)
    if r.returncode:
        sys.exit("LaTeX a refusé :\n  %s\n%s" % (s, r.stdout[-1200:]))
    r = subprocess.run(["dvisvgm", "--no-fonts", "--exact-bbox", "-o", "f.svg", "f.dvi"],
                       cwd=d, capture_output=True, text=True)
    if r.returncode:
        sys.exit("dvisvgm a échoué pour : %s\n%s" % (s, r.stderr[-600:]))
    svg = open(os.path.join(d, "f.svg"), encoding="utf-8").read()
    m = re.search(r"<svg[^>]*width='([\d.]+)pt'[^>]*height='([\d.]+)pt'[^>]*"
                  r"viewBox='([-\d.]+) ([-\d.]+) ([\d.]+) ([\d.]+)'", svg)
    if not m:
        sys.exit("en-tête SVG illisible pour : %s" % s)
    inner = svg[svg.index(">", svg.index("<svg")) + 1: svg.rindex("</svg>")]
    out = dict(w=float(m.group(1)), h=float(m.group(2)),
               vx=float(m.group(3)), vy=float(m.group(4)), inner=inner)
    json.dump(out, open(meta, "w"))
    return out

def group(s, x, y, hpx=None, wpx=None, col="#1d1d20", anchor="mid", op=None,
          pt=None, maxw=None):
    """Renvoie (svg, largeur, hauteur) : la formule placée, ancrée par son centre
    (anchor='mid'), son coin haut-gauche ('tl'), le milieu gauche ('ml') ou droit ('mr').
    pt = corps de la formule (comparable à une taille de police) ; maxw la borne en largeur."""
    d = _render(s)
    if pt:
        sc = pt / 12.0
    elif hpx:
        sc = hpx / d["h"]
    else:
        sc = wpx / d["w"]
    if maxw and d["w"] * sc > maxw:
        sc = maxw / d["w"]
    w, h = d["w"] * sc, d["h"] * sc
    if anchor == "mid":
        x0, y0 = x - w / 2.0, y - h / 2.0
    elif anchor == "ml":
        x0, y0 = x, y - h / 2.0
    elif anchor == "mr":
        x0, y0 = x - w, y - h / 2.0
    else:
        x0, y0 = x, y
    # préfixe déterministe : deux images successives d'un plan fixe doivent
    # produire exactement le même SVG, sinon le plan est pris pour animé.
    pre = "t%s_" % hashlib.md5(
        ("%s|%.2f|%.2f|%.5f|%s" % (s, x0, y0, sc, col)).encode("utf-8")).hexdigest()[:8]
    inner = re.sub(r"id='(g\d+-\d+)'", lambda m: "id='%s%s'" % (pre, m.group(1)), d["inner"])
    inner = re.sub(r"xlink:href='#(g\d+-\d+)'",
                   lambda m: "xlink:href='#%s%s'" % (pre, m.group(1)), inner)
    o = ' opacity="%g"' % op if op is not None else ''
    g = ('<g transform="translate(%.2f %.2f) scale(%.5f) translate(%.3f %.3f)" fill="%s" '
         'stroke="none"%s>%s</g>' % (x0, y0, sc, -d["vx"], -d["vy"], col, o, inner))
    return g, w, h

def put(c, s, x, y, hpx=None, wpx=None, col="#1d1d20", anchor="mid", op=None,
        pt=None, maxw=None):
    g, w, h = group(s, x, y, hpx, wpx, col, anchor, op, pt, maxw)
    c.el.append(g)
    return w, h
