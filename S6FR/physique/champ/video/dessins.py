# -*- coding: utf-8 -*-
"""Dessins de base réutilisés par scenes.py.
Une fonction par dessin : (canvas, index de phrase, phase 0..1) -> dessin."""
import math
from canvas import (C, W, H, INK, MUT, POS, NEG, ACC, SOFT, OR, PALE, BG,
                    ease, pingpong, clamp, seg, head, formule)

CX, CY = W / 2.0, 560.0

def bullets(c, items, upto, x, y0, dy=74, size=34, col=INK, puce=OR):
    for i, s in enumerate(items):
        if i > upto:
            break
        op = 1.0 if i < upto else 1.0
        c.dot(x - 26, y0 + i * dy - 11, 8, col=puce, op=op)
        c.txt(x, y0 + i * dy, s, size=size, col=col, anchor="start", op=op)

def soustitre(c, s, y=200, size=40, col=INK, op=None):
    c.txt(CX, y, s, size=size, col=col, op=op)

def plaques(c, x, y, w, h, u="U", col=INK):
    c.rect(x, y, w, 14, fill=POS); c.rect(x, y + h, w, 14, fill=NEG)
    c.txt(x - 30, y + 14, "+", size=46, col=POS, anchor="end")
    c.txt(x - 30, y + h + 22, "–", size=52, col=NEG, anchor="end")

# ----------------------------------------------------------------- 1. titre
def sc_titre(c, pi, t):
    for i in range(14):
        a = 2 * math.pi * (i / 14.0 + 0.12 * t)
        r = 300 + 120 * math.sin(2.1 * a + i)
        x, y = CX + r * math.cos(a) * 2.1, 600 + r * math.sin(a) * 0.72
        if 60 < x < W - 60 and 180 < y < H - 90:
            c.charge(x, y, 1 if i % 2 else -1, r=17, op=0.16)
    c.txt(CX, 430, "Champ électrique", size=132, col=INK, bold=True)
    c.rect(CX - 300, 470, 600, 5, fill=OR)
    c.txt(CX, 540, "Physique S6 · École européenne Jacques Delors", size=36, col=MUT)
    if pi >= 1:
        c.txt(CX, 680, "Comment deux objets peuvent-ils s’attirer", size=46, col=INK)
        c.txt(CX, 740, "sans se toucher ?", size=46, col=OR, bold=True)
    if pi >= 2:
        c.txt(CX, 860, "la charge  ·  la loi de Coulomb  ·  le champ  ·  les lignes  ·  le potentiel",
              size=30, col=MUT)

# ----------------------------------------------------------------- 2. question
def sc_question(c, pi, t):
    head(c, "Agir à distance", 2, 12)
    if pi <= 1:
        soustitre(c, "Une règle frottée attire des bouts de papier")
        rx, ry = CX, 360
        c.rect(rx - 420, ry - 44, 840, 88, fill="#ffffff", col=INK, sw=4, rx=10)
        c.txt(rx, ry - 74, "règle en plastique frottée", size=30, col=MUT)
        for i in range(9):
            c.txt(rx - 370 + i * 92, ry + 16, "–", size=46, col=NEG)
        base = 840
        for i in range(8):
            x = CX - 340 + i * 97
            ph = pingpong((t + i * 0.13) % 1.0)
            y = base - 330 * ph * (0.55 + 0.45 * math.sin(i * 2.0) ** 2)
            c.rect(x - 34, y - 24, 68, 48, fill="#ffffff", col=SOFT, sw=3, rx=4)
            c.txt(x, y + 12, "+", size=34, col=POS, op=0.85)
        c.line(220, base + 30, W - 220, base + 30, col=SOFT, sw=3)
        c.txt(CX, base + 72, "bouts de papier", size=26, col=MUT)
        if pi >= 1:
            c.txt(CX, 300, "aucun contact, aucun fil, aucun souffle d’air", size=32, col=OR)
    else:
        soustitre(c, "La réponse des physiciens, en deux temps")
        for i, (num, titre, sub) in enumerate([
                ("1", "La charge électrique", "mesure à quel point un objet est électrisé"),
                ("2", "Le champ électrique", "une charge transforme l’espace autour d’elle")]):
            y = 300 + i * 205
            actif = (pi == 3 and i == 0) or (pi >= 4 and i == 1)
            col = OR if actif else PALE
            c.card(300, y, 1320, 165, col=col, sw=5 if actif else 3)
            c.circle(390, y + 82, 42, col=col, sw=5, fill="#ffffff")
            c.txt(390, y + 97, num, size=48, col=OR if actif else SOFT, bold=True)
            c.txt(475, y + 72, titre, size=42, col=INK, anchor="start", bold=True)
            c.txt(475, y + 122, sub, size=30, col=MUT, anchor="start")
        if pi >= 4:
            x0, y0 = 700, 870
            c.charge(x0, y0, +1, r=38)
            c.txt(x0, y0 + 78, "Q", size=32, col=POS, it=True)
            for k in range(3):
                u = (t + k / 3.0) % 1.0
                c.circle(x0, y0, 54 + u * 150, col=POS, sw=3, op=0.45 * (1 - u))
            c.charge(x0 + 420, y0, +1, r=28, col=ACC)
            c.txt(x0 + 420, y0 + 72, "q", size=32, col=ACC, it=True)
            c.arrow(x0 + 462, y0, x0 + 600, y0, col=ACC, sw=7, head=22)
            c.txt(x0 + 540, y0 - 40, "force", size=28, col=ACC)

