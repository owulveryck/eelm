# -*- coding: utf-8 -*-
"""Dessins de base de la vidéo de révision « spécial test ».

Les cartes de lignes de champ ne sont pas dessinées à la main : elles sont
intégrées numériquement à partir du champ des charges (fonction ligne()), donc
leur allure est exacte — c'est justement ce que le test demande de reconnaître.
"""
import math
from canvas import (C, W, H, INK, MUT, POS, NEG, ACC, SOFT, OR, PALE, BG,
                    ease, pingpong, clamp, seg)

CX = W / 2.0

# ----------------------------------------------------------------- petits utilitaires
def sous(c, s, y=186, size=40, col=INK, op=None):
    c.txt(CX, y, s, size=size, col=col, op=op)

def chip(c, x, y, s, size=30, col=INK, bold=False, pad=18):
    """étiquette sur fond blanc, pour rester lisible par-dessus un dessin"""
    w = len(s) * size * 0.54 + 2 * pad
    c.rect(x - w / 2.0, y - size * 0.86, w, size * 1.52, fill="#ffffff", col=None, rx=8, op=0.92)
    c.txt(x, y + size * 0.34, s, size=size, col=col, bold=bold)

def puces(c, items, upto, x, y0, dy=74, size=33, actif=True):
    """liste à puces qui se construit au fil des phrases"""
    for i, s in enumerate(items):
        if i >= upto:
            break
        der = (i == upto - 1) and actif
        c.dot(x - 28, y0 + i * dy - 11, 8, col=OR if der else SOFT)
        c.txt(x, y0 + i * dy, s, size=size, col=INK if der else MUT, anchor="start")

def tableau(c, x, y, cols, lignes, cw=None, rh=56, size=28, hl=None, hlcol=OR,
            hlc=()):
    """tableau simple : cols = en-têtes, lignes = liste de listes.
    hl = indice de ligne à mettre en valeur."""
    n = len(cols)
    cw = cw or [150] * n
    yy = y
    for j in hlc:                                   # colonnes mises en valeur
        c.rect(x + sum(cw[:j]), y, cw[j], rh * (len(lignes) + 1), fill="#fdf0e2")
    c.rect(x, yy, sum(cw), rh, fill=PALE)
    xx = x
    for j, t in enumerate(cols):
        c.txt(xx + cw[j] / 2.0, yy + rh / 2.0 + 10, t, size=size, col=INK, bold=True)
        xx += cw[j]
    yy += rh
    for i, L in enumerate(lignes):
        if hl is not None and i == hl:
            c.rect(x, yy, sum(cw), rh, fill="#fdf0e2")
        xx = x
        for j, t in enumerate(L):
            col = hlcol if ((hl is not None and i == hl and j > 0) or j in hlc) else INK
            c.txt(xx + cw[j] / 2.0, yy + rh / 2.0 + 10, t, size=size, col=col,
                  bold=(hl is not None and i == hl) or j in hlc)
            xx += cw[j]
        yy += rh
    # la grille
    tot = sum(cw)
    for i in range(len(lignes) + 2):
        c.line(x, y + i * rh, x + tot, y + i * rh, col=SOFT, sw=1.6, cap="butt")
    xx = x
    for j in range(n + 1):
        c.line(xx, y, xx, y + (len(lignes) + 1) * rh, col=SOFT, sw=1.6, cap="butt")
        if j < n:
            xx += cw[j]

# ----------------------------------------------------------------- lignes de champ
def _champ(chs, x, y):
    """champ des charges chs = [(x, y, q)] au point (x, y), en unités arbitraires"""
    ex = ey = 0.0
    for cx, cy, q in chs:
        dx, dy = x - cx, y - cy
        r2 = dx * dx + dy * dy
        if r2 < 1.0:
            return 0.0, 0.0
        r3 = r2 * math.sqrt(r2)
        ex += q * dx / r3
        ey += q * dy / r3
    return ex, ey

