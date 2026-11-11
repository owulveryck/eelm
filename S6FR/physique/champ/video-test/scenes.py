# -*- coding: utf-8 -*-
"""Les 24 plans de la vidéo de révision « spécial test ».
Les dessins de base sont dans dessins.py ; le texte lu est dans script.py."""
import math
import canvas, tex
import dessins, script
from canvas import (C, W, H, INK, MUT, POS, NEG, ACC, SOFT, OR, PALE, BG,
                    ease, pingpong, clamp, seg)
from dessins import (sous, puces, chip, tableau, carte, condensateur, dispositif,
                     bilan, nuage, escalier)

canvas.CHAPITRE = "Champ électrique · révision"
CX = W / 2.0

RANG = {sid: i + 1 for i, (sid, _, _) in enumerate(script.SCENES)}
NSC = len(script.SCENES)

def head(c, titre, sid):
    canvas.head(c, titre, RANG[sid], NSC)

# ------------------------------------------------------------------ l'exemple type
def exemple(c, sid, titre, enonce, lignes, upto, resultat=None, comm=None, fig=None, t=0.0):
    """Mise en page d'un exemple résolu : situation à gauche, calcul à droite."""
    head(c, titre, sid)
    c.card(220, 150, 1480, 118, col=PALE, sw=3)
    for i, l in enumerate(enonce[:2]):
        c.txt(CX, 194 + i * 44, l, size=31, col=INK)
    if fig:
        fig(c, upto, t)
        xc, pt0, pt1, larg = 1290, 34, 38, 830
        y, pas = 378, 94
    else:
        xc, pt0, pt1, larg = CX, 40, 46, 1560
        y, pas = 390, 112
    for i, l in enumerate(lignes):
        if i >= upto:
            break
        der = (i == upto - 1)
        tex.put(c, l, xc, y, pt=pt1 if der else pt0,
                col=INK if der else MUT, maxw=larg)
        y += pas
    if resultat and upto >= len(lignes):
        c.card(890, 800, 800, 112, col=OR)
        tex.put(c, resultat, 1290, 856, pt=46, maxw=740)
    if comm and upto > len(lignes):
        c.txt(CX, 1010, comm, size=31, col=ACC)

# ------------------------------------------------------------------ 1. titre
def s_titre(c, pi, t):
    for i in range(12):                       # décor : quelques charges pâles
        a = 2 * math.pi * (i / 12.0 + 0.1 * t)
        x, y = CX + 620 * math.cos(a), 600 + 330 * math.sin(a * 1.7)
        c.charge(x, y, 1 if i % 2 else -1, r=16, op=0.14)
    c.txt(CX, 300, "Révision — le test", size=118, col=INK, bold=True)
    c.rect(CX - 300, 342, 600, 5, fill=OR)
    c.txt(CX, 408, "Champ électrique · Olivier Wulveryck · Creative Commons", size=32, col=MUT)
    if pi >= 1:
        c.txt(CX, 520, "Coulomb  ·  condensateur  ·  lignes de champ  ·  Millikan  ·  quantification",
              size=37, col=INK)
    if pi >= 2:
        c.txt(CX, 585, "les calculs en entier, les schémas tels qu’il faut les tracer",
              size=31, col=OR)
    # le fil directeur : la goutte immobile entre deux plaques
    bx, by, bw, bh = 700, 660, 520, 300
    c.rect(bx, by, bw, 13, fill=POS)
    c.rect(bx, by + bh, bw, 13, fill=NEG)
    wob = 0 if pi >= 3 else 11 * math.sin(2 * math.pi * t)
    bilan(c, bx + bw / 2.0, by + bh / 2.0 + wob, 95, 95, lab=pi >= 3)
    if pi >= 3:
        c.txt(CX, by + bh + 78, "une goutte d’huile immobile : presque tout le test est là",
              size=34, col=INK, bold=True)

# ------------------------------------------------------------------ 2. le programme
def s_prog(c, pi, t):
    head(c, "Le programme du test", "prog")
    sous(c, "Six points, et rien d’autre")
    items = ["la force de Coulomb, et le carré de la distance",
             "le champ uniforme dans un condensateur : E = U / d",
             "les lignes de champ dans un condensateur, loin des bords",
             "deux charges : signes opposés, puis mêmes signes",
             "l’expérience de Millikan : dispositif et démonstration",
             "l’analyse des données : montrer qu’une grandeur est quantifiée"]
    n = min(pi, 6)
    for i, s in enumerate(items):
        y = 300 + i * 112
        vu = i < n
        act = (i == n - 1)
        c.card(230, y, 1460, 92, col=OR if act else (PALE if vu else "#f2efe8"),
               sw=4 if act else 2, fill="#ffffff" if vu else "#f6f3ec")
        c.circle(300, y + 46, 30, col=OR if act else SOFT, sw=4,
                 fill="#ffffff" if vu else "#f6f3ec")
        if vu:
            c.path("M%.1f %.1f L%.1f %.1f L%.1f %.1f" % (286, y + 46, 297, y + 58, 316, y + 33),
                   col=OR if act else ACC, sw=5)
        else:
            c.txt(300, y + 58, str(i + 1), size=34, col=SOFT, bold=True)
        c.txt(360, y + 58, s, size=33, col=INK if vu else SOFT, anchor="start",
              bold=act)

