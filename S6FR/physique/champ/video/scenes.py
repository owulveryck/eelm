# -*- coding: utf-8 -*-
"""Les 25 plans du chapitre « Champ électrique ».
Les dessins de base sont dans dessins.py ; le texte lu est dans script.py."""
import math
import canvas, tex
import dessins, script
from canvas import (C, W, H, INK, MUT, POS, NEG, ACC, SOFT, OR, PALE, BG,
                    ease, pingpong, clamp, seg, formule)

CX = W / 2.0

# Le numéro du plan et leur nombre total se lisent dans script.py : insérer une
# scène au milieu ne demande donc de renuméroter nulle part.
RANG = {sid: i + 1 for i, (sid, _, _) in enumerate(script.SCENES)}
NSC = len(script.SCENES)

def head(c, titre, sid):
    canvas.head(c, titre, RANG[sid], NSC)

def sous(c, s, y=200, size=40, col=INK, op=None):
    c.txt(CX, y, s, size=size, col=col, op=op)

def reuse(fn, c, pi, t, titre, idx):
    """réutilise un dessin de la v1 puis réécrit le bandeau"""
    fn(c, pi, t)
    head(c, titre, idx)

# ------------------------------------------------------------------ l'exemple type
def exemple(c, idx, num, titre, enonce, lignes, upto, resultat=None, comm=None,
            fig=None, t=0.0):
    """Mise en page d'un exemple résolu.

    fig : dessin de la situation, appelé fig(c, upto, t) et logé à gauche
    (x 140..840, y 320..940) ; le calcul passe alors dans la colonne de droite.
    Sans dessin, le calcul occupe toute la largeur comme avant.
    """
    head(c, "Exemple %d — %s" % (num, titre), idx)
    c.card(220, 160, 1480, 120, col=PALE, sw=3)
    for i, l in enumerate(enonce[:2]):
        c.txt(CX, 205 + i * 44, l, size=31, col=INK)
    if fig:
        fig(c, upto, t)
        xc, pt0, pt1, larg = 1290, 36, 40, 840
        y, pas = 400, 104
    else:
        xc, pt0, pt1, larg = CX, 40, 46, 1560
        y, pas = 390, 112
    for i, l in enumerate(lignes):
        if i >= upto:
            break
        dernier = (i == upto - 1)
        tex.put(c, l, xc, y, pt=pt1 if dernier else pt0,
                col=INK if dernier else MUT, maxw=larg)
        y += pas
    if resultat and upto >= len(lignes):
        if fig:
            c.card(890, 800, 800, 112, col=OR)
            tex.put(c, resultat, xc, 856, pt=46, maxw=740)
        else:
            c.card(430, 846, 1060, 118, col=OR)
            tex.put(c, resultat, CX, 905, pt=54, maxw=980)
    if comm and upto > len(lignes):
        c.txt(CX, 1010, comm, size=32, col=ACC)

# ------------------------------------------------- dessins des exemples (colonne de gauche)
# Zone réservée : x de 140 à 840, y de 320 à 940. Centre pratique : (490, 630).

def fig_goutte(c, upto, t):
    """exemple 1 : l'électrode dépose des électrons sur la gouttelette"""
    c.rect(200, 470, 104, 170, fill="#ffffff", col=ACC, sw=3, rx=8)
    c.txt(252, 448, "électrode", size=25, col=ACC)
    c.path("M 600 500 Q 690 620 690 680 A 90 90 0 1 1 510 680 Q 510 620 600 500 Z",
           col=NEG if upto >= 1 else SOFT, sw=4,
           fill="#e8eeff" if upto >= 1 else "#f2f2f4")
    c.txt(600, 820, "une gouttelette", size=27, col=MUT)
    for k in range(4):                       # les électrons qui sautent vers la goutte
        u = (t + k / 4.0) % 1.0
        x = 310 + (500 - 310) * u
        c.circle(x, 560 + 26 * math.sin(6 * u), 13, col=NEG, sw=3, fill="#eef2ff")
        c.line(x - 6, 560 + 26 * math.sin(6 * u), x + 6, 560 + 26 * math.sin(6 * u),
               col=NEG, sw=3)
    if upto >= 1:
        for k in range(7):
            a = 2 * math.pi * k / 7.0 + 0.3
            c.line(600 + 52 * math.cos(a) - 9, 690 + 52 * math.sin(a),
                   600 + 52 * math.cos(a) + 9, 690 + 52 * math.sin(a), col=NEG, sw=4)
        c.txt(600, 880, "5,0 × 10⁴ électrons en trop", size=27, col=NEG)
    if upto >= 4:
        c.txt(600, 926, "elle est donc négative", size=27, col=ACC)


def fig_deux_spheres(c, upto, t):
    """exemple 2 : deux sphères chargées, et les deux forces égales"""
    xa, xb, y = 280, 720, 620
    c.charge(xa, y, +1, r=52); c.charge(xb, y, -1, r=62)
    c.txt(xa, y + 96, "+3,0 nC", size=28, col=POS)
    c.txt(xb, y + 96, "−5,0 nC", size=28, col=NEG)
    c.line(xa, y + 150, xb, y + 150, col=SOFT, sw=3)
    c.line(xa, y + 136, xa, y + 164, col=SOFT, sw=3)
    c.line(xb, y + 136, xb, y + 164, col=SOFT, sw=3)
    c.txt((xa + xb) / 2, y + 196, "4,0 cm", size=28, col=MUT)
    if upto >= 1:                             # attraction : deux flèches de même longueur
        d = 112 * (0.85 + 0.15 * math.sin(2 * math.pi * t))
        c.arrow(xa + 64, y - 110, xa + 64 + d, y - 110, col=POS, sw=7, head=24)
        c.arrow(xb - 74, y - 110, xb - 74 - d, y - 110, col=NEG, sw=7, head=24)
        c.txt((xa + xb) / 2, y - 158, "même valeur, sens opposés", size=26, col=MUT)
    if upto >= 4:
        c.txt((xa + xb) / 2, 900, "signes opposés : elles s’attirent", size=28, col=ACC)