# ----------------------------------------------------------------- 3. charge
def sc_charge(c, pi, t):
    head(c, "La charge électrique", 3, 12)
    if pi <= 1:
        soustitre(c, "Tout part de l’atome")
        cx, cy = CX - 120, 580
        c.circle(cx, cy, 58, col=POS, sw=4, fill="#fdf0ee")
        c.txt(cx, cy + 14, "+3", size=40, col=POS, bold=True)
        c.txt(cx, cy + 110, "noyau : protons +", size=26, col=MUT)
        orx, ory = 250, 165
        c.ell(cx, cy, orx, ory, col=SOFT, sw=2.5)
        for i in range(3):
            a = 2 * math.pi * (t + i / 3.0)
            x, y = cx + orx * math.cos(a), cy + ory * math.sin(a)
            c.dot(x, y, 22, col=NEG)
            c.txt(x, y + 11, "–", size=32, col="#ffffff")
        c.txt(cx + 430, cy - 40, "3 protons  +", size=34, col=POS, anchor="start")
        c.txt(cx + 430, cy + 10, "3 électrons  –", size=34, col=NEG, anchor="start")
        c.line(cx + 430, cy + 32, cx + 700, cy + 32, col=INK, sw=3)
        c.txt(cx + 430, cy + 86, "total : neutre", size=36, col=INK, anchor="start", bold=True)
        if pi >= 1:
            c.txt(CX, 930, "les charges se compensent exactement", size=32, col=MUT)
    elif pi <= 4:
        soustitre(c, "Le frottement ne crée rien : il transfère des électrons")
        ax, bx, y = 560, 1360, 560
        c.rect(ax - 190, y - 110, 380, 220, fill="#ffffff", col=INK, sw=3, rx=12)
        c.txt(ax, y - 140, "chiffon", size=30, col=MUT)
        c.rect(bx - 190, y - 110, 380, 220, fill="#ffffff", col=INK, sw=3, rx=12)
        c.txt(bx, y - 140, "règle", size=30, col=MUT)
        n = 5
        for i in range(n):
            ph = (t + i / float(n)) % 1.0
            x = ax + (bx - ax) * ease(ph)
            yy = y - 150 - 110 * math.sin(math.pi * ph)
            c.dot(x, yy, 17, col=NEG, op=0.95)
            c.txt(x, yy + 8, "–", size=24, col="#ffffff")
        c.arrow(ax + 210, y + 150, bx - 210, y + 150, col=SOFT, sw=4, head=18)
        c.txt(CX, y + 195, "les électrons passent d’un objet à l’autre", size=28, col=MUT)
        if pi >= 3:
            c.txt(ax, y + 30, "+", size=78, col=POS, bold=True)
            c.txt(bx, y + 30, "–", size=86, col=NEG, bold=True)
            c.txt(ax, y + 100, "a perdu des électrons", size=26, col=MUT)
            c.txt(bx, y + 100, "en a gagné autant", size=26, col=MUT)
        if pi >= 4:
            c.card(430, 860, 1060, 110, col=OR)
            c.txt(CX, 930, "ce qui est positif quelque part manque ailleurs",
                  size=40, col=INK, bold=True)
    elif pi == 5:
        soustitre(c, "L’unité : le coulomb")
        c.txt(CX, 400, "la charge se note  q  et se mesure en coulombs (C)", size=40, col=INK)
        c.card(460, 470, 1000, 150, col=OR)
        formule(c, "e = 1,60 × 10⁻¹⁹ C", y=565, size=58)
        c.txt(CX, 670, "la charge élémentaire : celle d’un électron, la plus petite qui existe",
              size=30, col=MUT)
        formule(c, "q = n × e", y=790, size=50, sub="toute charge est un multiple entier de e")
    else:
        soustitre(c, "Des ordres de grandeur")
        data = [("un électron", "1,6 × 10⁻¹⁹ C", 0.06), ("un ballon frotté", "10⁻⁸ C", 0.33),
                ("une ampoule en 1 s", "0,5 C", 0.66), ("un éclair", "1 à 20 C", 1.0)]
        for i, (nom, val, f) in enumerate(data):
            y = 360 + i * 130
            c.txt(400, y + 12, nom, size=34, col=INK, anchor="end")
            c.rect(440, y - 26, 900 * f, 52, fill=OR, rx=6, op=0.28 + 0.2 * i)
            c.txt(460, y + 12, val, size=32, col=INK, anchor="start", it=True)
        c.txt(CX, 930, "en électrostatique on travaille en nC et en µC : il faut convertir",
              size=30, col=MUT)