def ligne(chs, x, y, sgn=1, ds=7.0, nmax=700, box=(40, 126, W - 40, H - 30), rstop=30):
    """suit une ligne de champ depuis (x, y) — méthode du point milieu."""
    pts = [(x, y)]
    for _ in range(nmax):
        ex, ey = _champ(chs, x, y)
        n = math.hypot(ex, ey)
        if n < 1e-13:
            break
        xm, ym = x + sgn * ds * 0.5 * ex / n, y + sgn * ds * 0.5 * ey / n
        ex, ey = _champ(chs, xm, ym)
        n = math.hypot(ex, ey)
        if n < 1e-13:
            break
        x, y = x + sgn * ds * ex / n, y + sgn * ds * ey / n
        pts.append((x, y))
        if not (box[0] < x < box[2] and box[1] < y < box[3]):
            break
        if any(math.hypot(x - cx, y - cy) < rstop for cx, cy, q in chs if q * sgn < 0):
            break
    return pts

def trait(c, pts, col=SOFT, sw=3.0, op=None):
    if len(pts) < 2:
        return
    d = "M%.1f %.1f " % pts[0] + " ".join("L%.1f %.1f" % p for p in pts[1:])
    c.path(d, col=col, sw=sw, op=op)

def tete(c, pts, u, col=SOFT, s=17, op=None):
    """pointe de flèche à la fraction u du trajet, orientée dans le sens du parcours"""
    if len(pts) < 6:
        return
    i = int(clamp(u) * (len(pts) - 2))
    (x1, y1), (x2, y2) = pts[i], pts[i + 1]
    dx, dy = x2 - x1, y2 - y1
    n = math.hypot(dx, dy)
    if n < 1e-9:
        return
    ux, uy = dx / n, dy / n
    px, py = -uy, ux
    c.path("M%.1f %.1f L%.1f %.1f L%.1f %.1f Z"
           % (x2 + ux * s, y2 + uy * s,
              x2 - ux * s * 0.5 + px * s * 0.66, y2 - uy * s * 0.5 + py * s * 0.66,
              x2 - ux * s * 0.5 - px * s * 0.66, y2 - uy * s * 0.5 - py * s * 0.66),
           col=col, sw=1.0, fill=col, op=op)

_CACHE = {}

def carte(c, x1, x2, y, s1, s2, n=14, r=42, col=NEG, sw=3.2, fl=(0.3, 0.72),
          box=(40, 126, W - 40, H - 30), ds=7.0):
    """carte des lignes de champ de deux charges ponctuelles de même valeur.
    s1, s2 = signes. Renvoie la liste des tracés.

    Les tracés sont mis en cache : une même carte est demandée 36 fois par plan
    (le montage compare les images d'une boucle pour savoir si le plan est animé),
    et l'intégration des lignes est ce qui coûte le plus cher ici."""
    cle = (x1, x2, y, s1, s2, n, r, box, ds)
    out = _CACHE.get(cle)
    if out is None:
        chs = [(x1, y, float(s1)), (x2, y, float(s2))]
        out = []
        for (xs, ys, q) in chs:
            if q < 0 and s1 * s2 < 0:
                continue                  # dipôle : les lignes tracées depuis le + suffisent
            for k in range(n):
                a = 2 * math.pi * (k + 0.5) / n
                out.append(ligne(chs, xs + (r + 2) * math.cos(a), ys + (r + 2) * math.sin(a),
                                 sgn=1 if q > 0 else -1, box=box, ds=ds))
        _CACHE[cle] = out
    for pts in out:
        trait(c, pts, col=col, sw=sw)
        for u in fl:
            tete(c, pts, u, col=col)
    c.charge(x1, y, s1, r=r)
    c.charge(x2, y, s2, r=r)
    return out