def fig_dome(c, upto, t):
    """exemple 4 : le dôme de Van de Graaff — charges en surface, calcul depuis le centre"""
    cx, cy, R = 450, 640, 146
    c.rect(cx - 24, cy + R - 10, 48, 150, fill=PALE, col=SOFT, sw=2)   # la colonne
    c.circle(cx, cy, R, col=MUT, sw=4, fill="#ffffff")
    for k in range(12):                                             # charges en périphérie
        ang = 2 * math.pi * k / 12.0
        c.charge(cx + R * math.cos(ang), cy + R * math.sin(ang), +1, r=17)
    c.txt(cx + 52, cy + R + 104, "le dôme", size=27, col=MUT, anchor="start")
    if upto >= 1:
        c.dot(cx, cy, 11, col=INK)
        ang = -0.62                                                 # rayon tracé vers le haut
        c.arrow(cx, cy, cx + R * math.cos(ang), cy + R * math.sin(ang), col=INK, sw=4, head=18)
        c.txt(cx + 104, cy - 112, "r = 20 cm", size=26, col=INK, anchor="start")
        c.txt(cx - 28, cy + 14, "Q", size=38, col=POS, it=True, anchor="end")
        c.txt(490, 372, "les charges sont toutes en surface…", size=27, col=MUT)
        c.txt(490, 410, "…mais tout se passe comme si Q était au centre",
              size=27, col=ACC)
    if upto >= 3:                                                   # le champ sort, radial
        for k in range(12):
            ang = 2 * math.pi * k / 12.0
            if math.sin(ang) > 0.55:                                # pas au-dessus de la colonne
                continue
            u = 0.6 + 0.4 * ((t + k / 12.0) % 1.0)
            c.arrow(cx + (R + 14) * math.cos(ang), cy + (R + 14) * math.sin(ang),
                    cx + (R + 14 + 54 * u) * math.cos(ang),
                    cy + (R + 14 + 54 * u) * math.sin(ang), col=POS, sw=4, head=15)


def fig_sphere_pot(c, upto, t):
    """exemple 6 : une sphère conductrice — même potentiel partout, champ nul dedans"""
    cx, cy, R = 470, 620, 160
    c.circle(cx, cy, R, col=MUT, sw=4, fill="#f3f7f4")
    for k in range(10):
        a = 2 * math.pi * k / 10.0 + 0.2
        c.charge(cx + R * math.cos(a), cy + R * math.sin(a), +1, r=17)
    c.dot(cx, cy, 9, col=INK)
    c.arrow(cx, cy, cx + R, cy, col=INK, sw=4, head=18)
    c.txt(cx + R / 2, cy - 22, "r = 12 cm", size=26, col=INK)
    c.txt(cx, cy + R + 64, "0,16 nC en surface", size=27, col=MUT)
    if upto >= 3:
        c.txt(cx, cy + 56, "E = 0", size=34, col=ACC, it=True)
        c.txt(cx, 384, "le potentiel est le même partout dans le métal", size=27, col=MUT)
    if upto >= 4:
        c.card(cx - 160, 860, 320, 76, col=ACC)
        c.txt(cx, 908, "V = 12 V partout", size=32, col=ACC, bold=True)


# ------------------------------------------------------------------ le fil directeur
def imprimante(c, t, y0=560, charges=(0.0, 0.5, -0.5, 1.0, 0.0, -1.0), labels=0, dev_max=120,
               paper_h=300):
    """schéma de l'imprimante à jet d'encre ; labels : 0 aucun, 1..4 progressifs"""
    bx, by, bw, bh = 760, y0 - 170, 520, 340
    c.rect(250, y0 - 52, 170, 104, fill="#ffffff", col=INK, sw=3, rx=8)
    c.txt(335, y0 + 8, "canon", size=28, col=MUT)
    c.rect(470, y0 - 48, 86, 96, fill="#ffffff", col=ACC, sw=3, rx=6)
    c.txt(513, y0 - 92, "électrode", size=24, col=ACC)
    c.txt(513, y0 - 64, "de charge", size=24, col=ACC)
    c.rect(bx, by, bw, 15, fill=POS); c.rect(bx, by + bh, bw, 15, fill=NEG)
    c.txt(bx - 26, by + 18, "+", size=46, col=POS, anchor="end")
    c.txt(bx - 26, by + bh + 26, "–", size=52, col=NEG, anchor="end")
    c.rect(1540, y0 - paper_h, 26, 2 * paper_h, fill=PALE)
    c.txt(1553, y0 + paper_h + 34, "papier", size=26, col=MUT)
    for i, q in enumerate(charges):
        u = (t + i / float(len(charges))) % 1.0
        x = 420 + (1540 - 420) * u
        dev = 0.0
        if x > bx:
            s = min(1.0, (x - bx) / float(bw))
            dev = -q * dev_max * 0.55 * s * s
            if x > bx + bw:
                dev = -q * dev_max * 0.55 * (1 + 1.6 * (x - bx - bw) / float(1540 - bx - bw))
        col = NEG if q > 0 else (POS if q < 0 else SOFT)
        c.dot(min(x, 1540), y0 + dev, 12, col=col)
    if labels >= 1:
        c.txt(513 + 120, y0 + 120, "elle dépose une charge q", size=28, col=ACC, anchor="start")
    if labels >= 2:
        c.txt(bx + bw / 2, by - 44, "champ uniforme entre les plaques", size=28, col=MUT)
    if labels >= 3:
        c.txt(1566, y0 - paper_h - 22, "la goutte arrive ici", size=26, col=INK, anchor="end")
    return bx, by, bw, bh