# ----------------------------------------------------------------- 4. règles
def sc_regles(c, pi, t):
    head(c, "Les deux règles d’or", 4, 12)
    if pi <= 3:
        soustitre(c, "Mêmes signes : répulsion   ·   signes opposés : attraction")
        d = 120 * pingpong(t)
        y = 520
        c.card(170, 330, 760, 380, col=PALE, sw=3, fill=BG)
        c.card(1000, 330, 760, 380, col=PALE, sw=3, fill=BG)
        c.txt(550, 390, "mêmes signes", size=34, col=MUT)
        c.txt(1380, 390, "signes opposés", size=34, col=MUT)
        # répulsion
        x0 = 550
        c.charge(x0 - 120 - d, y, +1, r=42); c.charge(x0 + 120 + d, y, +1, r=42)
        c.arrow(x0 - 175 - d, y, x0 - 300 - d, y, col=POS, sw=6)
        c.arrow(x0 + 175 + d, y, x0 + 300 + d, y, col=POS, sw=6)
        c.txt(x0, y + 160, "se repoussent", size=38, col=POS, bold=True)
        # attraction
        x1 = 1380
        c.charge(x1 - 180 + d, y, +1, r=42); c.charge(x1 + 180 - d, y, -1, r=42)
        c.arrow(x1 - 125 + d, y, x1 - 10 + d, y, col=NEG, sw=6)
        c.arrow(x1 + 125 - d, y, x1 + 10 - d, y, col=NEG, sw=6)
        c.txt(x1, y + 160, "s’attirent", size=38, col=NEG, bold=True)
        if pi >= 2:
            c.card(360, 800, 1200, 170, col=OR)
            c.txt(CX, 862, "les deux forces ont toujours la même valeur", size=42, col=INK, bold=True)
            c.txt(CX, 920, "même si une charge est mille fois plus grande que l’autre",
                  size=30, col=MUT)
        if pi >= 3:
            c.txt(CX, 300, "comme la pomme et la Terre", size=30, col=MUT)
    else:
        soustitre(c, "Pourquoi un objet chargé attire-t-il un objet neutre ?")
        rx, ry = 430, 560
        c.rect(rx - 60, ry - 190, 120, 380, fill="#ffffff", col=INK, sw=3, rx=8)
        for i in range(6):
            c.txt(rx, ry - 150 + i * 64, "–", size=40, col=NEG)
        c.txt(rx, ry - 230, "règle négative", size=30, col=MUT)
        px, py = 1180, 560
        c.rect(px - 230, py - 150, 460, 300, fill="#ffffff", col=SOFT, sw=3, rx=10)
        c.txt(px, py + 200, "papier neutre", size=30, col=MUT)
        sep = 26 * (seg(t, 0.1, 0.6) if pi >= 5 else 0)
        for i in range(3):
            for j in range(2):
                x = px - 150 + i * 150
                y = py - 70 + j * 140
                c.charge(x - 34 - sep, y, +1, r=24)
                c.charge(x + 34 + sep, y, -1, r=24)
        if pi == 4:
            c.txt(px, py - 210, "ni positif, ni négatif", size=32, col=MUT)
        if pi >= 5:
            c.txt(px, py - 210, "les charges se déplacent un peu : le papier se polarise",
                  size=30, col=MUT)
        if pi >= 6:
            c.arrow(px - 250, py + 230, rx + 90, py + 230, col=ACC, sw=6)
            c.txt((px + rx) / 2, py + 285, "les  +  sont plus proches, et le 1/r² les avantage",
                  size=32, col=ACC)
        if pi >= 7:
            c.card(360, 880, 1200, 110, col=OR)
            c.txt(CX, 950, "un objet chargé attire toujours un objet neutre",
                  size=42, col=INK, bold=True)

