#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Construit cours-champ-electrique.html (site autonome) a partir de champ-electrique.md.
   Usage : python3 build-site.py"""
import os, re, subprocess, html, sys, shutil, tempfile

ROOT = os.path.dirname(os.path.abspath(__file__))
MD   = os.path.join(ROOT, "champ-electrique.md")
OUT  = os.path.join(ROOT, "cours-champ-electrique.html")
FIGS = os.path.join(ROOT, "figures")
VEND = os.path.join(ROOT, "vendor")
KCSS = os.path.join(VEND, "katex.inline.css")
KJS  = os.path.join(VEND, "katex.min.js")
# KaTeX rend les formules exactement comme LaTeX ; sans node ni vendor/, on retombe sur MathML
KATEX = bool(shutil.which("node")) and os.path.exists(KCSS) and os.path.exists(KJS)
# identifiant YouTube de la vidéo du chapitre (vidéo non répertoriée) ; "" = pas de page vidéo.
# C'est la seule ressource externe de la page : check-site.py la tolère explicitement.
VIDEO_YT = ""

# ---------------------------------------------------------------- markdown -> html
def pandoc(md):
    if not md.strip():
        return ""
    md = re.sub(r"\\boxed\{\\;?(.*?)\\;?\}", r"\1", md, flags=re.S)   # menclose mal supporté
    r = subprocess.run(["pandoc", "-f", "markdown", "-t", "html5", "--wrap=none",
                        "--katex" if KATEX else "--mathml"],
                       input=md, capture_output=True, text=True)
    if r.returncode:
        sys.exit("pandoc: " + r.stderr)
    return r.stdout

SVG_CACHE = {}
def inline_svg(name):
    if name not in SVG_CACHE:
        s = open(os.path.join(FIGS, name), encoding="utf-8").read()
        s = re.sub(r"<style>.*?</style>", "", s, flags=re.S)        # pas de variante sombre
        s = re.sub(r"<title>.*?</title>", "", s, flags=re.S)
        s = s.replace("<svg ", '<svg class="figsvg" ', 1)
        # on garde width/height : avec max-width:100% + height:auto, le SVG reste responsive
        SVG_CACHE[name] = s.strip()
    return SVG_CACHE[name]

def embed_figures(h):
    def rep(m):
        name = m.group(1)
        if not os.path.exists(os.path.join(FIGS, name)):
            return m.group(0)
        return inline_svg(name)
    return re.sub(r'<img src="figures/([^"]+)"[^>]*/?>', rep, h)

def classify(h):
    """donne une couleur aux encadres selon leur premier mot-cle"""
    def rep(m):
        t = m.group(2)
        cls = "note"
        if t.startswith("En clair"):
            cls = "enclair"
        elif t.startswith("TL;DR"):
            cls = "tldr"
        elif t.startswith(("À retenir pour les exercices", "Comment choisir sa formule",
                           "Ce que ça fait travailler", "Par où commencer")):
            cls = "pourexos"
        elif t.startswith(("À retenir", "L'idée clé", "Le point remarquable", "Moyen mnémotechnique",
                           "Conséquence utile", "Astuce", "Le point important")):
            cls = "retenir"
        elif t.startswith(("Exemple résolu", "Corrigé")):
            cls = "exemple"
        return '<blockquote class="%s">%s<strong>%s</strong>' % (cls, m.group(1), t)
    return re.sub(r"<blockquote>(\s*<p>)<strong>([^<]*)</strong>", rep, h)

def H(md):
    return classify(embed_figures(pandoc(md)))

# ---------------------------------------------------------------- decoupage du markdown
src = open(MD, encoding="utf-8").read()
src = re.sub(r"\A---\n.*?\n---\n", "", src, flags=re.S)             # front matter

def split_on(text, level):
    """decoupe en [(titre, corps)] sur les titres de niveau donne ; le preambule a pour titre None"""
    pat = re.compile(r"^#{%d} (.+)$" % level, re.M)
    out, last, title = [], 0, None
    for m in pat.finditer(text):
        out.append((title, text[last:m.start()]))
        title, last = m.group(1).strip(), m.end()
    out.append((title, text[last:]))
    return [(t, b) for t, b in out if t is not None or b.strip()]

parties = dict()
order = []
for title, body in split_on(src, 1):
    key = title if title else "__intro__"
    parties[key] = body
    order.append(key)

def clean(md):
    return re.sub(r"\n---\n", "\n", md).strip()

PAGES = []          # (id, group, title, html, kind)  kind: cours | exo | sol
def add(pid, group, title, body_html, kind="cours", extra=None):
    PAGES.append(dict(id=pid, group=group, title=title, html=body_html, kind=kind, extra=extra or {}))

def plain(t):
    """enleve le balisage mathematique pour l'affichage dans le menu"""
    def m2(m):
        x = m.group(1)
        x = re.sub(r"\\vec\{([^}]*)\}", r"\1", x)
        x = re.sub(r"\\mathrm\{([^}]*)\}", r"\1", x)
        x = re.sub(r"[\\{}_]", "", x)
        return x
    return re.sub(r"\$([^$]*)\$", m2, t)