# ------------------------------------------------------------------ 1. titre
def s01(c, pi, t):
    for i in range(10):
        a = 2 * math.pi * (i / 10.0 + 0.1 * t)
        x, y = CX + 640 * math.cos(a), 600 + 330 * math.sin(a)
        c.charge(x, y, 1 if i % 2 else -1, r=18, op=0.14)
    c.txt(CX, 380, "Champ électrique", size=130, col=INK, bold=True)
    c.rect(CX - 300, 420, 600, 5, fill=OR)
    c.txt(CX, 488, "Olivier Wulveryck · Creative Commons", size=34, col=MUT)
    if pi >= 2:
        c.txt(CX, 590, "Comment une imprimante vise-t-elle à un dixième de millimètre ?",
              size=42, col=OR, bold=True)
    if pi >= 1:
        imprimante(c, t, y0=840, dev_max=80, paper_h=150)

# ------------------------------------------------------------------ 2. énigme
def s02(c, pi, t):
    head(c, "Le fil directeur", "enigme")
    sous(c, "L’imprimante à jet d’encre")
    imprimante(c, t, y0=560, labels=min(3, pi), paper_h=230)
    if pi >= 3:
        items = ["ce qu’est une charge", "comment deux charges s’attirent",
                 "ce qu’est un champ", "comment on le fabrique entre deux plaques"]
        for i, s in enumerate(items):
            x = 390 + (i % 2) * 700
            y = 930 + (i // 2) * 48
            c.dot(x, y - 9, 9, col=OR)
            c.txt(x + 26, y, s, size=28, col=INK, anchor="start")
    if pi >= 4:
        c.txt(CX, 1036, "et à chaque étape, un exemple chiffré en entier", size=30, col=ACC)

# ------------------------------------------------------------------ 3. la charge
def s03(c, pi, t):
    if pi <= 4:
        reuse(dessins.sc_charge, c, min(pi, 4), t, "La charge électrique", "charge")
        return
    head(c, "La charge électrique", "charge")
    sous(c, "L’unité : le coulomb")
    c.txt(CX, 330, "la charge se note q et se mesure en coulombs (C)", size=38, col=INK)
    c.card(500, 400, 920, 150, col=OR)
    tex.put(c, r"e = 1{,}60 \times 10^{-19}\ \mathrm{C}", CX, 475, pt=56)
    c.txt(CX, 600, "la charge élémentaire : celle d’un électron, la plus petite qui existe",
          size=30, col=MUT)
    if pi >= 6:
        c.card(500, 680, 920, 140, col=PALE, sw=3)
        tex.put(c, r"q = n \times e", CX, 750, pt=54)
        c.txt(CX, 880, "toute charge est un multiple entier de e : la charge est quantifiée",
              size=32, col=ACC)

# ------------------------------------------------------------------ 4. exemple 1
def s04(c, pi, t):
    lignes = [r"q = n \times e",
              r"q = 5{,}0 \times 10^{4} \times 1{,}60 \times 10^{-19}",
              r"q = (5{,}0 \times 1{,}60) \times 10^{4-19} = 8{,}0 \times 10^{-15}"]
    exemple(c, "ex1", 1, "la charge d’une goutte",
            ["L’électrode dépose 5,0 × 10⁴ électrons en trop sur une gouttelette.",
             "Quelle charge porte-t-elle ?"],
            lignes, max(0, pi - 1),
            r"q = -\,8{,}0 \times 10^{-15}\ \mathrm{C}",
            "négative, puisque ce sont des électrons — nous la réutiliserons à la fin",
            fig=fig_goutte, t=t)

# ------------------------------------------------------------------ 5. les règles
def s05(c, pi, t):
    m = {0: 0, 1: 1, 2: 2, 3: 4, 4: 5, 5: 7}[min(pi, 5)]
    reuse(dessins.sc_regles, c, m, t, "Les deux règles d’or", "regles")

# ------------------------------------------------------------------ 6. Coulomb
def s06(c, pi, t):
    head(c, "La loi de Coulomb", "coulomb")
    sous(c, "La valeur de la force entre deux charges")
    c.card(340, 300, 1240, 200, col=OR)
    tex.put(c, r"F = k\,\frac{\lvert Q \rvert \times \lvert q \rvert}{r^{2}}", CX, 400, pt=72)
    if pi >= 2:
        items = [(r"Q,\ q", "les deux charges, en coulombs", POS),
                 (r"r", "la distance entre elles, en mètres", NEG),
                 (r"k \approx 9{,}0 \times 10^{9}", "une constante, en N m² C⁻²", ACC)]
        for i, (s, d, col) in enumerate(items):
            y = 600 + i * 92
            tex.put(c, s, 780, y, pt=40, col=col, anchor="mr")
            c.txt(820, y + 12, d, size=32, col=INK, anchor="start")
    if pi >= 4:
        c.card(430, 880, 1060, 110, col=PALE, sw=3)
        c.txt(CX, 948, "la distance est AU CARRÉ : c’est tout le caractère de cette force",
              size=36, col=INK, bold=True)

# ------------------------------------------------------------------ 7. exemple 2
def s07(c, pi, t):
    lignes = [r"F = k\,\frac{\lvert Q_1 \rvert \lvert Q_2 \rvert}{r^{2}}",
              r"Q_1 = 3{,}0 \times 10^{-9}\ \mathrm{C} \qquad Q_2 = 5{,}0 \times 10^{-9}\ \mathrm{C}"
              r" \qquad r = 4{,}0 \times 10^{-2}\ \mathrm{m}",
              r"F = \frac{9{,}0 \times 10^{9} \times 3{,}0 \times 10^{-9} \times 5{,}0 \times 10^{-9}}"
              r"{(4{,}0 \times 10^{-2})^{2}}",
              r"F = \frac{1{,}35 \times 10^{-7}}{1{,}6 \times 10^{-3}}"]
    exemple(c, "ex2", 2, "deux sphères chargées",
            ["Deux sphères portent +3,0 nC et −5,0 nC, distantes de 4,0 cm.",
             "Quelle force subissent-elles ?"],
            lignes, max(0, pi - 1),
            r"F \approx 8{,}4 \times 10^{-5}\ \mathrm{N}",
            "signes opposés : les deux forces sont attractives, et de même valeur",
            fig=fig_deux_spheres, t=t)

# ------------------------------------------------------------------ 8. le carré
def s08(c, pi, t):
    m = {0: 2, 1: 3, 2: 3, 3: 4, 4: 5}[min(pi, 4)]
    reuse(dessins.sc_coulomb, c, m, t, "Le poids du carré", "carre")
    if pi == 3:
        tex.put(c, r"r \times n \;\Rightarrow\; F \div n^{2}", CX, 1000, pt=42, col=ACC)

# ------------------------------------------------------------------ 9. vecteurs
def s09(c, pi, t):
    if pi <= 3:
        reuse(dessins.sc_vecteur, c, min(pi, 3), t, "Vecteurs", "vecteur")
        return
    head(c, "Vecteurs", "vecteur")
    sous(c, "Le vecteur unitaire u")
    c.charge(520, 560, +1, r=46); c.txt(520, 660, "Q", size=36, col=POS, it=True)
    c.charge(1180, 560, +1, r=34); c.txt(1180, 660, "q", size=36, col=ACC, it=True)
    c.arrow(580, 560, 760, 560, col=MUT, sw=6, head=22)
    tex.put(c, r"\vec{u}", 670, 505, pt=40, col=MUT)
    c.txt(670, 700, "longueur 1, sans unité", size=26, col=MUT)
    c.arrow(1220, 560, 1480, 560, col=POS, sw=7, head=24)
    tex.put(c, r"\vec{F}", 1350, 505, pt=40, col=POS)
    c.card(340, 760, 1240, 180, col=OR)
    tex.put(c, r"\vec{F}_{el} = k\,\frac{Q \cdot q}{r^{2}}\,\vec{u}", CX, 850, pt=62)
    if pi >= 5:
        c.txt(CX, 1010, "le signe du produit Q·q donne le sens : + pour la répulsion, – pour l’attraction",
              size=32, col=ACC)

# ------------------------------------------------------------------ 10. exemple 3
def s10(c, pi, t):
    head(c, "Exemple 3 — additionner deux flèches", "ex3")
    sous(c, "On additionne les coordonnées, jamais les longueurs")
    ox, oy = 620, 800
    v1, v2 = (360, 0), (0, -270)
    a = seg(t, 0.05, 0.35); b = seg(t, 0.40, 0.68); s = seg(t, 0.74, 0.95)
    c.dot(ox, oy, 10, col=INK)
    if pi >= 1 and a > 0:
        c.arrow(ox, oy, ox + v1[0] * a, oy + v1[1] * a, col=POS, sw=7, head=26)
        c.txt(ox + 180, oy + 54, "4", size=38, col=POS, it=True)
    if pi >= 1 and b > 0:
        c.arrow(ox + v1[0], oy, ox + v1[0], oy + v2[1] * b, col=NEG, sw=7, head=26)
        c.txt(ox + v1[0] + 44, oy - 140, "3", size=38, col=NEG, it=True)
    if pi >= 1 and s > 0:
        c.arrow(ox, oy, ox + v1[0] * s, oy + v2[1] * s, col=INK, sw=8, head=30)
        c.txt(ox + 130, oy - 180, "5", size=44, col=INK, it=True)
    if pi >= 2:
        tex.put(c, r"x = x_1 + x_2 \qquad y = y_1 + y_2", 1340, 480, pt=40, col=INK)
    if pi >= 3:
        tex.put(c, r"\lVert \vec{E} \rVert = \sqrt{x^{2} + y^{2}}", 1340, 600, pt=44, col=ACC)
    if pi >= 4:
        c.card(1060, 700, 560, 150, col=OR)
        tex.put(c, r"\sqrt{3^{2} + 4^{2}} = 5", 1340, 775, pt=50)
        c.txt(1340, 900, "trois et quatre ne font pas sept", size=30, col=MUT)

# ------------------------------------------------------------------ 11. le champ
def s11(c, pi, t):
    m = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 7}[min(pi, 6)]
    reuse(dessins.sc_champ, c, m, t, "Le champ électrique", "champ")
    if pi == 3:
        c.rect(330, 290, 1260, 200, fill=BG)
        c.card(380, 300, 1160, 180, col=OR)
        tex.put(c, r"E = \frac{F_{el}}{\lvert q \rvert}", CX, 392, pt=64)
    if pi == 4:
        c.rect(330, 590, 1260, 200, fill=BG)
        c.card(380, 600, 1160, 180, col=PALE, sw=3)
        tex.put(c, r"\vec{F} = q\,\vec{E}", CX, 692, pt=60)