# ----------------------------------------------------------------- 5. Coulomb
def sc_coulomb(c, pi, t):
    head(c, "La loi de Coulomb", 5, 12)
    if pi <= 1:
        soustitre(c, "La valeur de la force entre deux charges")
        c.card(380, 320, 1160, 200, col=OR)
        formule(c, "F = k · |Q| · |q| / r²", y=445, size=74)
        if pi >= 1:
            items = [("Q, q", "les deux charges, en coulombs", POS),
                     ("r", "la distance entre elles, en mètres — au carré", NEG),
                     ("k", "une constante : 9,0 × 10⁹ N m² C⁻²", ACC)]
            for i, (s, d, col) in enumerate(items):
                y = 620 + i * 100
                c.txt(620, y, s, size=46, col=col, it=True, anchor="end")
                c.txt(680, y, d, size=34, col=INK, anchor="start")
    elif pi <= 2:
        soustitre(c, "Le point important : la distance est au carré")
        y = 420
        c.charge(430, y, +1, r=44)
        ph = pingpong(t)
        x = 760 + 700 * ph
        r = (x - 430) / 330.0
        c.charge(x, y, +1, r=36)
        F = 1.0 / (r * r)
        c.arrow(x + 50, y, x + 50 + 40 + 300 * clamp(F, 0, 1.2), y, col=POS, sw=8, head=26)
        c.line(430, y + 140, x, y + 140, col=SOFT, sw=3)
        c.txt((430 + x) / 2, y + 185, "r", size=38, col=MUT, it=True)
        # courbe 1/r²
        gx, gy, gw, gh = 1200, 640, 520, 260
        c.line(gx, gy + gh, gx + gw, gy + gh, col=SOFT, sw=3)
        c.line(gx, gy, gx, gy + gh, col=SOFT, sw=3)
        pts = []
        for i in range(61):
            rr = 1.0 + 2.0 * i / 60.0
            pts.append("%s%.1f %.1f" % ("M" if i == 0 else "L",
                                        gx + gw * (rr - 1) / 2.0, gy + gh - gh * min(1.0, 1.0 / rr**2)))
        c.path(" ".join(pts), col=ACC, sw=4)
        c.dot(gx + gw * (r - 1) / 2.0, gy + gh - gh * min(1.0, 1.0 / r**2), 11, col=ACC)
        c.txt(gx + gw / 2, gy - 26, "F  en fonction de  r", size=28, col=MUT)
        c.txt(320, 700, "la force s’effondre", size=34, col=MUT, anchor="start")
        c.txt(320, 748, "quand on s’éloigne", size=34, col=MUT, anchor="start")
        formule(c, "F  ∝  1 / r²", y=850, size=52, col=ACC)
    elif pi <= 4:
        soustitre(c, "On double la distance, la force est divisée par quatre")
        data = [("1 cm", 1.0, "90 N"), ("2 cm", 0.25, "22,5 N"), ("3 cm", 1 / 9.0, "10 N"),
                ("10 cm", 0.01, "0,9 N")]
        for i, (d, f, v) in enumerate(data):
            x = 370 + i * 400
            hbar = 420 * f
            c.rect(x - 70, 760 - hbar, 140, hbar, fill=POS, rx=6, op=0.85)
            c.txt(x, 810, d, size=36, col=INK)
            c.txt(x, 730 - hbar, v, size=32, col=POS, bold=True)
        c.line(220, 762, 1700, 762, col=SOFT, sw=3)
        c.txt(CX, 900, "deux charges de 1 µC : 90 N à 1 cm, c’est le poids d’un sac de 9 kg",
              size=32, col=MUT)
        if pi >= 4:
            c.txt(CX, 960, "×2 sur la distance → ÷4 sur la force    ·    ×3 → ÷9",
                  size=34, col=OR, bold=True)
    else:
        soustitre(c, "Pourquoi un carré ? L’image de l’ampoule")
        cx, cy = CX, 580
        c.dot(cx, cy, 26, col=OR)
        for k, (rr, lab) in enumerate([(150, "r"), (300, "2r")]):
            c.circle(cx, cy, rr, col=SOFT, sw=3, dash="8 10")
            c.txt(cx + rr + 50, cy - 10, lab, size=36, col=MUT, it=True)
        for i in range(16):
            a = 2 * math.pi * i / 16.0
            L = 150 + 150 * seg(t, 0.15, 0.85)
            c.line(cx + 30 * math.cos(a), cy + 30 * math.sin(a),
                   cx + L * math.cos(a), cy + L * math.sin(a), col=OR, sw=3, op=0.55)
        c.txt(CX, 930, "deux fois plus loin, la même lumière couvre quatre fois plus de surface",
              size=34, col=MUT)