# ------------------------------------------------------------------ 3. la loi de Coulomb
def s_coulomb(c, pi, t):
    head(c, "La force de Coulomb", "coulomb")
    sous(c, "Deux charges ponctuelles, une force")
    xa, xb, y = 660, 1260, 390
    c.charge(xa, y, +1, r=44)
    c.charge(xb, y, -1, r=44)
    c.txt(xa, y + 96, "Q", size=36, col=POS, it=True)
    c.txt(xb, y + 96, "q", size=36, col=NEG, it=True)
    d = 118 * (0.88 + 0.12 * math.sin(2 * math.pi * t))
    c.arrow(xa + 56, y - 92, xa + 56 + d, y - 92, col=POS, sw=7, head=24)
    c.arrow(xb - 56, y - 92, xb - 56 - d, y - 92, col=NEG, sw=7, head=24)
    c.line(xa, y + 150, xb, y + 150, col=SOFT, sw=3)
    c.line(xa, y + 136, xa, y + 164, col=SOFT, sw=3)
    c.line(xb, y + 136, xb, y + 164, col=SOFT, sw=3)
    c.txt((xa + xb) / 2.0, y + 196, "r", size=38, col=MUT, it=True)
    if pi >= 1:
        c.card(430, 610, 1060, 150, col=OR)
        tex.put(c, r"F = k\,\frac{\lvert Q \rvert\,\lvert q \rvert}{r^{2}}", CX, 685, pt=62)
    if pi >= 2:
        c.txt(CX, 812, "k = 9,0 × 10⁹ (SI)   ·   Q et q en coulombs   ·   r en mètres",
              size=32, col=MUT)
    if pi >= 3:
        c.txt(CX, 866, "les valeurs absolues donnent la valeur de la force : un nombre positif",
              size=31, col=MUT)
    if pi >= 4:
        c.txt(660, 924, "mêmes signes : répulsion", size=33, col=POS)
        c.txt(1290, 924, "signes opposés : attraction", size=33, col=NEG)
    if pi >= 5:
        c.card(330, 960, 1260, 86, col=ACC)
        c.txt(CX, 1014, "les deux forces ont toujours la même valeur — 3ᵉ loi de Newton",
              size=33, col=INK, bold=True)

# ------------------------------------------------------------------ 4. exemple Coulomb
def fig_coulomb(c, upto, t):
    xa, xb, y = 280, 700, 600
    c.charge(xa, y, +1, r=50)
    c.charge(xb, y, -1, r=50)
    c.txt(xa, y + 100, "+2,0 µC", size=29, col=POS)
    c.txt(xb, y + 100, "−3,0 µC", size=29, col=NEG)
    c.line(xa, y + 160, xb, y + 160, col=SOFT, sw=3)
    c.line(xa, y + 146, xa, y + 174, col=SOFT, sw=3)
    c.line(xb, y + 146, xb, y + 174, col=SOFT, sw=3)
    c.txt((xa + xb) / 2.0, y + 206, "5,0 cm", size=29, col=MUT)
    if upto >= 5:
        d = 112 * (0.86 + 0.14 * math.sin(2 * math.pi * t))
        c.arrow(xa + 62, y - 110, xa + 62 + d, y - 110, col=POS, sw=7, head=24)
        c.arrow(xb - 62, y - 110, xb - 62 - d, y - 110, col=NEG, sw=7, head=24)
        c.txt((xa + xb) / 2.0, y - 160, "21,6 N chacune", size=29, col=INK)
    if upto >= 6:
        c.txt((xa + xb) / 2.0, 900, "signes opposés : elles s’attirent", size=29, col=ACC)

def s_exC(c, pi, t):
    lignes = [r"F = k\,\frac{\lvert Q \rvert\,\lvert q \rvert}{r^{2}}",
              r"Q = 2{,}0 \times 10^{-6}\ \mathrm{C}\quad q = 3{,}0 \times 10^{-6}\ \mathrm{C}"
              r"\quad r = 5{,}0 \times 10^{-2}\ \mathrm{m}",
              r"r^{2} = (5{,}0 \times 10^{-2})^{2} = 2{,}5 \times 10^{-3}\ \mathrm{m^{2}}",
              r"k\,\lvert Q \rvert\,\lvert q \rvert = 9{,}0 \times 10^{9} \times 2{,}0 \times 10^{-6}"
              r" \times 3{,}0 \times 10^{-6} = 5{,}4 \times 10^{-2}",
              r"F = \frac{5{,}4 \times 10^{-2}}{2{,}5 \times 10^{-3}}"]
    exemple(c, "exC", "Exemple — la force de Coulomb",
            ["Deux charges ponctuelles +2,0 µC et −3,0 µC sont distantes de 5,0 cm.",
             "Calculer la force qu’elles exercent l’une sur l’autre."],
            lignes, max(0, pi - 1), r"F = 21{,}6\ \mathrm{N}",
            "même valeur, sens opposés : chacune est attirée vers l’autre",
            fig=fig_coulomb, t=t)

# ------------------------------------------------------------------ 5. le carré
def s_carre(c, pi, t):
    head(c, "Le carré de la distance", "carre")
    sous(c, "Répondre par un rapport, sans calculatrice")
    ox, oy, lw, lh = 330, 880, 820, 540
    c.line(ox, oy, ox, oy - lh, col=INK, sw=3)
    c.line(ox, oy, ox + lw, oy, col=INK, sw=3)
    c.txt(ox - 40, oy - lh - 10, "F", size=36, col=INK, it=True)
    c.txt(ox + lw + 28, oy + 14, "r", size=36, col=INK, it=True, anchor="start")
    r0, F0 = 170.0, 440.0
    pts = []
    for k in range(121):
        r = r0 * (0.75 + k * 0.03)
        f = F0 / (r / r0) ** 2
        if f > lh or r > lw:
            continue
        pts.append((ox + r, oy - f))
    dessins.trait(c, pts, col=NEG, sw=5)
    for i, (mult, lab) in enumerate([(1, "F"), (2, "F / 4"), (3, "F / 9")]):
        if i >= min(pi, 3):
            continue
        r = r0 * mult
        f = F0 / mult ** 2
        c.line(ox, oy - f, ox + r, oy - f, col=SOFT, sw=2, dash="9 9")
        c.line(ox + r, oy, ox + r, oy - f, col=SOFT, sw=2, dash="9 9")
        c.dot(ox + r, oy - f, 11, col=OR)
        c.txt(ox - 16, oy - f + 12, lab, size=30, col=OR, anchor="end")
        c.txt(ox + r, oy + 42, ["r", "2r", "3r"][i], size=30, col=OR, it=True)
    if pi >= 2:
        c.card(1240, 300, 560, 170, col=OR)
        tex.put(c, r"F \propto \frac{1}{r^{2}}", 1520, 385, pt=58)
    if pi >= 3:
        c.txt(1520, 540, "une charge × 2", size=33, col=INK)
        c.txt(1520, 588, "→ la force × 2", size=33, col=ACC, bold=True)
        c.txt(1520, 648, "le carré ne porte", size=30, col=MUT)
        c.txt(1520, 690, "que sur la distance", size=30, col=MUT)
    if pi >= 4:
        c.card(1240, 752, 560, 228, col=NEG, sw=3)
        c.txt(1520, 812, "le piège", size=34, col=NEG, bold=True)
        c.txt(1520, 868, "jamais de centimètres", size=29, col=INK)
        c.txt(1520, 910, "ni de nanocoulombs", size=29, col=INK)
        c.txt(1520, 952, "dans une formule", size=29, col=INK)