# ------------------------------------------------------------------ 12. champ radial
def s12(c, pi, t):
    head(c, "Le champ d’une charge seule", "radial")
    sous(c, "On part de Coulomb, et on divise par q")
    if pi <= 1:
        tex.put(c, r"E = \frac{F_{el}}{\lvert q \rvert} = \frac{1}{\lvert q \rvert}\;"
                   r"k\,\frac{\lvert Q \rvert \lvert q \rvert}{r^{2}}", CX, 400, pt=54, col=MUT)
        if pi >= 1:
            c.card(430, 520, 1060, 190, col=OR)
            tex.put(c, r"E = k\,\frac{\lvert Q \rvert}{r^{2}}", CX, 615, pt=70)
            c.txt(CX, 790, "la charge d’essai a disparu : le champ ne dépend que de Q et de r",
                  size=34, col=ACC)
    else:
        x0, y0 = 620, 620
        sgn = +1 if pi <= 3 else -1
        c.charge(x0, y0, sgn, r=52)
        for k in range(16):
            a = 2 * math.pi * k / 16.0
            r0, r1 = 72, 230
            if sgn > 0:
                c.arrow(x0 + r0 * math.cos(a), y0 + r0 * math.sin(a),
                        x0 + r1 * math.cos(a), y0 + r1 * math.sin(a), col=POS, sw=4, head=16)
            else:
                c.arrow(x0 + r1 * math.cos(a), y0 + r1 * math.sin(a),
                        x0 + r0 * math.cos(a), y0 + r0 * math.sin(a), col=NEG, sw=4, head=16)
        c.txt(x0, y0 + 320, "centrifuge  (Q > 0)" if sgn > 0 else "centripète  (Q < 0)",
              size=36, col=POS if sgn > 0 else NEG)
        tex.put(c, r"E = k\,\frac{\lvert Q \rvert}{r^{2}}", 1360, 480, pt=60)
        if pi >= 4:
            gx, gy, gw, gh = 1100, 640, 520, 240
            c.line(gx, gy + gh, gx + gw, gy + gh, col=SOFT, sw=3)
            c.line(gx, gy, gx, gy + gh, col=SOFT, sw=3)
            pts = []
            for i in range(61):
                rr = 1.0 + 2.0 * i / 60.0
                pts.append("%s%.1f %.1f" % ("M" if i == 0 else "L",
                           gx + gw * (rr - 1) / 2.0, gy + gh - gh * min(1.0, 1.0 / rr ** 2)))
            c.path(" ".join(pts), col=ACC, sw=4)
            c.txt(gx + gw / 2, gy - 20, "deux fois plus loin : quatre fois plus faible",
                  size=28, col=MUT)