# ----------------------------------------------------------------- 6. vecteur
def sc_vecteur(c, pi, t):
    head(c, "Vecteurs et addition", 6, 12)
    if pi <= 3:
        soustitre(c, "Une flèche porte une valeur et une orientation")
        x0, y0 = 480, 620
        c.arrow(x0, y0, x0 + 520, y0 - 260, col=POS, sw=8, head=30)
        c.dot(x0, y0, 12, col=INK)
        c.txt(x0 - 30, y0 + 40, "origine", size=28, col=MUT, anchor="end")
        c.txt(x0 + 170, y0 - 180, "longueur = valeur", size=28, col=MUT, anchor="start")
        c.txt(x0 + 560, y0 - 300, "sens", size=28, col=POS, anchor="start")
        c.txt(x0 + 330, y0 + 60, "direction : la droite qui la porte", size=28, col=MUT)
        if pi >= 2:
            c.card(1180, 400, 560, 300, col=PALE, sw=3)
            c.txt(1460, 490, "F", size=66, col=INK, it=True)
            c.line(1436, 432, 1482, 432, col=INK, sw=4)
            c.path("M1492 432 l-16 -9 l0 18 z", col=INK, fill=INK, sw=1)
            c.txt(1460, 530, "le vecteur : une flèche", size=28, col=MUT)
            c.txt(1460, 620, "F", size=64, col=INK, it=True)
            c.txt(1460, 670, "la norme : un nombre positif", size=28, col=MUT)
        if pi >= 3:
            c.card(380, 860, 1160, 110, col=OR)
            c.txt(CX, 930, "une norme n’est jamais négative", size=42, col=INK, bold=True)
    else:
        soustitre(c, "Additionner deux vecteurs : bout à bout")
        ox, oy = 560, 760
        v1 = (420, -120)
        v2 = (180, -330)
        a = seg(t, 0.05, 0.40)
        b = seg(t, 0.45, 0.72)
        s = seg(t, 0.78, 0.97)
        c.dot(ox, oy, 10, col=INK)
        if a > 0:
            c.arrow(ox, oy, ox + v1[0] * a, oy + v1[1] * a, col=POS, sw=7, head=26)
            c.txt(ox + v1[0] * 0.5, oy + v1[1] * 0.5 + 46, "E₁", size=38, col=POS, it=True)
        if b > 0:
            c.arrow(ox + v1[0], oy + v1[1], ox + v1[0] + v2[0] * b, oy + v1[1] + v2[1] * b,
                    col=NEG, sw=7, head=26)
            c.txt(ox + v1[0] + v2[0] * 0.5 + 56, oy + v1[1] + v2[1] * 0.5, "E₂",
                  size=38, col=NEG, it=True)
        if s > 0:
            c.arrow(ox, oy, ox + (v1[0] + v2[0]) * s, oy + (v1[1] + v2[1]) * s,
                    col=INK, sw=8, head=30)
            c.txt(ox + (v1[0] + v2[0]) * 0.55 - 70, oy + (v1[1] + v2[1]) * 0.55 - 30,
                  "E", size=44, col=INK, it=True)
        if s > 0:
            c.line(ox, oy, ox + v2[0], oy + v2[1], col=SOFT, sw=2, dash="7 9")
            c.line(ox + v2[0], oy + v2[1], ox + v1[0] + v2[0], oy + v1[1] + v2[1],
                   col=SOFT, sw=2, dash="7 9")
        if pi >= 5:
            c.card(1280, 330, 480, 330, col=PALE, sw=3)
            c.txt(1520, 400, "par le calcul", size=32, col=MUT)
            c.txt(1520, 470, "x = x₁ + x₂", size=38, col=INK, it=True)
            c.txt(1520, 525, "y = y₁ + y₂", size=38, col=INK, it=True)
            c.txt(1520, 600, "‖E‖ = √(x² + y²)", size=36, col=ACC, it=True)
        if pi >= 6:
            c.card(380, 880, 1160, 110, col=OR)
            c.txt(CX, 950, "3 et 4 perpendiculaires ne font pas 7, mais 5",
                  size=42, col=INK, bold=True)