# ------------------------------------------------------------------ 6. champ et force
def s_champ(c, pi, t):
    head(c, "Champ et force", "champ")
    sous(c, "Trente secondes de rappel, tout le reste en dépend")
    if pi >= 1:
        c.card(180, 280, 740, 220, col=PALE, sw=3)
        c.txt(550, 330, "le champ : la force par unité de charge", size=29, col=MUT)
        tex.put(c, r"E = \frac{F}{\lvert q \rvert}", 550, 420, pt=56)
    if pi >= 2:
        c.card(1000, 280, 740, 220, col=OR, sw=3)
        c.txt(1370, 330, "la relation retournée, celle qu’on utilise", size=29, col=MUT)
        tex.put(c, r"\vec{F} = q\,\vec{E}", 1370, 420, pt=56)
    if pi >= 3:
        c.txt(CX, 570, "unité du champ :  1 V m⁻¹  =  1 N C⁻¹   (les deux sont justes)",
              size=34, col=INK)
    if pi >= 4:
        for i, (sgn, lab, col) in enumerate([(+1, "charge positive : force dans le sens de E", POS),
                                             (-1, "charge négative : force en sens opposé", NEG)]):
            y = 700 + i * 170
            for k in range(4):
                c.arrow(560 + k * 150, y, 560 + k * 150 + 96, y, col=SOFT, sw=3, head=14)
            c.txt(520, y + 12, "E", size=36, col=SOFT, it=True, anchor="end")
            c.charge(1180, y, sgn, r=32)
            c.arrow(1222, y, 1222 + 150 * sgn, y, col=col, sw=7, head=24)
            c.txt(CX, y + 92, lab, size=31, col=col)

# ------------------------------------------------------------------ 7. le condensateur
def s_condo(c, pi, t):
    head(c, "Le condensateur plan", "condo")
    sous(c, "Deux plaques parallèles : le champ est uniforme")
    condensateur(c, 560, 270, 800, 300, nl=7, U="U" if pi < 3 else "U", dd=True)
    if pi >= 2:
        for i, s in enumerate(["même direction", "même sens", "même valeur"]):
            c.card(430 + i * 370, 630, 330, 74, col=ACC, sw=3)
            c.txt(595 + i * 370, 678, s, size=30, col=INK)
    if pi >= 3:
        c.card(560, 740, 800, 148, col=OR)
        tex.put(c, r"E = \frac{U}{d}", 960, 814, pt=60)
        c.txt(1430, 790, "U en volts", size=29, col=MUT, anchor="start")
        c.txt(1430, 838, "d en mètres", size=29, col=MUT, anchor="start")
    if pi >= 4:
        for k, xx in enumerate((620, 960, 1300)):
            c.charge(xx, 420 - 0 * k, +1, r=24, op=0.9)
            c.arrow(xx, 448, xx, 520, col=ACC, sw=5, head=18)
        c.txt(CX, 920, "la même force partout entre les plaques : en haut, au milieu, en bas",
              size=32, col=ACC)
    if pi >= 5:
        c.txt(CX, 980, "c’est une pente : on descend de U volts en parcourant d mètres",
              size=32, col=MUT)
        c.txt(CX, 1026, "plaques plus proches → champ plus intense, à tension égale",
              size=32, col=MUT)

# ------------------------------------------------------------------ 8. lignes dans le condensateur
def s_lignescondo(c, pi, t):
    head(c, "Les lignes dans le condensateur", "lignescondo")
    sous(c, "La question de cours : trois caractéristiques")
    condensateur(c, 200, 300, 700, 400, nl=6, equi=(pi >= 5), bords=(pi >= 6),
                 zone=(pi >= 6), dd=False, marge=80)
    items = ["perpendiculaires aux plaques",
             "orientées du ⊕ vers le ⊖",
             "parallèles et régulièrement espacées"]
    n = clamp(pi - 1, 0, 3)
    for i, s in enumerate(items):
        if i >= n:
            break
        y = 340 + i * 112
        act = (i == n - 1)
        c.circle(1100, y, 30, col=OR if act else PALE, sw=4, fill="#ffffff")
        c.txt(1100, y + 13, str(i + 1), size=34, col=OR if act else SOFT, bold=True)
        c.txt(1156, y + 13, s, size=31, col=INK if act else MUT, anchor="start")
    if pi >= 1 and pi < 2:
        c.txt(1420, 420, "souvent un point par caractéristique", size=31, col=MUT)
    if pi >= 5:
        c.card(1070, 690, 740, 120, col=ACC, sw=3)
        c.txt(1440, 740, "les équipotentielles : en pointillés,", size=29, col=INK)
        c.txt(1440, 782, "à angle droit des lignes de champ", size=29, col=INK)
    if pi >= 6:
        c.card(230, 860, 1460, 160, col=OR)
        c.txt(CX, 915, "pourquoi « loin des bords » ?", size=34, col=INK, bold=True)
        c.txt(CX, 965, "au bord des plaques, les lignes s’évasent et débordent :", size=31, col=INK)
        c.txt(CX, 1006, "le champ n’y est plus uniforme — seule la région centrale l’est",
              size=31, col=INK)

# ------------------------------------------------------------------ 9. exemple E = U/d
def fig_condo_ex(c, upto, t):
    bx, by, bw, bh = 200, 400, 560, 300
    c.rect(bx, by, bw, 15, fill=POS)
    c.rect(bx, by + bh, bw, 15, fill=NEG)
    c.txt(bx + bw / 2.0, by - 40, "U = 240 V", size=34, col=INK, bold=True)
    c.txt(bx - 32, by + 20, "+", size=46, col=POS, anchor="end")
    c.txt(bx - 32, by + bh + 28, "–", size=52, col=NEG, anchor="end")
    for j in range(5):
        xx = bx + 70 + j * (bw - 140) / 4.0
        c.arrow(xx, by + 24, xx, by + bh - 10, col=POS, sw=4, head=20)
    c.line(bx + bw + 50, by + 15, bx + bw + 50, by + bh, col=MUT, sw=3)
    c.txt(bx + bw + 74, by + bh / 2.0 + 12, "d = 8,0 mm", size=30, col=MUT, anchor="start")
    if upto >= 3:
        c.charge(bx + bw / 2.0, by + bh / 2.0, +1, r=28, col=ACC)
        dessins.chip(c, bx + bw / 2.0 - 150, by + bh / 2.0 - 4, "+5,0 nC", size=27, col=ACC)
    if upto >= 4:
        c.arrow(bx + bw / 2.0, by + bh / 2.0 + 40, bx + bw / 2.0, by + bh / 2.0 + 120,
                col=ACC, sw=7, head=24)
        c.txt(bx + bw / 2.0 + 34, by + bh / 2.0 + 100, "F", size=34, col=ACC, it=True,
              anchor="start")
    c.txt(bx + bw / 2.0, by + bh + 120, "le champ descend du ⊕ vers le ⊖", size=28, col=MUT)