# ------------------------------------------------------------------ 13. exemple 4
def s13(c, pi, t):
    lignes = [r"E = k\,\frac{\lvert Q \rvert}{r^{2}} \quad\text{(sphère : charge au centre)}",
              r"Q = 15 \times 10^{-6}\ \mathrm{C} \qquad r = 0{,}20\ \mathrm{m}",
              r"E = \frac{9{,}0 \times 10^{9} \times 15 \times 10^{-6}}{(0{,}20)^{2}}"
              r" = \frac{1{,}35 \times 10^{5}}{4{,}0 \times 10^{-2}}"]
    exemple(c, "ex4", 4, "le dôme de Van de Graaff",
            ["Le dôme est une sphère de rayon 20 cm portant une charge de 15 µC.",
             "Quel est le champ à sa surface ?"],
            lignes, max(0, pi - 1),
            r"E \approx 3{,}4 \times 10^{6}\ \mathrm{V\,m^{-1}}", None,
            fig=fig_dome, t=t)
    if pi >= 4:
        c.card(300, 980, 1320, 84, col=PALE, sw=3)
        c.txt(CX, 1032, "au-delà de 3,0 × 10⁶ V/m l’air devient conducteur : "
                        "des étincelles jaillissent", size=30, col=ACC)

# ------------------------------------------------------------------ 14. lignes de champ
def s14(c, pi, t):
    m = {0: 0, 1: 1, 2: 3, 3: 4, 4: 5, 5: 6, 6: 6}[min(pi, 6)]
    reuse(dessins.sc_lignes, c, m, t, "Les lignes de champ", "lignes")

# ------------------------------------------------------------------ 15. exemple 5
def s15(c, pi, t):
    head(c, "Exemple 5 — deux charges, un point", "ex5")
    if pi <= 1:
        sous(c, "Chaque charge crée son champ comme si l’autre n’existait pas")
        dessins.sc_super(c, 2 if pi else 1, t)
        head(c, "Exemple 5 — deux charges, un point", "ex5")
        sous(c, "Chaque charge crée son champ comme si l’autre n’existait pas")
        return
    c.card(220, 160, 1480, 120, col=PALE, sw=3)
    c.txt(CX, 205, "Deux charges +4,0 nC et +2,0 nC sont distantes de 6,0 cm.", size=31, col=INK)
    c.txt(CX, 249, "Que vaut le champ au milieu du segment ?", size=31, col=INK)
    y = 640
    c.charge(520, y, +1, r=44); c.charge(1400, y, +1, r=38)
    c.txt(520, y + 92, "+4,0 nC", size=30, col=POS); c.txt(1400, y + 92, "+2,0 nC", size=30, col=POS)
    c.dot(960, y, 11, col=INK); c.txt(960, y + 52, "P", size=34, col=INK, it=True)
    c.line(520, y + 150, 960, y + 150, col=SOFT, sw=3)
    c.line(960, y + 150, 1400, y + 150, col=SOFT, sw=3)
    c.txt(740, y + 192, "3,0 cm", size=28, col=MUT); c.txt(1180, y + 192, "3,0 cm", size=28, col=MUT)
    if pi >= 3:
        c.arrow(960, y - 60, 1260, y - 60, col=POS, sw=7, head=24)
        c.txt(1115, y - 100, "E₁ = 4,0 × 10⁴", size=28, col=POS)
        c.arrow(960, y - 170, 810, y - 170, col=NEG, sw=7, head=24)
        c.txt(805, y - 210, "E₂ = 2,0 × 10⁴", size=28, col=NEG, anchor="start")
    if pi >= 4:
        tex.put(c, r"E_1 = k\,\frac{4{,}0 \times 10^{-9}}{(3{,}0 \times 10^{-2})^{2}}"
                   r" = 4{,}0 \times 10^{4} \qquad "
                   r"E_2 = 2{,}0 \times 10^{4}", CX, 356, pt=34, col=MUT, maxw=1400)
    if pi >= 5:
        c.card(430, 846, 1060, 118, col=OR)
        tex.put(c, r"E = E_1 - E_2 = 2{,}0 \times 10^{4}\ \mathrm{V\,m^{-1}}", CX, 905, pt=50)
    if pi >= 6:
        c.txt(CX, 1020, "dirigé vers la charge la plus faible — et plus loin, il existe un point nul",
              size=31, col=ACC)