# ----------------------------------------------------------------- 7. champ
def sc_champ(c, pi, t):
    head(c, "Le champ électrique", 7, 12)
    if pi <= 2:
        soustitre(c, "La force dépend de la charge d’essai… pas le rapport")
        qs = [(1.0, "q"), (2.0, "2q"), (-1.0, "–q")]
        k = int(t * 3) % 3
        for i, (f, lab) in enumerate(qs):
            x = 440 + i * 520
            actif = (i == k)
            c.rect(x - 220, 300, 440, 430, fill="#ffffff" if actif else BG,
                   col=OR if actif else PALE, sw=4 if actif else 2, rx=12)
            c.charge(x, 470, 1 if f > 0 else -1, r=26 + 12 * abs(f))
            c.txt(x, 560, lab, size=38, col=INK, it=True)
            c.arrow(x, 470, x + 90 * f, 470, col=POS if f > 0 else NEG, sw=7, head=22)
            if pi >= 2:
                c.txt(x, 680, "F / |q|  =  E", size=32, col=ACC, it=True)
        if pi >= 1:
            c.txt(CX, 790, "trois charges différentes au même endroit : la force change",
                  size=34, col=MUT)
        if pi >= 2:
            c.txt(CX, 850, "mais le rapport force divisée par charge, lui, ne change pas",
                  size=34, col=ACC)
    elif pi <= 4:
        soustitre(c, "La définition du champ")
        c.card(380, 300, 1160, 180, col=OR)
        formule(c, "E = F / |q|", y=415, size=72)
        c.txt(CX, 530, "le champ, c’est la force par unité de charge", size=36, col=MUT)
        if pi >= 4:
            c.card(380, 600, 1160, 180, col=PALE, sw=3)
            formule(c, "F = q · E", y=715, size=66)
            flip = 1 if (t < 0.5) else -1
            y = 880
            c.charge(700, y, flip, r=34)
            c.arrow(760, y, 760 + 220 * flip, y, col=POS if flip > 0 else NEG, sw=8, head=26)
            c.txt(1180, y + 12, "q > 0 : même sens que E" if flip > 0
                  else "q < 0 : sens opposé à E", size=34, col=INK, anchor="start")
    elif pi <= 6:
        soustitre(c, "L’analogie la plus utile : la pesanteur")
        for i, (titre, l1, l2, col) in enumerate([
                ("Gravitation", "une masse M crée un champ  g", "un objet m subit  P = m · g", MUT),
                ("Électricité", "une charge Q crée un champ  E", "une charge q subit  F = q · E", POS)]):
            x = 500 + i * 920
            c.card(x - 400, 300, 800, 420, col=PALE if i == 0 else OR, sw=3)
            c.txt(x, 370, titre, size=44, col=INK, bold=True)
            if i == 0:
                c.circle(x, 480, 46, col=MUT, sw=4, fill="#efe7d8")
                for k in range(5):
                    xx = x - 160 + k * 80
                    c.arrow(xx, 540, xx, 620, col=MUT, sw=4, head=16, op=0.8)
            else:
                c.charge(x, 480, +1, r=40)
                for k in range(8):
                    a = 2 * math.pi * k / 8.0
                    c.arrow(x + 58 * math.cos(a), 480 + 58 * math.sin(a),
                            x + 128 * math.cos(a), 480 + 128 * math.sin(a), col=POS, sw=4, head=14)
            c.txt(x, 670, l1, size=30, col=MUT, it=True)
            c.txt(x, 705, l2, size=30, col=INK, it=True)
        c.txt(CX, 800, "la charge joue exactement le rôle de la masse", size=36, col=INK)
    else:
        soustitre(c, "Le champ existe même si on ne pose rien dedans")
        x0 = CX - 260
        c.charge(x0, 560, +1, r=48)
        c.txt(x0, 660, "Q", size=40, col=POS, it=True)
        for k in range(16):
            a = 2 * math.pi * k / 16.0
            c.arrow(x0 + 66 * math.cos(a), 560 + 66 * math.sin(a),
                    x0 + 176 * math.cos(a), 560 + 176 * math.sin(a), col=POS, sw=4, head=15, op=0.85)
        op = 0.15 + 0.85 * pingpong(t)
        c.charge(x0 + 560, 560, +1, r=30, col=ACC, op=op)
        c.arrow(x0 + 600, 560, x0 + 740, 560, col=ACC, sw=7, head=22, op=op)
        c.txt(x0 + 620, 650, "q : on la met, on l’enlève…", size=30, col=ACC, op=op)
        c.card(380, 840, 1160, 110, col=OR)
        c.txt(CX, 910, "le champ, lui, ne bouge pas : q ne fait que le révéler",
              size=40, col=INK, bold=True)

# ----------------------------------------------------------------- 8. lignes
def _dip(c, t, montrer_points=True):
    xa, xb, y = 640, 1280, 540
    c.charge(xa, y, +1, r=40); c.charge(xb, y, -1, r=40)
    for k in range(-4, 5):
        if k == 0:
            c.path("M%d %d L%d %d" % (xa + 44, y, xb - 44, y), col=SOFT, sw=3)
            continue
        bulge = 70 * k
        d = "M%d %d Q%d %d %d %d" % (xa + 40, y, (xa + xb) / 2, y + bulge * 1.5, xb - 40, y)
        c.path(d, col=SOFT, sw=3)
    if montrer_points:
        for k in range(-4, 5):
            for j in range(3):
                u = (t + j / 3.0 + k * 0.067) % 1.0
                bulge = 70 * k
                x = xa + 40 + (xb - xa - 80) * u
                yy = y + (0 if k == 0 else bulge * 1.5 * 2 * u * (1 - u))
                c.dot(x, yy, 9, col=OR)
    return xa, xb, y

def sc_lignes(c, pi, t):
    head(c, "Les lignes de champ", 8, 12)
    soustitre(c, "Des courbes qui suivent les flèches")
    xa, xb, y = _dip(c, t)
    regles = ["E est tangent à la ligne",
              "elles sortent du  +  et entrent dans le  –",
              "elles ne se croisent jamais",
              "serrées = champ intense",
              "perpendiculaires à un conducteur"]
    if 2 <= pi <= 6:
        n = min(pi - 1, 5)
        for i in range(n):
            c.dot(360, 800 + i * 52 - 10, 7, col=OR if i == n - 1 else SOFT)
            c.txt(390, 800 + i * 52, regles[i], size=30,
                  col=INK if i == n - 1 else MUT, anchor="start")
    if pi == 1:
        c.txt(CX, 830, "cinq règles de lecture, et elles tombent toutes en contrôle",
              size=34, col=MUT)
    if pi >= 6:
        c.card(1120, 790, 660, 140, col=OR)
        c.txt(1450, 850, "ces points ne sont pas", size=32, col=INK)
        c.txt(1450, 895, "des charges qui se déplacent", size=32, col=INK, bold=True)