def s_exE(c, pi, t):
    lignes = [r"E = \frac{U}{d}",
              r"d = 8{,}0\ \mathrm{mm} = 8{,}0 \times 10^{-3}\ \mathrm{m}",
              r"E = \frac{240}{8{,}0 \times 10^{-3}} = 3{,}0 \times 10^{4}\ \mathrm{V\,m^{-1}}",
              r"F = q\,E = 5{,}0 \times 10^{-9} \times 3{,}0 \times 10^{4}"]
    exemple(c, "exE", "Exemple — le champ uniforme",
            ["Deux plaques distantes de 8,0 mm, sous une tension de 240 V.",
             "Champ entre les plaques, et force sur une charge de +5,0 nC ?"],
            lignes, max(0, pi - 1), r"F = 1{,}5 \times 10^{-4}\ \mathrm{N}",
            None, fig=fig_condo_ex, t=t)

# ------------------------------------------------------------------ 10. tracer une carte
def s_cartes(c, pi, t):
    head(c, "Tracer une carte de champ", "cartes")
    sous(c, "Cinq règles, et elles suffisent à tout")
    # une charge seule, en rappel
    cx, cy = 520, 620
    chs = [(cx, cy, 1.0)]
    for k in range(12):
        a = 2 * math.pi * (k + 0.5) / 12
        pts = dessins.ligne(chs, cx + 44 * math.cos(a), cy + 44 * math.sin(a),
                            box=(140, 280, 960, 1010))
        dessins.trait(c, pts, col=SOFT, sw=3)
        dessins.tete(c, pts, 0.55, col=SOFT)
    c.charge(cx, cy, +1, r=42)
    c.txt(cx, 1020, "le cas le plus simple : une charge seule", size=29, col=MUT)
    regles = ["elles sortent du ⊕ et entrent dans le ⊖",
              "E est tangent à la ligne ; la flèche donne le sens",
              "elles ne se croisent jamais",
              "serrées = champ intense, écartées = champ faible",
              "perpendiculaires aux surfaces chargées"]
    n = clamp(pi, 0, 5)
    for i, s in enumerate(regles):
        if i >= n:
            break
        y = 330 + i * 104
        act = (i == n - 1)
        c.circle(1070, y, 29, col=OR if act else PALE, sw=4, fill="#ffffff")
        c.txt(1070, y + 12, str(i + 1), size=32, col=OR if act else SOFT, bold=True)
        c.txt(1125, y + 12, s, size=31, col=INK if act else MUT, anchor="start")
    if pi >= 6:
        c.card(1040, 880, 760, 100, col=OR)
        c.txt(1420, 942, "les deux cas du test, maintenant", size=34, col=INK, bold=True)

# ------------------------------------------------------------------ 11. deux charges opposées
def s_dipole(c, pi, t):
    head(c, "Deux charges de signes opposés", "dipole")
    xa, xb, y = 700, 1220, 540
    carte(c, xa, xb, y, +1, -1, n=16, r=44, col=SOFT, sw=3.2,
          box=(60, 240, W - 60, 880))
    c.txt(xa, y + 100, "+Q", size=34, col=POS, it=True)
    c.txt(xb, y + 100, "−Q", size=34, col=NEG, it=True)
    if pi >= 1:
        c.card(110, 250, 470, 112, col=OR)
        c.txt(345, 300, "toutes les lignes vont", size=30, col=INK)
        c.txt(345, 342, "du ⊕ au ⊖, sans exception", size=30, col=INK, bold=True)
    if pi >= 2:
        c.arrow(xa + 48, y, xb - 48, y, col=POS, sw=7, head=24)
        c.card(1360, 250, 460, 112, col=NEG, sw=3)
        c.txt(1590, 300, "sur l’axe : la ligne droite,", size=30, col=INK)
        c.txt(1590, 342, "et le champ le plus fort", size=30, col=INK, bold=True)
    if pi >= 3:
        chip(c, CX, 898, "les autres s’écartent en boucles de plus en plus larges",
             size=31, col=MUT)
    if pi >= 4:
        c.line(260, y, 1660, y, col=ACC, sw=2.5, dash="16 12")
        chip(c, 400, y - 44, "axe de symétrie", size=27, col=ACC)
        chip(c, CX, 952, "figure symétrique : nulle part le champ ne s’annule",
             size=31, col=MUT)
    if pi >= 5:
        xm = (xa + xb) / 2.0
        c.arrow(xm - 80, y - 170, xm + 80, y - 170, col=POS, sw=7, head=24)
        c.card(560, 990, 800, 70, col=OR)
        c.txt(960, 1036, "au milieu : les champs s’additionnent", size=31, col=INK, bold=True)