def slug(s):
    s = re.sub(r"[^a-z0-9]+", "-", s.lower().replace("é", "e").replace("è", "e").replace("ê", "e")
               .replace("à", "a").replace("ô", "o").replace("û", "u").replace("ç", "c"))
    return s.strip("-")[:48]

# ---------------------------------------------------------------- encadrés de synthèse
# Le cours porte ses TL;DR et ses « à retenir » dans champ-electrique.md lui-même.
# Ici, seulement les pages construites morceau par morceau : énoncés et corrigés.
EXO_TLDR = {
 "exos-infos":  "Les constantes, les données et les conventions à utiliser dans tous les exercices qui suivent, et la provenance des énoncés.",
 "ex-5":        "Superposition : deux charges, un point, et le champ résultant à construire vecteur par vecteur.",
 "ex-thomson":  "L'électron dans un champ uniforme : $E = U/d$, puis $F = qE$, puis la déviation.",
 "ex-bac":      "Sujet complet de Bac : champ entre deux plaques, force sur une charge, et la gouttelette de Millikan.",
 "ex-autotest": "Dix questions courtes pour vérifier, en dix minutes, que tout le chapitre est en place.",
 "g-1":  "Vocabulaire et définitions : un texte à compléter sur la charge, le champ et le potentiel.",
 "g-2":  "L'analogie pesanteur / électricité : ce qui se correspond, et la différence qui reste.",
 "g-3":  "Pourquoi un déplacement le long d'une équipotentielle ne coûte aucun travail.",
 "g-4":  "La technique du rapport sur $F = kQq/r^{2}$ : répondre sans calculatrice.",
 "g-5":  "La loi de Coulomb prise à l'envers : de la force à la charge, puis au nombre d'électrons.",
 "g-6":  "La force électrique dans l'atome d'hydrogène, comparée à l'attraction gravitationnelle.",
 "g-7":  "Le champ d'une charge ponctuelle à deux distances : le $1/r^{2}$ en action.",
 "g-8":  "Application directe de $F = qE$.",
 "g-9":  "Superposition sur un axe : deux charges de même signe, au milieu du segment puis ailleurs.",
 "g-10": "Champ uniforme entre deux plaques : $E = U/d$, puis la force sur une charge.",
 "g-11": "Le seuil de claquage de l'air utilisé comme condition : quelle tension, quelle distance ?",
 "g-12": "Une sphère chargée vue de l'extérieur : son champ et son potentiel de surface.",
 "g-13": "Chercher le point où le champ résultant de deux charges s'annule exactement.",
 "g-14": "Le potentiel d'une sphère conductrice isolée : $V = kQ/r$.",
 "g-15": "Le potentiel en $1/r$, et le champ obtenu comme pente du potentiel.",
 "g-16": "QCM : les potentiels s'additionnent comme des nombres, pas comme des vecteurs.",
 "g-17": "Le travail d'un déplacement dans le champ d'une charge ponctuelle : $W = q\\,\\Delta V$.",
 "g-18": "Entre deux plaques, le potentiel varie linéairement : lire un potentiel intermédiaire.",
 "g-19": "L'expérience de Millikan : la gouttelette immobile, $qE = mg$, et la charge quantifiée.",
 "g-20": "L'expérience de Thomson : un faisceau d'électrons dévié entre deux plaques.",
 "g-21": "Question de cours : le pulvérisateur de peinture électrostatique.",
 "g-22": "Question de cours : les équipotentielles et le danger de l'orage.",
}
SOL_RETENIR = {
 "sol-5":        "On projette chaque champ sur $x$ et sur $y$, on additionne coordonnée par coordonnée, puis Pythagore : c'est la seule méthode qui ne se trompe jamais sur un angle.",
 "sol-6":        "L'ordre attendu par le barème : formule en lettres, conversion en unités SI, et seulement ensuite les valeurs.",
 "sol-thomson":  "$E = U/d$ donne le champ, $F = qE$ la force ; l'électron étant négatif, il est dévié **vers la plaque positive**.",
 "sol-bac":      "Un sujet long se traite en enchaînant trois relations connues : $E = U/d$, $F = qE$, puis l'équilibre $qE = mg$. Vérifier l'unité à chaque étape.",
 "sol-autotest": "Tout le chapitre tient dans cinq relations : $F = k\\lvert Q \\rvert \\lvert q \\rvert/r^{2}$, $E = F/\\lvert q \\rvert$, $E = k\\lvert Q \\rvert/r^{2}$, $E = U/d$ et $W = q\\,\\Delta V$.",
 "gsol-1":  "Savoir redonner la définition **et** l'unité de la charge, du champ et du potentiel : c'est la moitié des points d'une question de cours.",
 "gsol-2":  "$\\vec{P} = m\\,\\vec{g}$ et $\\vec{F} = q\\,\\vec{E}$ ont la même forme ; la différence est dans le signe, car une masse ne peut pas repousser.",
 "gsol-3":  "Le long d'une équipotentielle, $\\Delta V = 0$ donc $W = q\\,\\Delta V = 0$ : aucun travail, quel que soit le chemin suivi.",
 "gsol-4":  "Quand l'énoncé ne demande qu'un rapport, ne rien calculer : distance $\\times n$ → force $\\div n^{2}$, charge $\\times n$ → force $\\times n$.",
 "gsol-5":  "De la force à la charge : $q = \\sqrt{F r^{2}/k}$, puis $n = q/e$ pour le nombre d'électrons.",
 "gsol-6":  "À l'échelle de l'atome, la force électrique écrase la gravitation d'environ 39 ordres de grandeur.",
 "gsol-7":  "Deux fois plus loin, quatre fois plus faible : c'est la signature du $1/r^{2}$.",
 "gsol-8":  "$F = qE$ — et convertir les nC en C **avant** de multiplier.",
 "gsol-9":  "Sur un axe, on additionne des valeurs **signées** : deux champs de sens opposés se soustraient, de même sens s'ajoutent.",
 "gsol-10": "$E = U/d$ avec $U$ en volts et $d$ en mètres ; entre les plaques, la force sur une charge est la même partout.",
 "gsol-11": "On écrit la condition $E = 3{,}0 \\times 10^{6}\\ \\mathrm{V\\,m^{-1}}$ et on en déduit l'inconnue : c'est un exercice d'inversion de formule.",
 "gsol-12": "Pour une sphère, tout se passe comme si la charge était au centre : $E = k\\lvert Q \\rvert/r^{2}$ et $V = kQ/r$, avec $r$ compté depuis le centre.",
 "gsol-13": "Un point nul se trouve en écrivant l'égalité des deux normes ; il est toujours plus proche de la **plus petite** charge.",
 "gsol-14": "$V = kQ/r$ : le potentiel d'un conducteur chargé est le même partout, surface comprise.",
 "gsol-15": "$V$ varie en $1/r$ (doubler la distance divise $V$ par 2, mais $E$ par 4), et le champ est la pente : $E = -\\Delta V/\\Delta r$.",
 "gsol-16": "Les potentiels s'additionnent comme de simples nombres — même aux endroits où les champs, eux, s'annulent.",
 "gsol-17": "$W = q\\,\\Delta V$, avec $\\Delta V$ calculé par $V = kQ/r$ aux deux distances ; surveiller le signe de $Q$.",
 "gsol-18": "Entre deux plaques, $V$ décroît linéairement : un potentiel intermédiaire se lit par proportionnalité.",
 "gsol-19": "La gouttelette immobile donne $qE = mg$, soit $q = mgd/U$ ; on compare ensuite à $e$ pour trouver le nombre de charges.",
 "gsol-20": "Même enchaînement que chez Thomson : $E = U/d$, $F = qE$, puis la cinématique si la déviation est demandée.",
 "gsol-21": "Deux effets à citer, pas un : la répulsion mutuelle des gouttes, et l'influence sur l'objet relié à la terre.",
 "gsol-22": "Raisonner en équipotentielles : elles se resserrent autour du point le plus haut, donc le champ y est maximal.",
}