# ----------------------------------------------------------------- le condensateur
def condensateur(c, x, y, w, h, nl=7, equi=False, bords=False, zone=False,
                 U=None, dd=True, col=POS, marge=90):
    """deux plaques parallèles, les lignes de champ, et au besoin les équipotentielles,
    la zone uniforme et l'évasement près des bords."""
    c.rect(x, y, w, 16, fill=POS)
    c.rect(x, y + h, w, 16, fill=NEG)
    c.txt(x - 34, y + 20, "+", size=48, col=POS, anchor="end")
    c.txt(x - 34, y + h + 28, "–", size=54, col=NEG, anchor="end")
    if U is not None:
        c.txt(x + w / 2.0, y - 36, U, size=38, col=INK, bold=True)
    if dd:
        c.line(x + w + 56, y + 16, x + w + 56, y + h, col=MUT, sw=3)
        c.line(x + w + 46, y + 16, x + w + 66, y + 16, col=MUT, sw=3)
        c.line(x + w + 46, y + h, x + w + 66, y + h, col=MUT, sw=3)
        c.txt(x + w + 86, y + h / 2.0 + 12, "d", size=42, col=MUT, it=True, anchor="start")
    # les lignes de champ, de la plaque + vers la plaque –
    for j in range(nl):
        xx = x + marge + (w - 2 * marge) * j / float(nl - 1)
        c.arrow(xx, y + 24, xx, y + h - 10, col=col, sw=4, head=20)
    if bords:
        for s in (-1, 1):
            for k in range(3):
                x0 = x + (w - 14 if s > 0 else 14)
                b = 60 + 46 * k
                c.path("M%.1f %.1f C%.1f %.1f %.1f %.1f %.1f %.1f"
                       % (x0, y + 22, x0 + s * b, y + 30 + 0.18 * h,
                          x0 + s * b, y + h - 30 - 0.18 * h, x0, y + h - 14),
                       col=SOFT, sw=3)
    if equi:
        for j in range(5):
            yy = y + 16 + (h - 16) * (j + 0.5) / 5.0
            c.line(x - 20, yy, x + w + 20, yy, col=ACC, sw=2.4, dash="12 12")
        c.txt(x + w / 2.0, y + h + 108, "équipotentielles : parallèles aux plaques",
              size=26, col=ACC)
    if zone:
        c.rect(x + marge - 30, y + 30, w - 2 * marge + 60, h - 56, col=OR, sw=3,
               fill="none", rx=10, dash="14 12")

# ----------------------------------------------------------------- Millikan
def dispositif(c, etape=9, t=0.0, x0=560, y0=250):
    """le montage de Millikan : pulvérisateur, plaques, rayons X, microscope"""
    bw, bh = 700, 300
    bx, by = x0, y0 + 120
    # la chambre
    c.rect(bx - 120, by - 110, bw + 240, bh + 220, fill="#ffffff", col=SOFT, sw=3, rx=12)
    # le pulvérisateur
    c.rect(bx + 40, y0 - 60, 150, 70, fill=PALE, col=MUT, sw=3, rx=10)
    c.txt(bx + 20, y0 - 18, "pulvérisateur d’huile", size=25, col=MUT, anchor="end")
    c.path("M%d %d L%d %d" % (bx + 190, y0 - 25, bx + 260, y0 - 25), col=MUT, sw=4)
    # les plaques, avec le trou dans la plaque du haut
    c.rect(bx, by, 300, 14, fill=POS)
    c.rect(bx + 350, by, bw - 350, 14, fill=POS)
    c.rect(bx, by + bh, bw, 14, fill=NEG)
    c.txt(bx + 325, by - 26, "trou", size=23, col=MUT)
    c.txt(bx - 30, by + 18, "+", size=44, col=POS, anchor="end")
    c.txt(bx - 30, by + bh + 26, "–", size=50, col=NEG, anchor="end")
    # les gouttelettes qui tombent par le trou
    for k in range(4):
        u = (t + k / 4.0) % 1.0
        c.dot(bx + 325 + 6 * math.sin(7 * u), y0 - 10 + (by - y0 + 10) * u, 7, col=MUT, op=0.6)
    if etape >= 1:                                    # les rayons X
        c.txt(bx - 310, by + bh / 2.0 - 46, "source de", size=26, col=ACC)
        c.txt(bx - 310, by + bh / 2.0 - 14, "rayons X", size=26, col=ACC)
        for k in range(3):
            yy = by + bh / 2.0 + 20 + k * 26
            c.line(bx - 400, yy, bx - 136, yy, col=ACC, sw=3, dash="16 10")
        c.arrow(bx - 170, by + bh / 2.0 + 46, bx - 130, by + bh / 2.0 + 46,
                col=ACC, sw=3, head=14)
    if etape >= 2:                                    # le microscope
        mx = bx + bw + 180
        c.rect(mx, by + bh / 2.0 - 34, 190, 68, fill=PALE, col=MUT, sw=3, rx=8)
        c.path("M%d %d L%d %d L%d %d L%d %d Z"
               % (mx, by + bh / 2.0 - 34, mx - 60, by + bh / 2.0 - 58,
                  mx - 60, by + bh / 2.0 + 58, mx, by + bh / 2.0 + 34),
               col=MUT, sw=3, fill="#ffffff")
        c.txt(mx + 95, by + bh / 2.0 + 92, "microscope", size=26, col=MUT)
        c.line(bx + bw + 40, by + bh / 2.0, mx - 66, by + bh / 2.0, col=SOFT, sw=2, dash="8 8")
    # la gouttelette observée
    gy = by + bh / 2.0
    c.dot(bx + bw / 2.0, gy, 15, col=INK)
    c.txt(bx + bw / 2.0 + 30, gy - 24, "la goutte", size=25, col=INK, anchor="start")
    if etape >= 3:                                    # l'alimentation réglable
        yw = by + bh + 140
        c.line(bx + 40, by + 7, bx - 80, by + 7, col=MUT, sw=3)      # la plaque ⊕
        c.line(bx - 80, by + 7, bx - 80, yw, col=MUT, sw=3)
        c.line(bx - 80, yw, bx + 250, yw, col=MUT, sw=3)
        c.circle(bx + 300, yw, 50, col=MUT, sw=3, fill="#ffffff")
        c.txt(bx + 300, yw + 12, "U", size=38, col=INK, it=True)
        c.line(bx + 350, yw, bx + bw - 60, yw, col=MUT, sw=3)        # la plaque ⊖
        c.line(bx + bw - 60, yw, bx + bw - 60, by + bh + 14, col=MUT, sw=3)
        c.txt(bx + 300, yw + 78, "tension réglable", size=25, col=MUT)
    return bx, by, bw, bh, gy