# ----------------------------------------------------------------- 9. superposition
def sc_super(c, pi, t):
    head(c, "Superposition", 9, 12)
    soustitre(c, "Chaque charge crée son champ comme si les autres n’existaient pas")
    xa, xb, y = 520, 1400, 880
    c.charge(xa, y, +1, r=42); c.charge(xb, y, +1, r=42)
    c.txt(xa, y + 90, "Q₁", size=34, col=POS, it=True)
    c.txt(xb, y + 90, "Q₂", size=34, col=POS, it=True)
    mx = xa + 150 + (xb - xa - 300) * pingpong(t)
    my = 580
    c.dot(mx, my, 11, col=INK)
    c.txt(mx, my - 34, "M", size=36, col=INK, it=True)
    def champ(xs):
        dx, dy = mx - xs, my - y
        d = math.hypot(dx, dy)
        g = min(255.0, 7.0e7 / (d * d))
        return dx / d * g, dy / d * g
    e1 = champ(xa); e2 = champ(xb)
    if pi >= 1:
        c.arrow(mx, my, mx + e1[0], my + e1[1], col=POS, sw=6, head=22)
        c.arrow(mx, my, mx + e2[0], my + e2[1], col=NEG, sw=6, head=22)
        c.txt(mx + e1[0] - 40, my + e1[1] - 16, "E₁", size=32, col=POS, it=True)
        c.txt(mx + e2[0] + 40, my + e2[1] - 16, "E₂", size=32, col=NEG, it=True)
    if pi >= 2:
        sx, sy = e1[0] + e2[0], e1[1] + e2[1]
        c.line(mx + e1[0], my + e1[1], mx + sx, my + sy, col=SOFT, sw=2, dash="7 9")
        c.line(mx + e2[0], my + e2[1], mx + sx, my + sy, col=SOFT, sw=2, dash="7 9")
        c.arrow(mx, my, mx + sx, my + sy, col=INK, sw=8, head=28)
        c.txt(mx + sx + 40, my + sy + 10, "E", size=40, col=INK, it=True)
    if pi >= 3:
        c.txt(300, 700, "projeter, additionner,", size=32, col=ACC, anchor="start")
        c.txt(300, 744, "puis Pythagore", size=32, col=ACC, anchor="start")
        formule(c, "E = Σ Eᵢ", y=990, size=48)
    if pi >= 4:
        c.card(1180, 660, 600, 140, col=OR)
        c.txt(1480, 715, "le point nul : l’endroit où", size=30, col=INK)
        c.txt(1480, 760, "les deux champs s’annulent", size=30, col=INK, bold=True)

# ----------------------------------------------------------------- 10. potentiel
def sc_potentiel(c, pi, t):
    head(c, "Potentiel, tension, plaques", 10, 12)
    if pi <= 4:
        soustitre(c, "L’analogie du relief")
        ox, oy, w, h = 300, 760, 700, 380
        c.path("M%d %d Q%d %d %d %d" % (ox, oy, ox + w / 2, oy - h * 1.5, ox + w, oy),
               col=MUT, sw=4)
        for i in range(1, 5):
            yy = oy - h * i / 5.0
            dx = w / 2.0 * math.sqrt(1 - i / 5.0)
            c.line(ox + w / 2 - dx, yy, ox + w / 2 + dx, yy, col=SOFT, sw=2, dash="8 8")
        c.txt(ox + w / 2, oy + 54, "altitude = potentiel  V", size=32, col=MUT)
        bx = 1150
        plaques(c, bx, 300, 560, 420)
        for i in range(5):
            xx = bx + 60 + i * 110
            c.line(xx, 310, xx, 720, col=SOFT, sw=2, dash="8 8")
        for j in range(3):
            yy = 380 + j * 130
            c.arrow(bx + 30, yy, bx + 530, yy, col=POS, sw=5, head=20)
        c.txt(bx + 280, 790, "équipotentielles = courbes de niveau", size=30, col=MUT)
        if pi >= 1:
            c.txt(CX, 880, "V : l’altitude électrique d’un point    ·    U = V(A) – V(B) : la dénivelée",
                  size=34, col=INK)
        if pi >= 3:
            c.txt(CX, 935, "le champ est perpendiculaire aux équipotentielles", size=32, col=ACC)
        if pi >= 4:
            c.txt(CX, 985, "et il pointe vers les potentiels décroissants : ça descend",
                  size=32, col=ACC)
    elif pi <= 6:
        soustitre(c, "Entre deux plaques : un champ uniforme")
        U = 1.0 if t < 0.5 else 2.0
        bx, by, bw, bh = 520, 320, 880, 400
        plaques(c, bx, by, bw, bh)
        n = 5
        for j in range(n):
            yy = by + 50 + j * (bh - 80) / (n - 1.0)
            c.arrow(bx + 40, yy, bx + bw - 40, yy, col=POS, sw=3 + 3 * (U - 1), head=18 + 8 * (U - 1))
        c.line(bx + bw + 60, by, bx + bw + 60, by + bh, col=MUT, sw=3)
        c.txt(bx + bw + 110, by + bh / 2, "d", size=40, col=MUT, it=True, anchor="start")
        c.txt(bx + bw / 2, by - 40, "U = %d V" % int(200 * U), size=42, col=INK, bold=True)
        c.card(560, 790, 800, 150, col=OR)
        formule(c, "E = U / d", y=880, size=62)
        if pi >= 6:
            c.txt(1430, 850, "double U → E double", size=30, col=INK, anchor="start")
            c.txt(1430, 896, "rapproche d → E augmente", size=30, col=INK, anchor="start")
    else:
        soustitre(c, "Travail et énergie")
        c.card(380, 320, 1160, 170, col=OR)
        formule(c, "W = q · ΔV", y=430, size=66)
        c.txt(CX, 560, "le long d’une équipotentielle, ΔV = 0, donc W = 0", size=40, col=INK)
        ox, oy, w = 420, 820, 1080
        for i in range(4):
            yy = oy - i * 70
            c.line(ox, yy, ox + w, yy, col=SOFT, sw=2, dash="8 8")
        c.path("M%d %d Q%d %d %d %d" % (ox + 60, oy - 10, ox + w / 2, oy - 40, ox + w - 60, oy - 10),
               col=ACC, sw=5)
        px = ox + 60 + (w - 120) * pingpong(t)
        c.dot(px, oy - 10 - 30 * 4 * ((px - ox - 60) / (w - 120)) * (1 - (px - ox - 60) / (w - 120)),
              14, col=ACC)
        c.txt(CX, oy + 70, "marcher à flanc de colline ne coûte rien", size=32, col=MUT)