def box(cls, label, texte):
    """le texte passe par pandoc : les $...$ deviennent des formules, comme dans le .md"""
    inner = pandoc(texte).strip()
    inner = re.sub(r"^<p>", "", inner)
    inner = re.sub(r"</p>$", "", inner)
    return ('<blockquote class="%s"><p><strong>%s</strong> %s</p></blockquote>'
            % (cls, label, inner))

def put_tldr(h, texte):
    """insère l'encadré juste après le titre de la page"""
    m = re.search(r"</h2>", h)
    bx = box("tldr", "Ce que ça fait travailler.", texte)
    return (h[:m.end()] + "\n" + bx + h[m.end():]) if m else bx + h

# ---- accueil
intro = clean(parties.get("__intro__", ""))
intro = re.sub(r"^# Champ électrique\s*", "", intro)
intro = intro.split("### Comment utiliser ce document")[0]
intro += """
> **TL;DR.** Tout le chapitre « Champ électrique » de S6, découpé en une page par notion : d'abord **comprendre** (ce qu'est une charge, une force à distance, un vecteur, un champ, une tension), puis le **cours** officiel, ses **applications**, et enfin **27 exercices corrigés**. Chaque page commence par un résumé et finit par un encadré orange qui rassemble ce qu'il faut pour faire les exercices.

### Comment utiliser ce site

- Le **menu de gauche** donne accès à chaque notion, une par page. Le champ de recherche en haut du menu filtre la liste.
- Les touches **←** et **→** (ou les boutons en bas de page) font défiler les pages dans l'ordre.
- Les **énoncés** d'exercices et leurs **solutions** sont dans deux rubriques séparées : on peut donc chercher d'abord, puis cliquer sur *Voir la solution*.
- Beaucoup de figures sont **animées** : les flèches bougent, les vecteurs s'allongent, les constructions se font pas à pas. Rien à cliquer, elles tournent en boucle.
- Les formules importantes sont dans un **encadré jaune**, les explications en langage courant dans un encadré **bleu**.

> **Au fait.** Ce site est produit automatiquement à partir du fichier `champ-electrique.md` : modifier le cours et relancer `python3 build-site.py` suffit à le régénérer.

> **Par où commencer.**
>
> - Tu n'as jamais fait d'électrostatique → la rubrique **Les bases**, dans l'ordre, de A.1 à A.11.
> - Tu dois réviser avant un contrôle → **Méthode** (les 5 étapes, les erreurs classiques), puis le **Formulaire**, puis l'**auto-test**.
> - Tu veux t'entraîner → **Exercices** : les énoncés d'abord, les corrigés sont dans une rubrique séparée.
> - Tu bloques sur une formule → le **Formulaire** donne la relation, et le **lexique** (A.11) donne le sens de chaque symbole.
"""
add("accueil", "Pour commencer", "Accueil", H(intro))