# ------------------------------------------------------------------ 12. deux charges de même signe
def s_memesigne(c, pi, t):
    head(c, "Deux charges de même signe", "memesigne")
    xa, xb, y = 700, 1220, 540
    carte(c, xa, xb, y, +1, +1, n=15, r=44, col=SOFT, sw=3.2,
          box=(60, 240, W - 60, 880))
    c.txt(xa - 70, y + 86, "+Q", size=34, col=POS, it=True)
    c.txt(xb + 70, y + 86, "+Q", size=34, col=POS, it=True)
    if pi >= 1:
        c.card(120, 250, 440, 112, col=OR)
        c.txt(340, 300, "aucune ligne ne va", size=30, col=INK)
        c.txt(340, 342, "d’une charge à l’autre", size=30, col=INK, bold=True)
    if pi >= 2:
        xm = (xa + xb) / 2.0
        c.circle(xm, y, 34, col=ACC, sw=5, fill="#ffffff")
        c.dot(xm, y, 9, col=ACC)
        c.card(1360, 250, 460, 112, col=ACC, sw=3)
        c.txt(1590, 300, "au milieu : un point", size=30, col=INK)
        c.txt(1590, 342, "où le champ est nul", size=30, col=INK, bold=True)
    if pi >= 3:
        c.card(560, 920, 800, 136, col=ACC, sw=3)
        tex.put(c, r"\vec{E}_1 + \vec{E}_2 = \vec{0}", 960, 972, pt=42, col=ACC)
        c.txt(960, 1034, "égaux et opposés : la somme est nulle, au milieu",
              size=29, col=INK)
    if pi >= 4:
        chip(c, 960, 886, "la région du milieu est vide de lignes", size=30, col=MUT)
    if pi >= 5:
        c.card(110, 390, 470, 116, col=NEG, sw=3)
        c.txt(345, 440, "deux charges négatives :", size=29, col=INK)
        c.txt(345, 482, "même dessin, flèches inversées", size=29, col=INK, bold=True)

# ------------------------------------------------------------------ 13. les deux cartes
def s_cartespieges(c, pi, t):
    head(c, "Les deux cartes côte à côte", "cartespieges")
    sous(c, "C’est ainsi qu’on les retient")
    if pi >= 1:
        carte(c, 240, 640, 500, +1, -1, n=12, r=34, col=SOFT, sw=2.6,
              box=(80, 250, 930, 760), ds=8.0)
        c.txt(440, 300, "signes opposés", size=36, col=INK, bold=True)
        c.txt(440, 800, "les lignes relient les deux charges", size=29, col=MUT)
        c.txt(440, 844, "champ maximal au milieu", size=30, col=POS, bold=True)
    if pi >= 2:
        carte(c, 1280, 1680, 500, +1, +1, n=12, r=34, col=SOFT, sw=2.6,
              box=(990, 250, 1840, 760), ds=8.0)
        c.txt(1480, 300, "mêmes signes", size=36, col=INK, bold=True)
        c.txt(1480, 800, "les lignes s’écartent vers l’extérieur", size=29, col=MUT)
        c.txt(1480, 844, "champ nul au milieu", size=30, col=ACC, bold=True)
        c.circle(1480, 500, 26, col=ACC, sw=4, fill="#ffffff")
        c.dot(1480, 500, 7, col=ACC)
    if pi >= 3:
        c.card(330, 886, 1260, 130, col=NEG, sw=3)
        c.txt(CX, 934, "les trois erreurs qui coûtent des points", size=30, col=NEG, bold=True)
        c.txt(CX, 984, "pas de flèches  ·  deux lignes qui se croisent  ·  "
                       "une ligne qui s’arrête dans le vide", size=28, col=INK)
    if pi >= 4:
        c.txt(CX, 1052, "et les équipotentielles coupent toujours les lignes à angle droit",
              size=31, col=ACC)

# ------------------------------------------------------------------ 14. Millikan : le dispositif
def s_mdisp(c, pi, t):
    head(c, "L’expérience de Millikan", "mdisp")
    if pi <= 1:
        sous(c, "1909 : quelle est la plus petite charge qui existe ?")
    else:
        sous(c, "Le dispositif, pièce par pièce")
    et = 0 if pi < 4 else (2 if pi == 4 else 3)
    dispositif(c, etape=et, t=t, x0=600, y0=292)
    if pi == 1:
        c.card(520, 930, 880, 100, col=OR)
        tex.put(c, r"e = ?", 960, 982, pt=52)
    if pi >= 2 and pi <= 3:
        c.txt(CX, 970, "un brouillard de gouttelettes d’huile au-dessus des plaques",
              size=32, col=MUT)
    if pi >= 4 and pi < 5:
        c.txt(CX, 970, "les rayons X chargent les gouttes, le microscope les montre",
              size=32, col=ACC)
    if pi >= 5:
        c.card(430, 940, 1060, 94, col=OR)
        c.txt(CX, 998, "U est le seul bouton de l’expérience", size=36, col=INK, bold=True)

# ------------------------------------------------------------------ 15. le rôle de chaque pièce
def s_mroles(c, pi, t):
    head(c, "Le rôle de chaque pièce", "mroles")
    sous(c, "Ce que le barème demande d’écrire")
    if pi >= 1:
        c.card(150, 250, 780, 230, col=ACC, sw=3)
        c.txt(540, 304, "les rayons X", size=36, col=ACC, bold=True)
        c.txt(540, 356, "ils ionisent l’air : les gouttes captent", size=29, col=INK)
        c.txt(540, 398, "ou perdent quelques électrons", size=29, col=INK)
        c.txt(540, 448, "sans eux, les gouttes sont neutres", size=27, col=MUT)
    if pi >= 2:
        c.card(990, 250, 780, 230, col=MUT, sw=3)
        c.txt(1380, 304, "le microscope", size=36, col=INK, bold=True)
        c.txt(1380, 356, "les gouttes mesurent quelques µm :", size=29, col=INK)
        c.txt(1380, 398, "il montre une goutte isolée, son rayon", size=29, col=INK)
        c.txt(1380, 448, "donc sa masse — et son mouvement", size=27, col=MUT)
    cas = [("monte", 150, 80, ACC), ("descend", 80, 150, MUT), ("immobile", 118, 118, OR)]
    for i, (lab, fe, fg, col) in enumerate(cas):
        if i >= clamp(pi - 2, 0, 3):
            break
        x = 420 + i * 540
        y = 690
        c.rect(x - 150, y - 180, 300, 11, fill=POS)
        c.rect(x - 150, y + 180, 300, 11, fill=NEG)
        dy = (14 * math.sin(2 * math.pi * t) * (1 if lab == "monte" else -1)
              if lab != "immobile" else 0)
        bilan(c, x, y + dy, fe, fg, lab=False)
        c.txt(x, y + 240, lab, size=36, col=col, bold=True)
        tex.put(c, {"monte": r"q\,E > m\,g", "descend": r"q\,E < m\,g",
                    "immobile": r"q\,E = m\,g"}[lab], x, y + 288, pt=32, col=MUT)
    if pi >= 5:
        c.card(300, 1004, 1320, 62, col=OR)
        c.txt(CX, 1046, "seule la goutte immobile permet de calculer la charge",
              size=32, col=INK, bold=True)