# ----------------------------------------------------------------- 11. application
def sc_appli(c, pi, t):
    head(c, "Ça sert vraiment", 11, 12)
    soustitre(c, "L’imprimante à jet d’encre")
    bx, by, bw, bh = 620, 380, 560, 300
    c.rect(300, 480, 180, 100, fill="#ffffff", col=INK, sw=3, rx=8)
    c.txt(390, 540, "canon", size=28, col=MUT)
    c.rect(500, 495, 70, 70, fill="#ffffff", col=ACC, sw=3, rx=6)
    c.txt(535, 460, "charge", size=24, col=ACC)
    plaques(c, bx, by, bw, bh - 60)
    c.rect(1420, 330, 24, 520, fill=PALE)
    c.txt(1432, 890, "papier", size=28, col=MUT)
    charges = [0.0, 0.45, -0.5, 0.9, 0.0, -0.9]
    for i, q in enumerate(charges):
        u = (t + i / float(len(charges))) % 1.0
        x = 560 + (1420 - 560) * u
        dev = 0.0
        if x > bx:
            s = min(1.0, (x - bx) / float(bw))
            dev = -q * 90 * s * s
            if x > bx + bw:
                dev = -q * 90 * (1 + 1.1 * (x - bx - bw) / float(1420 - bx - bw))
        c.dot(x, 530 + dev, 11, col=NEG if q > 0 else (POS if q < 0 else SOFT))
    if pi >= 3:
        c.card(300, 790, 900, 150, col=OR)
        c.txt(750, 850, "le champ ne change pas :", size=34, col=INK)
        c.txt(750, 900, "c’est la charge qui décide de la déviation", size=34, col=INK, bold=True)
        formule(c, "F = q · E", y=990, size=44)
    if pi >= 4:
        c.txt(1600, 540, "non chargée :", size=28, col=MUT)
        c.txt(1600, 578, "tout droit", size=28, col=MUT)
    if pi >= 5:
        c.txt(CX, 300, "photocopieuse · peinture · dépoussiéreur · paratonnerre : même principe",
              size=32, col=ACC)

# ----------------------------------------------------------------- 12. final
def sc_final(c, pi, t):
    head(c, "Ce qu’il faut retenir", 12, 12)
    soustitre(c, "Tout le chapitre tient dans cinq relations", y=210)
    forms = [("F = k · |Q| · |q| / r²", "la loi de Coulomb"),
             ("E = F / |q|          F = q · E", "le champ : force par unité de charge"),
             ("E = k · |Q| / r²", "le champ d’une charge ponctuelle"),
             ("E = U / d", "le champ uniforme entre deux plaques"),
             ("W = q · ΔV", "l’énergie échangée")]
    for i, (f, d) in enumerate(forms):
        if pi >= 1 and i > pi - 1:
            break
        y = 320 + i * 125
        actif = (i == pi - 1)
        c.card(330, y, 1260, 105, col=OR if actif else PALE, sw=4 if actif else 2)
        c.txt(640, y + 68, f, size=44, col=INK, it=True)
        c.txt(1180, y + 66, d, size=28, col=MUT)
    if pi >= 6:
        c.txt(CX, 1010, "un schéma propre avant chaque calcul, et tout devient faisable",
              size=36, col=ACC)

SCENES = {"titre": sc_titre, "question": sc_question, "charge": sc_charge, "regles": sc_regles,
          "coulomb": sc_coulomb, "vecteur": sc_vecteur, "champ": sc_champ, "lignes": sc_lignes,
          "superposition": sc_super, "potentiel": sc_potentiel, "application": sc_appli,
          "final": sc_final}