# ---- la vidéo du chapitre (hébergée sur YouTube, non répertoriée)
if VIDEO_YT:
    add("video", "Pour commencer", "La vidéo du chapitre", H("""## La vidéo du chapitre

> **TL;DR.** Vingt minutes qui reprennent tout le chapitre dans l'ordre, avec un exemple chiffré
> résolu après chaque notion. Fil directeur : la gouttelette d'encre d'une imprimante à jet
> d'encre, posée en énigme au début et calculée entièrement à la fin.

<div class="ytbox"><iframe src="https://www.youtube-nocookie.com/embed/%s" title="Champ électrique — cours complet" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe></div>

Les sous-titres français sont disponibles dans le lecteur. La vidéo ne remplace pas les pages :
elle donne le fil, les pages donnent le détail et les exercices.

> **À retenir pour les exercices**
>
> - La vidéo suit exactement l'ordre du menu de gauche : charge, loi de Coulomb, vecteur, champ,
>   lignes de champ, potentiel, plaques, énergie.
> - Les six exemples chiffrés qu'elle résout sont les six situations types du chapitre ; savoir les
>   refaire seul suffit à traiter la plupart des exercices.
> - La méthode en cinq étapes présentée à la fin est la même que sur la page **Méthode**.
""" % VIDEO_YT))