# ------------------------------------------------------------------ 16. la démonstration
def s_mdemo(c, pi, t):
    head(c, "La démonstration à savoir", "mdemo")
    sous(c, "Trois points au barème, trois lignes")
    bx, by, bw, bh = 180, 330, 520, 420
    c.rect(bx, by, bw, 15, fill=POS)
    c.rect(bx, by + bh, bw, 15, fill=NEG)
    c.txt(bx - 30, by + 20, "+", size=46, col=POS, anchor="end")
    c.txt(bx - 30, by + bh + 28, "–", size=52, col=NEG, anchor="end")
    c.line(bx + bw + 50, by + 15, bx + bw + 50, by + bh, col=MUT, sw=3)
    c.txt(bx + bw + 74, by + bh / 2.0 + 12, "d", size=38, col=MUT, it=True, anchor="start")
    bilan(c, bx + bw / 2.0, by + bh / 2.0, 130, 130)
    c.txt(bx + bw / 2.0, by + bh + 74, "la goutte est immobile", size=31, col=INK)
    lignes = [r"q\,E = m\,g",
              r"q\,\frac{U}{d} = m\,g",
              r"q = \frac{m\,g\,d}{U}"]
    n = clamp(pi - 1, 0, 3)
    for i, f in enumerate(lignes):
        if i >= n:
            break
        y = 370 + i * 190
        act = (i == n - 1)
        c.card(880, y - 80, 880, 160, col=OR if act else PALE, sw=4 if act else 2)
        tex.put(c, f, 1130, y, pt=54 if act else 46, col=INK if act else MUT)
        c.txt(1530, y + 10, ["les forces se compensent", "E = U / d entre les plaques",
                             "on isole q"][i], size=26, col=MUT)
    if pi >= 5:
        c.card(180, 960, 1580, 86, col=ACC)
        c.txt(CX, 1014, "plus la goutte est lourde, plus il faut de charge ; "
                        "plus U est grand, moins il en faut", size=32, col=INK)

# ------------------------------------------------------------------ 17. interpréter le graphique
def s_mgraphe(c, pi, t):
    head(c, "Interpréter les résultats", "mgraphe")
    sous(c, "Les charges mesurées sur 50 gouttelettes")
    nuage(c, 300, 250, 1080, 520, nmax=5, pal=(pi >= 1), labe=(pi >= 3))
    if pi >= 1:
        c.txt(840, 884, "des droites horizontales, pas un nuage au hasard", size=32, col=OR)
    if pi >= 2:
        c.txt(840, 932, "les valeurs intermédiaires ne se rencontrent jamais",
              size=32, col=MUT)
    if pi >= 3:
        c.card(1480, 300, 380, 150, col=OR)
        tex.put(c, r"q = n\,e", 1670, 375, pt=56)
        c.txt(1670, 492, "n entier", size=30, col=MUT)
    if pi >= 4:
        c.card(1480, 530, 380, 170, col=PALE, sw=3)
        c.txt(1670, 582, "la charge", size=30, col=MUT)
        c.txt(1670, 624, "élémentaire", size=30, col=MUT)
        tex.put(c, r"e = 1{,}6 \times 10^{-19}\ \mathrm{C}", 1670, 674, pt=26, maxw=350)
        c.txt(1670, 746, "les écarts : les", size=27, col=MUT)
        c.txt(1670, 784, "incertitudes de mesure", size=27, col=MUT)
    if pi >= 5:
        c.card(230, 980, 1460, 80, col=ACC)
        c.txt(CX, 1030, "des sachets de pièces de 2 € : 2, 4, 6 € — jamais 3,40 €.  "
                        "Les paliers prouvent la pièce élémentaire.", size=27, col=INK)

# ------------------------------------------------------------------ 18. l'analyse des données
def s_mtable(c, pi, t):
    head(c, "L’analyse des données", "mtable")
    sous(c, "Six gouttelettes, des plaques à d = 2,76 mm")
    cols = ["gouttelette", "1", "2", "3", "4", "5", "6"]
    lig = [["U / V", "52", "174", "88", "117", "138", "92"],
           ["m / 10⁻¹⁶ kg", "6,16", "10,2", "15,4", "7,05", "16,7", "22,0"]]
    tableau(c, 210, 250, cols, lig, cw=[300] + [200] * 6, rh=58, size=30,
            hlc=(1,) if pi >= 3 else ())
    if pi >= 2:
        c.card(430, 470, 1060, 130, col=OR)
        c.txt(960, 512, "étape 1 : la charge de chaque goutte", size=29, col=MUT)
        tex.put(c, r"q = \frac{m\,g\,d}{U}", 960, 568, pt=46)
    if pi >= 3:
        tex.put(c, r"q_1 = \frac{6{,}16 \times 10^{-16} \times 9{,}81 \times "
                   r"2{,}76 \times 10^{-3}}{52}", CX, 690, pt=40, maxw=1500)
    if pi >= 4:
        c.card(560, 760, 800, 110, col=ACC)
        tex.put(c, r"q_1 = 3{,}21 \times 10^{-19}\ \mathrm{C}", CX, 815, pt=46)
    if pi >= 5:
        c.card(230, 900, 1460, 140, col=NEG, sw=3)
        c.txt(CX, 950, "les deux seuls pièges, et ils sont d’unités", size=32, col=NEG, bold=True)
        c.txt(CX, 998, "la masse est en 10⁻¹⁶ kg  ·  la distance est en millimètres : "
                       "d = 2,76 × 10⁻³ m", size=31, col=INK)