def bilan(c, cx, cy, fe, fg, r=17, lab=True):
    """la goutte et les deux forces : fe et fg sont des longueurs en pixels"""
    c.dot(cx, cy, r, col=INK)
    c.arrow(cx, cy - r - 8, cx, cy - r - 8 - fe, col=ACC, sw=7, head=24)
    c.arrow(cx, cy + r + 8, cx, cy + r + 8 + fg, col=MUT, sw=7, head=24)
    if lab:
        c.txt(cx - 46, cy - r - 8 - fe / 2.0, "qE", size=34, col=ACC, it=True, anchor="end")
        c.txt(cx + 46, cy + r + 8 + fg / 2.0 + 10, "mg", size=34, col=MUT, it=True,
              anchor="start")

def nuage(c, x, y, w, h, nmax=5, pal=True, labe=True):
    """les charges mesurées sur 50 gouttelettes : des paliers, pas un nuage au hasard"""
    import random
    rd = random.Random(11)
    c.line(x, y, x, y + h, col=INK, sw=3)
    c.line(x, y + h, x + w, y + h, col=INK, sw=3)
    c.txt(x - 54, y - 14, "q", size=34, col=INK, it=True)
    c.txt(x - 76, y + 26, "(10⁻¹⁹ C)", size=22, col=MUT, anchor="middle")
    c.txt(x + w - 10, y + h + 46, "numéro de la gouttelette", size=24, col=MUT, anchor="end")
    for n in range(1, 6):
        yy = y + h - h * n / 5.6
        if n <= nmax:
            if pal:
                c.line(x, yy, x + w, yy, col=OR, sw=2, dash="12 10", op=0.8)
            c.txt(x - 16, yy + 10, "%d,%d" % (int(1.6 * n), round(16 * n) % 10),
                  size=24, col=OR, anchor="end")
            if labe:
                c.txt(x + w + 24, yy + 10, "%de" % n if n > 1 else "e", size=28, col=OR,
                      anchor="start", it=True)
        for k in range(10):
            if n > nmax:
                break
            px = x + 24 + (w - 48) * ((n - 1) * 10 + k + rd.random() * 0.7) / 50.0
            c.dot(px, yy + (rd.random() - 0.5) * 13, 7, col=NEG)

def escalier(c, x, y, w, h, rampe=True):
    """l'escalier (quantifié) à côté de la rampe (continu)"""
    n = 5
    d = "M%.1f %.1f" % (x, y + h)
    for i in range(n):
        d += " L%.1f %.1f L%.1f %.1f" % (x + w * i / n, y + h - h * i / n,
                                         x + w * (i + 1) / n, y + h - h * i / n)
    d += " L%.1f %.1f" % (x + w, y)
    c.path(d, col=OR, sw=5)
    if rampe:
        c.line(x, y + h, x + w, y, col=SOFT, sw=5, dash="14 12")