# ---- parties de cours (A, B, E, F) : une page par ## (ou par ### s'il n'y a qu'un ##)
def add_partie(key, group, skip=(), kind="cours"):
    body = parties[key]
    secs = split_on(body, 2)
    head = [b for t, b in secs if t is None]
    secs = [(t, b) for t, b in secs if t is not None]
    if len(secs) <= 1:                        # ex. partie B : on decoupe sur ###
        inner = secs[0] if secs else (None, body)
        sub = [(t, b) for t, b in split_on(inner[1], 3) if t is not None]
        if sub:
            for t, b in sub:
                if t in skip:
                    continue
                add(slug(t), group, t, H("## " + t + "\n" + clean(b)), kind)
            return
    for t, b in secs:
        if t in skip:
            continue
        add(slug(t), group, t, H("## " + t + "\n" + clean(b)), kind)

add_partie("Partie A — Comprendre avant de calculer", "Les bases")
add_partie("Partie B — Le cours", "Le cours")
add_partie("Partie E — Le champ électrique au travail", "Au travail")
add_partie("Partie F — Méthode, erreurs et auto-test", "Méthode", skip=("F.3. Auto-test",))

# ---- exercices : en-tete de la rubrique
G0 = parties["Partie G — Entraînement supplémentaire"]
add("exos-infos", "Exercices", "Mode d'emploi et données", H(clean(split_on(G0, 2)[0][1])), "exo")

# ---- exercices : partie C
C = parties["Partie C — Exercices"]
c_secs = dict((t, b) for t, b in split_on(C, 3) if t)
c_h2 = dict((t, b) for t, b in split_on(C, 2) if t)

def cut(md, marker_level, marker_start):
    """separe enonce / corrige sur un titre dont le texte commence par marker_start"""
    pat = re.compile(r"^#{%d} (%s.*)$" % (marker_level, marker_start), re.M)
    m = pat.search(md)
    if not m:
        return md, ""
    return md[:m.start()], md[m.end():]

st, so = cut(c_secs["Exercice 5"], 4, "Corrigé")
add("ex-5", "Exercices", "Exercice 5 — superposition", H("## Exercice 5\n" + clean(st)), "exo",
    dict(sol="sol-5"))
add("sol-5", "Solutions", "Exercice 5", H("## Corrigé de l'exercice 5\n" + clean(so)), "sol",
    dict(exo="ex-5", fig="anim-01-addition-vecteurs.svg",
         cap="La construction de la somme, étape par étape, avec les valeurs de l'exercice."))

add("sol-6", "Solutions", "Exercice 6", H("## Exercice 6 — corrigé manuscrit\n"
    + clean(c_secs["Exercice 6 — corrigé (extrait manuscrit)"])), "sol", dict())

th = c_h2["Exercice II — L'expérience de J. J. Thomson"]
st, so = cut(th, 3, "Corrigé")
add("ex-thomson", "Exercices", "Exercice II — Thomson", H("## Exercice II — l'expérience de Thomson\n" + clean(st)),
    "exo", dict(sol="sol-thomson"))
add("sol-thomson", "Solutions", "Exercice II — Thomson", H("## Corrigé — expérience de Thomson\n" + clean(so)),
    "sol", dict(exo="ex-thomson", fig="anim-05-thomson.svg",
                cap="La trajectoire parabolique de l'électron et la force qui la provoque."))

# ---- exercices : partie D (bac)
D = parties["Partie D — Annexe"]
st, so = cut(D, 3, "Solution de la Question 1")
st = re.sub(r"^#{1,3} .*$", "", st, count=0, flags=0) if False else st
st = "\n".join(l for l in st.split("\n") if not l.startswith("## 6. Annexe") and not l.startswith("### 6.1."))
add("ex-bac", "Exercices", "Sujet de Bac — Champs", H("## Sujet de Bac — Question 1 : Champs\n" + clean(st)),
    "exo", dict(sol="sol-bac"))
add("sol-bac", "Solutions", "Sujet de Bac — Champs", H("## Corrigé du sujet de Bac\n" + clean(so)), "sol",
    dict(exo="ex-bac", fig="anim-07-millikan.svg",
         cap="La gouttelette de Millikan : elle tombe, remonte, puis reste en suspension quand qE = mg."))