# ------------------------------------------------------------------ 19. trouver e
def s_mresult(c, pi, t):
    head(c, "Trouver la charge élémentaire", "mresult")
    cols = ["gouttelette", "1", "2", "3", "4", "5", "6"]
    lig = [["U / V", "52", "174", "88", "117", "138", "92"],
           ["m / 10⁻¹⁶ kg", "6,16", "10,2", "15,4", "7,05", "16,7", "22,0"],
           ["q / 10⁻¹⁹ C", "3,21", "1,59", "4,74", "1,63", "3,28", "6,47"]]
    if pi >= 5:
        lig.append(["q / q₂,₄", "1,99", "0,99", "2,94", "1,01", "2,04", "4,02"])
    if pi >= 6:
        lig.append(["n", "2", "1", "3", "1", "2", "4"])
    tableau(c, 210, 170, cols, lig, cw=[300] + [200] * 6, rh=58, size=30,
            hl=len(lig) - 1 if pi >= 6 else None,
            hlc=(2, 4) if 2 <= pi <= 4 else ())
    y0 = 170 + 58 * (len(lig) + 1) + 40
    if pi >= 2:
        c.txt(CX, y0 + 20, "étape 2 : la plus petite valeur — les gouttes 2 et 4 "
                           "sont au même palier", size=33, col=INK)
    if pi >= 3:
        c.card(430, y0 + 56, 1060, 124, col=OR)
        tex.put(c, r"q_{2,4} = \frac{1{,}59 + 1{,}63}{2} \times 10^{-19} "
                   r"\approx 1{,}61 \times 10^{-19}\ \mathrm{C}", CX, y0 + 118, pt=40,
                maxw=1000)
        c.txt(CX, y0 + 216, "on moyenne les deux mesures du même palier : l’erreur diminue",
              size=30, col=MUT)
    if pi >= 4 and pi < 6:
        c.txt(CX, y0 + 272, "étape 3 : diviser toutes les charges par cette valeur",
              size=33, col=ACC, bold=True)
    if pi >= 6 and pi < 7:
        c.txt(CX, y0 + 272, "étape 4 : dans la marge d’erreur, ce sont tous des entiers",
              size=33, col=ACC, bold=True)
    if pi >= 7:
        c.card(330, y0 + 236, 1260, 100, col=ACC)
        tex.put(c, r"q = n\,e \quad\text{avec}\quad e \approx 1{,}61 \times 10^{-19}\ \mathrm{C}",
                CX, y0 + 288, pt=42, maxw=1160)
    if pi >= 8:
        c.txt(CX, y0 + 376, "valeur admise : 1,602 × 10⁻¹⁹ C — moins de 1 % d’écart",
              size=32, col=MUT)

# ------------------------------------------------------------------ 20. quantifié
def s_quant(c, pi, t):
    head(c, "Quantifié, au sens précis", "quant")
    sous(c, "Le mot, et sa définition exacte")
    if pi >= 1:
        c.txt(CX, 268, "une grandeur quantifiée ne prend que certaines valeurs isolées,",
              size=34, col=INK)
        c.txt(CX, 314, "jamais les valeurs intermédiaires", size=34, col=INK)
    if pi >= 2:
        escalier(c, 260, 400, 480, 330)
        c.txt(500, 776, "l’escalier : quantifié", size=32, col=OR, bold=True)
        c.txt(500, 822, "on ne se tient que sur les marches", size=28, col=MUT)
        c.txt(500, 884, "la rampe : continu", size=32, col=SOFT, bold=True)
        c.txt(500, 930, "toutes les hauteurs sont permises", size=28, col=MUT)
    if pi >= 3:
        c.card(900, 400, 880, 170, col=OR)
        tex.put(c, r"x = a \cdot f(n) \quad\text{avec } n \text{ entier}", 1340, 485,
                pt=44, maxw=820)
        c.txt(1340, 606, "a est une constante, f une fonction de l’entier n", size=30, col=MUT)
    if pi >= 4:
        c.card(900, 660, 880, 120, col=ACC, sw=3)
        c.txt(1340, 706, "pour la charge électrique :", size=30, col=MUT)
        tex.put(c, r"f(n) = n \quad\Rightarrow\quad q = n\,e", 1340, 752, pt=38, maxw=800)
    if pi >= 5:
        c.txt(1340, 850, "mais ce n’est pas toujours n :", size=32, col=INK)
        tex.put(c, r"n \qquad n^{2} \qquad \frac{1}{n} \qquad \frac{1}{n^{2}}",
                1340, 940, pt=48, maxw=820)
        c.txt(1340, 1020, "il faut savoir trouver laquelle", size=30, col=OR)

# ------------------------------------------------------------------ 21. quelle fonction de n
def s_famille(c, pi, t):
    head(c, "Quelle fonction de n ?", "famille")
    sous(c, "La méthode : diviser par f(n) et chercher la colonne constante", size=36)
    cols = ["", "n = 1", "n = 2", "n = 3", "n = 4"]
    toutes = [["mesure (eV)", "13,6", "3,40", "1,51", "0,85"],
              ["mesure / n", "13,6", "1,70", "0,503", "0,212"],
              ["mesure / n²", "13,6", "0,850", "0,168", "0,053"],
              ["mesure × n", "13,6", "6,80", "4,53", "3,40"],
              ["mesure × n²", "13,6", "13,6", "13,6", "13,6"]]
    nl = 0
    if pi >= 4:
        nl = 1
    if pi >= 5:
        nl = 2
    if pi >= 6:
        nl = 3
    if pi >= 7:
        nl = 4
    if pi >= 8:
        nl = 5
    if nl:
        tableau(c, 300, 300, cols, toutes[:nl], cw=[420] + [260] * 4, rh=62, size=31,
                hl=4 if pi >= 8 else None)
    if pi >= 1 and pi < 4:
        etapes = ["ranger les mesures dans l’ordre, et poser n = 1, 2, 3, 4",
                  "diviser chaque mesure par f(n), pour chaque candidate",
                  "la colonne constante donne la bonne fonction — et la constante a"]
        puces(c, etapes, clamp(pi, 0, 3), 420, 420, dy=110, size=36)
        tex.put(c, r"n \qquad n^{2} \qquad \frac{1}{n} \qquad \frac{1}{n^{2}}",
                CX, 800, pt=52, maxw=900)
        c.txt(CX, 900, "les quatre candidates habituelles", size=30, col=MUT)
    if pi >= 4:
        c.txt(CX, 760, "les niveaux d’énergie de l’atome d’hydrogène", size=32, col=MUT)
    if pi == 5:
        c.txt(CX, 816, "diviser par n : ça diminue — ce n’est pas n", size=34, col=NEG)
    if pi == 6:
        c.txt(CX, 816, "diviser par n² : ça diminue encore plus vite", size=34, col=NEG)
    if pi == 7:
        c.txt(CX, 816, "multiplier par n (diviser par 1/n) : toujours pas constant",
              size=34, col=NEG)
    if pi == 8:
        c.txt(CX, 816, "multiplier par n² (diviser par 1/n²) : constant !", size=36,
              col=ACC, bold=True)
    if pi >= 9:
        c.card(330, 824, 1260, 212, col=OR)
        c.txt(CX, 876, "la phrase à écrire", size=32, col=INK, bold=True)
        c.txt(CX, 926, "l’énergie ne prend que des valeurs discrètes, et elle est",
              size=32, col=INK)
        tex.put(c, r"\text{proportionnelle à } \frac{1}{n^{2}}", CX, 992, pt=38, maxw=800)