# ------------------------------------------------------- le potentiel : la définition
def s_potdef(c, pi, t):
    head(c, "Qu’est-ce que le potentiel ?", "potdef")
    sous(c, "Une énergie par unité de charge")
    if pi >= 1:                                   # rappel : ce qu'on a fait pour le champ
        c.card(170, 300, 700, 280, col=SOFT, sw=3)
        c.txt(520, 352, "ce qu’on a fait pour le champ", size=29, col=MUT)
        tex.put(c, r"\vec{E} = \frac{\vec{F}}{q}", 520, 452, pt=50, col=INK)
        c.txt(520, 544, "la force par unité de charge", size=27, col=MUT)
    if pi >= 4:                                   # la même opération, avec l'énergie
        c.card(1050, 300, 700, 280, col=OR, sw=3)
        c.txt(1400, 352, "la même opération avec l’énergie", size=29, col=MUT)
        tex.put(c, r"V = \frac{E_p}{q}", 1400, 452, pt=50, col=INK)
        c.txt(1400, 544, "l’énergie par unité de charge", size=27, col=ACC)
    elif pi == 3:
        c.txt(1400, 440, "et avec l’énergie ?", size=36, col=SOFT)

    if 3 <= pi <= 4:                              # doubler la charge double l'énergie
        base = 900
        c.txt(760, 648, "si je double la charge, je double l’énergie", size=30, col=MUT)
        for x, rq, h, lab, elab in ((540, 26, 90, "q", "Eₚ"), (900, 38, 180, "2q", "2 Eₚ")):
            c.charge(x, base - 44, +1, r=rq)
            c.txt(x, base + 46, lab, size=32, col=POS, it=True)
            c.rect(x + 86, base - h, 44, h, fill=NEG)
            c.txt(x + 108, base + 46, elab, size=28, col=NEG)
        if pi >= 4:
            c.arrow(1130, base - 70, 1240, base - 70, col=ACC, sw=6, head=22)
            c.txt(1185, base - 110, "÷ q", size=30, col=ACC)
            c.rect(1320, base - 110, 44, 110, fill=OR)
            c.rect(1440, base - 110, 44, 110, fill=OR)
            c.txt(1402, base + 46, "même V", size=30, col=ACC)
            c.txt(1402, base + 88, "c’est l’endroit qui parle", size=26, col=MUT)

    if 1 <= pi <= 2:                              # la force dépend de ce qu'on pose
        c.charge(1250, 780, +1, r=34)
        c.arrow(1300, 780, 1520, 780, col=POS, sw=7, head=24)
        tex.put(c, r"\vec{F}", 1410, 730, pt=38, col=POS)
        c.txt(1400, 876, "la force dépend de la charge qu’on pose", size=28, col=MUT)
        if pi >= 2:
            c.txt(1400, 920, "…et l’énergie aussi", size=28, col=ACC)
    if pi >= 5:                                   # l'unité
        c.card(560, 630, 800, 120, col=ACC)
        tex.put(c, r"1\ \mathrm{V} = 1\ \mathrm{J\,C^{-1}}", CX, 690, pt=52, col=INK)
    if pi >= 6:                                   # la pile
        bx, by = 620, 884
        c.line(bx, by - 46, bx, by + 46, col=INK, sw=7)
        c.line(bx + 34, by - 26, bx + 34, by + 26, col=INK, sw=7)
        c.line(bx - 90, by, bx, by, col=INK, sw=4)
        c.line(bx + 34, by, bx + 124, by, col=INK, sw=4)
        c.txt(bx + 17, by - 76, "12 V", size=34, col=INK, bold=True)
        u = (t * 1.2) % 1.0
        c.dot(bx - 90 + 214 * u, by, 12, col=POS)
        c.txt(820, by - 14, "chaque coulomb qui passe", size=30, col=MUT, anchor="start")
        c.txt(820, by + 30, "reçoit douze joules", size=30, col=ACC, anchor="start")
    if pi >= 7:
        c.txt(CX, 1016, "le champ est une flèche, le potentiel un simple nombre",
              size=32, col=INK)

# ------------------------------------------------------------------ 16. potentiel
def s16(c, pi, t):
    if pi <= 3:
        reuse(dessins.sc_potentiel, c, min(pi, 4), t, "Le potentiel", "potentiel")
        return
    head(c, "Le potentiel", "potentiel")
    sous(c, "Le potentiel d’une charge ponctuelle")
    c.card(430, 320, 1060, 180, col=OR)
    tex.put(c, r"V = k\,\frac{Q}{r}", CX, 410, pt=66)
    tex.put(c, r"V \propto \frac{1}{r} \qquad \text{alors que} \qquad E \propto \frac{1}{r^{2}}",
            CX, 600, pt=44, col=MUT)
    if pi >= 5:
        c.card(340, 700, 1240, 230, col=PALE, sw=3)
        c.txt(CX, 770, "V est un nombre, pas une flèche", size=40, col=INK, bold=True)
        c.txt(CX, 830, "pour plusieurs charges, on additionne de simples nombres", size=32, col=MUT)
        c.txt(CX, 890, "— c’est bien plus facile que d’additionner des vecteurs", size=32, col=MUT)

# ------------------------------------------------------------------ 17. exemple 6
def s17(c, pi, t):
    lignes = [r"V = k\,\frac{Q}{r}",
              r"V = \frac{9{,}0 \times 10^{9} \times 0{,}16 \times 10^{-9}}{0{,}12}",
              r"V = \frac{1{,}44}{0{,}12}"]
    exemple(c, "ex6", 6, "le potentiel d’une sphère",
            ["Une sphère conductrice isolée de rayon 12 cm reçoit une charge de 0,16 nC.",
             "Quel est son potentiel ?"],
            lignes, max(0, pi - 1), r"V = 12\ \mathrm{V}", None,
            fig=fig_sphere_pot, t=t)
    if pi >= 4:
        c.card(300, 980, 1320, 84, col=PALE, sw=3)
        c.txt(CX, 1032, "tout le métal est à 12 V, et le champ est nul à l’intérieur : "
                        "c’est la cage de Faraday", size=30, col=ACC)