# ---- auto-test (partie F.3)
F = parties["Partie F — Méthode, erreurs et auto-test"]
f3 = dict((t, b) for t, b in split_on(F, 2) if t)["F.3. Auto-test"]
st, so = cut(f3, 3, "Réponses")
add("ex-autotest", "Exercices", "Auto-test (10 questions)", H("## Auto-test\n" + clean(st)), "exo",
    dict(sol="sol-autotest"))
add("sol-autotest", "Solutions", "Auto-test", H("## Réponses de l'auto-test\n" + clean(so)), "sol",
    dict(exo="ex-autotest"))

# ---- exercices : partie G
FIGMAP = {
    4:  ("sol-04-coulomb-cas.svg", "Les quatre cas, l'un après l'autre : seules les longueurs changent."),
    6:  ("22-notion-de-champ.svg", "Même géométrie pour la gravitation et pour l'électricité."),
    7:  ("anim-02-loi-carre-inverse.svg", "La flèche se raccourcit comme 1/r² quand on s'éloigne."),
    9:  ("sol-09-champ-au-milieu.svg", "Cas a puis cas b : les champs se soustraient, puis s'ajoutent."),
    13: ("sol-13-point-nul.svg", "Le champ résultant s'annule exactement en P, puis change de sens."),
    16: ("06-superposition.svg", "Les potentiels s'additionnent comme des nombres, les champs comme des vecteurs."),
    18: ("25-tension-plaques.svg", "Entre deux plaques, le potentiel varie linéairement : E = U/d."),
    19: ("anim-07-millikan.svg", "L'équilibre de la gouttelette : qE = mg."),
    20: ("anim-05-thomson.svg", "La déviation d'un électron entre deux plaques."),
    21: ("anim-08-jet-encre.svg", "Même principe que le jet d'encre : la charge décide de la trajectoire."),
}
G = parties["Partie G — Entraînement supplémentaire"]
for gt, gb in [(t, b) for t, b in split_on(G, 2) if t]:
    blocks, cur = [], []
    for line in gb.split("\n"):
        if re.match(r"^\*\*\d+\.\*\* ", line):
            if cur:
                blocks.append(cur)
            cur = [line]
        elif cur:
            cur.append(line)
    if cur:
        blocks.append(cur)
    for blk in blocks:
        txt = "\n".join(blk)
        num = int(re.match(r"^\*\*(\d+)\.\*\*", txt).group(1))
        m = re.search(r"^> \*\*Corrigé\.\*\*", txt, re.M)
        enonce, corrige = (txt[:m.start()], txt[m.start():]) if m else (txt, "")
        corrige = re.sub(r"^> ?", "", corrige, flags=re.M).replace("**Corrigé.**", "").strip()
        fig, cap = FIGMAP.get(num, (None, None))
        theme = gt.split(". ", 1)[-1]
        add("g-%d" % num, "Exercices", "%d · %s" % (num, theme),
            H("## Exercice %d\n*%s*\n\n" % (num, theme) + clean(enonce)), "exo",
            dict(sol="gsol-%d" % num))
        add("gsol-%d" % num, "Solutions", "Exercice %d · %s" % (num, theme),
            H("## Corrigé de l'exercice %d\n" % num + clean(corrige)), "sol",
            dict(exo="g-%d" % num, fig=fig, cap=cap))

# ---- formulaire
form = [b for t, b in split_on(src, 2) if t and t.startswith("Formulaire")]
add("formulaire", "Mémo", "Formulaire", H("## Formulaire — récapitulatif\n" + clean(form[0])))

# ---------------------------------------------------------------- assemblage
GROUPORDER = ["Pour commencer", "Les bases", "Le cours", "Au travail", "Méthode",
              "Exercices", "Solutions", "Mémo"]
PAGES.sort(key=lambda p: GROUPORDER.index(p["group"]))
GROUPS = []
for p in PAGES:
    if p["group"] not in GROUPS:
        GROUPS.append(p["group"])

nav = []
for g in GROUPS:
    nav.append('<div class="navgroup"><h3>%s</h3><ul>' % html.escape(g))
    for p in PAGES:
        if p["group"] == g:
            lab = plain(p["title"])
            short = lab if len(lab) <= 46 else lab[:44].rstrip() + "…"
            nav.append('<li><a href="#%s" data-id="%s" title="%s">%s</a></li>'
                       % (p["id"], p["id"], html.escape(lab), html.escape(short)))
    nav.append("</ul></div>")