# ------------------------------------------------------------------ 22. pourquoi c'est important
def s_pourquoi(c, pi, t):
    head(c, "Pourquoi c’est important", "pourquoi")
    sous(c, "La question à deux points, et sa réponse")
    if pi >= 1:
        c.card(170, 280, 740, 300, col=SOFT, sw=3)
        c.txt(540, 338, "physique classique", size=38, col=MUT, bold=True)
        c.txt(540, 396, "toutes les grandeurs sont", size=30, col=INK)
        c.txt(540, 438, "supposées continues", size=30, col=INK)
        escalier(c, 390, 470, 300, 80, rampe=True)
        c.txt(540, 606, "une rampe : toutes les valeurs", size=28, col=MUT)
    if pi >= 2:
        c.card(1010, 280, 740, 300, col=OR, sw=3)
        c.txt(1380, 338, "physique quantique", size=38, col=INK, bold=True)
        c.txt(1380, 396, "certaines grandeurs ne vont", size=30, col=INK)
        c.txt(1380, 438, "que par paquets", size=30, col=INK)
        escalier(c, 1230, 470, 300, 80, rampe=False)
        c.txt(1380, 606, "un escalier : des marches", size=28, col=MUT)
        c.txt(CX, 680, "la charge électrique est la première grandeur dont on prouve",
              size=34, col=INK)
        c.txt(CX, 726, "expérimentalement la quantification", size=34, col=INK, bold=True)
    if pi >= 3:
        for i, s in enumerate(["l’énergie de la lumière : les photons",
                               "les niveaux d’énergie des atomes"]):
            c.card(390 + i * 580, 790, 560, 86, col=ACC, sw=3)
            c.txt(670 + i * 580, 842, s, size=28, col=INK)
        c.txt(CX, 920, "on a ensuite trouvé bien d’autres grandeurs quantifiées",
              size=31, col=MUT)
    if pi >= 4:
        c.card(330, 960, 1260, 86, col=OR)
        c.txt(CX, 1014, "Millikan, prix Nobel 1923 : le premier exemple de quantification",
              size=33, col=INK, bold=True)

# ------------------------------------------------------------------ 23. la fiche
def s_fiche(c, pi, t):
    head(c, "La fiche de révision", "fiche")
    sous(c, "Cinq lignes, et tu as l’essentiel", y=190)
    forms = [(r"F = k\,\frac{\lvert Q \rvert\,\lvert q \rvert}{r^{2}}", "la force de Coulomb",
              "k = 9,0 × 10⁹ SI · r en mètres · mêmes signes : répulsion"),
             (r"E = \frac{F}{\lvert q \rvert} \qquad \vec{F} = q\,\vec{E}",
              "le champ, et la force qu’il exerce",
              "E en V m⁻¹ = N C⁻¹ · charge négative : force en sens opposé"),
             (r"E = \frac{U}{d}", "le champ uniforme entre deux plaques",
              "U en volts · d en mètres · même direction, même sens, même valeur"),
             (r"q\,E = m\,g \;\Rightarrow\; q = \frac{m\,g\,d}{U}",
              "la goutte de Millikan en suspension",
              "valable seulement quand la goutte est immobile"),
             (r"q = n\,e", "la charge est quantifiée",
              "e = 1,60 × 10⁻¹⁹ C · n entier · diviser par la plus petite valeur")]
    n = clamp(pi, 0, 5)
    for i, (f, d, leg) in enumerate(forms):
        if i >= n:
            break
        y = 250 + i * 158
        act = (i == n - 1)
        c.card(150, y, 1620, 142, col=OR if act else PALE, sw=4 if act else 2)
        tex.put(c, f, 420, y + 72, pt=40, maxw=440)
        c.txt(700, y + 58, d, size=31, col=INK, anchor="start", bold=True)
        c.txt(700, y + 104, leg, size=25, col=MUT, anchor="start")

# ------------------------------------------------------------------ 24. avant de rendre
def s_final(c, pi, t):
    head(c, "Avant de rendre la copie", "final")
    sous(c, "La liste de contrôle, à relire cinq minutes avant")
    items = ["les unités SI avant tout calcul : m, kg, C, V",
             "le carré de la distance porte aussi sur la puissance de 10",
             "les lignes de champ : des flèches, aucun croisement, perpendiculaires",
             "« uniforme » = même direction, même sens, même valeur",
             "analyse de données : la plus petite valeur, on divise, les rapports sont entiers"]
    n = clamp(pi, 0, 5)
    for i, s in enumerate(items):
        if i >= n:
            break
        y = 300 + i * 116
        act = (i == n - 1)
        c.card(200, y, 1520, 96, col=OR if act else PALE, sw=4 if act else 2)
        c.path("M%.1f %.1f L%.1f %.1f L%.1f %.1f" % (268, y + 48, 282, y + 64, 308, y + 30),
               col=OR if act else ACC, sw=6)
        c.txt(350, y + 60, s, size=32, col=INK if act else MUT, anchor="start")
    if pi >= 6:
        c.txt(CX, 1000, "Tu as les six points.", size=46, col=INK, bold=True)
        c.txt(CX, 1056, "Bon test.", size=40, col=OR, bold=True)

SCENES = {"titre": s_titre, "prog": s_prog, "coulomb": s_coulomb, "exC": s_exC,
          "carre": s_carre, "champ": s_champ, "condo": s_condo,
          "lignescondo": s_lignescondo, "exE": s_exE, "cartes": s_cartes,
          "dipole": s_dipole, "memesigne": s_memesigne, "cartespieges": s_cartespieges,
          "mdisp": s_mdisp, "mroles": s_mroles, "mdemo": s_mdemo, "mgraphe": s_mgraphe,
          "mtable": s_mtable, "mresult": s_mresult, "quant": s_quant,
          "famille": s_famille, "pourquoi": s_pourquoi, "fiche": s_fiche, "final": s_final}