# ------------------------------------------------------------------ 18. plaques
def s18(c, pi, t):
    head(c, "Entre deux plaques", "plaques")
    sous(c, "Un champ uniforme")
    U = 1.0 if t < 0.5 else 2.0
    bx, by, bw, bh = 470, 320, 880, 380
    c.rect(bx, by, bw, 15, fill=POS); c.rect(bx, by + bh, bw, 15, fill=NEG)
    c.txt(bx - 30, by + 18, "+", size=46, col=POS, anchor="end")
    c.txt(bx - 30, by + bh + 26, "–", size=52, col=NEG, anchor="end")
    for j in range(5):
        yy = by + 55 + j * (bh - 110) / 4.0
        c.arrow(bx + 40, yy, bx + bw - 40, yy, col=POS,
                sw=3 + 3 * (U - 1), head=18 + 8 * (U - 1))
    c.line(bx + bw + 60, by, bx + bw + 60, by + bh, col=MUT, sw=3)
    c.txt(bx + bw + 100, by + bh / 2, "d", size=42, col=MUT, it=True, anchor="start")
    if pi >= 4:
        c.txt(bx + bw / 2, by - 44, "U = %d V" % int(200 * U), size=42, col=INK, bold=True)
    if pi >= 2:
        c.card(430, 760, 1060, 170, col=OR)
        tex.put(c, r"E = \frac{U}{d}", CX, 845, pt=66)
    if pi >= 3 and pi < 5:
        c.txt(CX, 990, "on descend de U volts en parcourant d mètres : c’est une pente",
              size=32, col=MUT)
    if pi >= 5:
        tex.put(c, r"E = \frac{200}{0{,}10} = 2{,}0 \times 10^{3}\ \mathrm{V\,m^{-1}}",
                CX, 1010, pt=40, col=ACC, maxw=900)

# ------------------------------------------------------------------ 19. énergie
def s19(c, pi, t):
    head(c, "Travail et énergie", "energie")
    sous(c, "Relier l’électricité à l’énergie")
    if pi >= 1:
        tex.put(c, r"1\ \mathrm{V} = 1\ \mathrm{J\,C^{-1}}", CX, 330, pt=44, col=MUT)
    c.card(430, 400, 1060, 170, col=OR)
    tex.put(c, r"W = q\,\Delta V", CX, 485, pt=66)
    if pi >= 2:
        tex.put(c, r"W = 2 \times (50 - 35) = 30\ \mathrm{J}", CX, 650, pt=48, col=INK)
        c.txt(CX, 715, "exemple 8 : une charge de 2 C qui passe de 50 V à 35 V", size=30, col=MUT)
    if pi >= 3:
        ox, oy, w = 420, 930, 1080
        for i in range(3):
            c.line(ox, oy - i * 56, ox + w, oy - i * 56, col=SOFT, sw=2, dash="8 8")
        px = ox + 80 + (w - 160) * pingpong(t)
        c.dot(px, oy - 112, 14, col=ACC)
        c.txt(CX, oy + 60, "le long d’une équipotentielle : ΔV = 0, donc W = 0", size=34, col=ACC)

# ------------------------------------------------------------------ 20-22. le fil directeur
def s20(c, pi, t):
    head(c, "Retour à la goutte — le champ", "fil1")
    imprimante(c, t, y0=390, dev_max=80, paper_h=150)
    if pi >= 1:
        c.txt(CX, 630, "plaques distantes de 12 mm, sous 1200 V", size=36, col=INK)
    lignes = [r"E = \frac{U}{d}",
              r"E = \frac{1200}{12 \times 10^{-3}}"]
    y = 730
    for i, l in enumerate(lignes):
        if i >= max(0, pi - 1):
            break
        tex.put(c, l, CX, y, pt=44, col=MUT if i < pi - 2 else INK)
        y += 104
    if pi >= 4:
        c.card(560, 930, 800, 110, col=OR)
        tex.put(c, r"E = 1{,}0 \times 10^{5}\ \mathrm{V\,m^{-1}}", CX, 985, pt=50)

def s21(c, pi, t):
    head(c, "Retour à la goutte — la force", "fil2")
    sous(c, "On applique la définition du champ")
    if pi >= 1:
        tex.put(c, r"q = 8{,}0 \times 10^{-15}\ \mathrm{C} \qquad "
                   r"E = 1{,}0 \times 10^{5}\ \mathrm{V\,m^{-1}}", CX, 330, pt=40, col=MUT)
    if pi >= 2:
        tex.put(c, r"F = q\,E = 8{,}0 \times 10^{-15} \times 1{,}0 \times 10^{5}", CX, 450, pt=46)
    if pi >= 3:
        c.card(560, 520, 800, 110, col=OR)
        tex.put(c, r"F = 8{,}0 \times 10^{-10}\ \mathrm{N}", CX, 575, pt=50)
    if pi >= 4:
        c.txt(CX, 700, "est-ce beaucoup ? comparons au poids de la goutte", size=34, col=INK)
        tex.put(c, r"P = m\,g = 1{,}3 \times 10^{-11} \times 9{,}81 = 1{,}3 \times 10^{-10}\ \mathrm{N}",
                CX, 790, pt=40, col=MUT, maxw=1500)
    if pi >= 5:
        c.card(430, 850, 1060, 150, col=PALE, sw=3)
        tex.put(c, r"\frac{F}{P} \approx 6", 700, 925, pt=48, col=ACC)
        c.txt(1120, 938, "la gravité est négligeable", size=34, col=INK)