nav = "\n".join(nav)

panes = []
for i, p in enumerate(PAGES):
    extra_top, extra_bot = "", ""
    if p["kind"] == "sol" and p["extra"].get("fig"):
        extra_top = ('<figure class="solfig">%s<figcaption>%s</figcaption></figure>'
                     % (inline_svg(p["extra"]["fig"]), html.escape(p["extra"]["cap"] or "")))
    if p["kind"] == "exo" and p["extra"].get("sol"):
        extra_bot = ('<p class="solbtn"><a class="btn" href="#%s">Voir la solution &rarr;</a></p>'
                     % p["extra"]["sol"])
    if p["kind"] == "sol" and p["extra"].get("exo"):
        extra_bot = ('<p class="solbtn"><a class="btn ghost" href="#%s">&larr; Revenir à l\'énoncé</a></p>'
                     % p["extra"]["exo"])
    body = p["html"]
    if p["id"] in EXO_TLDR:
        body = put_tldr(body, EXO_TLDR[p["id"]])
    if p["id"] in SOL_RETENIR:
        body += "\n" + box("pourexos", "À retenir.", SOL_RETENIR[p["id"]])
    panes.append('<section class="pane %s" id="%s" data-n="%d">\n%s\n%s\n%s\n</section>'
                 % (p["kind"], p["id"], i + 1, extra_top, body, extra_bot))
panes = "\n".join(panes)

# les titres générés par pandoc peuvent collisionner (deux « Exercice 5 ») : on désambiguïse
_seen = set()
def _uniq_head(m):
    pre, hid = m.group(1), m.group(2)
    if hid in _seen:
        k = 2
        while "%s-%d" % (hid, k) in _seen:
            k += 1
        hid = "%s-%d" % (hid, k)
    _seen.add(hid)
    return '%sid="%s"' % (pre, hid)
panes = re.sub(r'(<h[1-4] )id="([^"]+)"', _uniq_head, panes)

tpl = open(os.path.join(ROOT, "site-template.html"), encoding="utf-8").read()
out = (tpl.replace("<!--NAV-->", nav).replace("<!--PANES-->", panes)
          .replace("<!--NPAGES-->", str(len(PAGES))))

if KATEX:
    out = out.replace("<!--KATEXCSS-->", "<style>\n" + open(KCSS, encoding="utf-8").read() + "\n</style>")
    js = r"""
const katex = require(process.argv[2]);
const fs = require('fs');
let h = fs.readFileSync(process.argv[3], 'utf8');
let n = 0, bad = [];
const unesc = s => s.replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"')
                    .replace(/&#39;/g, "'").replace(/&amp;/g, '&');
const run = (re, display) => {
  h = h.replace(re, (m, tex) => {
    n++;
    try {
      return katex.renderToString(unesc(tex), {displayMode: display, throwOnError: true, strict: false});
    } catch (e) {
      bad.push(unesc(tex).slice(0, 60) + '  ->  ' + e.message.slice(0, 90));
      return katex.renderToString(unesc(tex), {displayMode: display, throwOnError: false, strict: false});
    }
  });
};
run(/<span\s+class="math display">([\s\S]*?)<\/span>/g, true);
run(/<span\s+class="math inline">([\s\S]*?)<\/span>/g, false);
fs.writeFileSync(process.argv[3], h);
console.error(JSON.stringify({rendered: n, errors: bad}));
"""
    tmp = tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8")
    tmp.write(js); tmp.close()
    open(OUT, "w", encoding="utf-8").write(out)
    r = subprocess.run(["node", tmp.name, KJS, OUT], capture_output=True, text=True)
    os.unlink(tmp.name)
    if r.returncode:
        sys.exit("node/katex: " + r.stderr)
    import json
    info = json.loads(r.stderr.strip().split("\n")[-1])
    print("KaTeX : %d formules rendues" % info["rendered"])
    for e in info["errors"]:
        print("   ! " + e)
else:
    out = out.replace("<!--KATEXCSS-->", "")
    open(OUT, "w", encoding="utf-8").write(out)
    print("KaTeX indisponible : rendu MathML")
print("%s : %d pages, %.0f Ko" % (os.path.basename(OUT), len(PAGES), os.path.getsize(OUT) / 1024))