def s22(c, pi, t):
    head(c, "Retour à la goutte — viser", "fil3")
    qs = (0.0, 0.5, -0.5, 1.0, 0.0, -1.0) if pi >= 1 else (0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    imprimante(c, t, y0=470, charges=qs, dev_max=200, paper_h=250)
    if pi >= 2:
        c.card(360, 790, 1200, 120, col=OR)
        tex.put(c, r"\vec{F} = q\,\vec{E} \quad\Rightarrow\quad "
                   r"\text{déviation} \;\propto\; q", CX, 850, pt=48)
    if pi >= 3:
        c.txt(CX, 960, "une goutte non chargée file tout droit : c’est l’espace entre deux mots",
              size=32, col=MUT)
    if pi >= 4:
        c.txt(CX, 1020, "q = n e      ·      E = U / d      ·      F = q E",
              size=34, col=ACC, bold=True)

# ------------------------------------------------------------------ 23. Millikan
def s23(c, pi, t):
    head(c, "Le même montage, à l’envers", "millikan")
    sous(c, "L’expérience de Millikan, 1909")
    bx, by, bw, bh = 520, 330, 780, 360
    c.rect(bx, by, bw, 15, fill=POS); c.rect(bx, by + bh, bw, 15, fill=NEG)
    gy = by + bh / 2 + (14 * math.sin(2 * math.pi * t) if pi < 2 else 0)
    c.dot(bx + bw / 2, gy, 18, col=INK)
    c.arrow(bx + bw / 2, gy - 26, bx + bw / 2, gy - 150, col=ACC, sw=7, head=24)
    c.txt(bx + bw / 2 - 80, gy - 100, "qE", size=34, col=ACC, it=True)
    c.arrow(bx + bw / 2, gy + 26, bx + bw / 2, gy + 150, col=MUT, sw=7, head=24)
    c.txt(bx + bw / 2 + 80, gy + 110, "mg", size=34, col=MUT, it=True)
    if pi >= 2:
        c.txt(bx + bw / 2, by + bh + 66, "on règle U jusqu’à l’immobilité", size=32, col=INK)
    if pi >= 3:
        tex.put(c, r"q\,E = m\,g \quad\text{avec}\quad E = \frac{U}{d}"
                   r"\quad\Rightarrow\quad q = \frac{m\,g\,d}{U}", CX, 822, pt=44, maxw=1400)
    if pi >= 4:
        c.card(430, 880, 1060, 112, col=OR)
        tex.put(c, r"q = 6{,}7 \times 10^{-19}\ \mathrm{C} \approx 4\,e", CX, 936, pt=48)
        c.txt(CX, 1032, "jamais 3,5 e, jamais 4,25 e : la charge est quantifiée", size=31, col=ACC)

# ------------------------------------------------------------------ 24. méthode
def s24(c, pi, t):
    head(c, "La méthode, et les pièges", "methode")
    sous(c, "Les cinq étapes suivies dans tous les exemples")
    etapes = ["faire un schéma : les charges, leurs signes, le point cherché",
              "reconnaître la situation : charge ponctuelle, deux plaques, ou superposition",
              "écrire la formule en lettres, avant les nombres",
              "convertir en unités SI : m, kg, s, C, V",
              "vérifier : unité, ordre de grandeur, sens de la flèche"]
    for i, s in enumerate(etapes):
        if i >= min(pi, 5):
            break
        y = 320 + i * 94
        actif = (i == min(pi, 5) - 1)
        c.circle(390, y - 10, 30, col=OR if actif else PALE, sw=4, fill="#ffffff")
        c.txt(390, y + 4, str(i + 1), size=34, col=OR if actif else SOFT, bold=True)
        c.txt(450, y + 6, s, size=33, col=INK if actif else MUT, anchor="start")
    if pi >= 6:
        c.card(300, 830, 1320, 200, col=OR)
        c.txt(CX, 890, "les trois pièges", size=34, col=INK, bold=True)
        c.txt(CX, 940, "le carré porte aussi sur la puissance de 10   ·   "
                       "on additionne des vecteurs, pas des normes", size=29, col=INK)
        c.txt(CX, 985, "pour une charge négative, la force et le champ sont de sens opposés",
              size=29, col=INK)

# ------------------------------------------------------------------ 25. récapitulatif
def s25(c, pi, t):
    head(c, "Ce qu’il faut retenir", "final")
    sous(c, "Tout le chapitre tient dans cinq relations", y=200)
    forms = [(r"F = k\,\frac{\lvert Q \rvert \lvert q \rvert}{r^{2}}", "la loi de Coulomb"),
             (r"E = \frac{F}{\lvert q \rvert} \qquad \vec{F} = q\,\vec{E}",
              "le champ : force par unité de charge"),
             (r"E = k\,\frac{\lvert Q \rvert}{r^{2}}", "le champ d’une charge ponctuelle"),
             (r"E = \frac{U}{d}", "le champ uniforme entre deux plaques"),
             (r"W = q\,\Delta V", "l’énergie échangée")]
    n = min(pi, 5) if pi >= 1 else 0
    for i, (f, d) in enumerate(forms):
        if i >= n:
            break
        y = 290 + i * 132
        actif = (i == n - 1)
        c.card(300, y, 1320, 118, col=OR if actif else PALE, sw=4 if actif else 2)
        tex.put(c, f, 640, y + 60, pt=40, maxw=560)
        c.txt(1040, y + 72, d, size=29, col=MUT, anchor="start")
    if pi >= 6:
        c.txt(CX, 1020, "cinq relations, une méthode, et une gouttelette d’encre pour tout relier",
              size=36, col=ACC)

SCENES = {"potdef": s_potdef, "titre": s01, "enigme": s02, "charge": s03, "ex1": s04, "regles": s05,
          "coulomb": s06, "ex2": s07, "carre": s08, "vecteur": s09, "ex3": s10,
          "champ": s11, "radial": s12, "ex4": s13, "lignes": s14, "ex5": s15,
          "potentiel": s16, "ex6": s17, "plaques": s18, "energie": s19,
          "fil1": s20, "fil2": s21, "fil3": s22, "millikan": s23, "methode": s24,
          "final": s25}
