# AGENTS.md — comment ce dépôt est fabriqué

Ce fichier explique la chaîne de production d'un chapitre, pour pouvoir en ajouter d'autres sans
rien redécouvrir. Il est écrit pour un agent (Claude Code) autant que pour un humain.

Une procédure pas-à-pas prête à lancer existe aussi en tant que *skill* :
`.claude/skills/nouveau-chapitre/SKILL.md` — dans Claude Code, taper `/nouveau-chapitre`.

---

## 1. Principe

Un chapitre = **un fichier Markdown**, source unique de vérité. Tout le reste est généré :

```
champ-electrique.md ──(build-site.py + site-template.html)──► cours-champ-electrique.html
        │                                                      (une page HTML autonome)
        └── figures/*.svg ─── inlinées dans le HTML
                                                 build-index.py ──► index.html, figures.html
```

Trois règles qui expliquent tous les choix techniques :

1. **Le HTML produit est autonome.** Aucune requête réseau : KaTeX est embarqué, les polices sont
   en base64, les SVG sont inlinés. Le fichier doit s'ouvrir depuis une clé USB, hors ligne.
2. **Le Markdown reste lisible seul**, et imprimable en PDF via pandoc. Rien d'essentiel ne vit
   uniquement dans le générateur.
3. **Une notion = une page.** Le découpage en pages est dérivé des titres du Markdown, pas écrit à
   la main.

## 2. Arborescence

```
<niveau>/<matière>/<chapitre>/
├── <chapitre>.md                 la source
├── cours-<chapitre>.html         le site généré (détecté par build-index.py via cours-*.html)
├── build-site.py                 le générateur, propre à ce chapitre
├── site-template.html            le gabarit (CSS + navigation)
├── figures/*.svg                 les figures, dont les animées
├── vendor/                       katex.min.js + katex.inline.css (polices en base64)
├── video/                        la vidéo du chapitre (cf. §8)
│   ├── script.py                 le texte lu, phrase par phrase
│   ├── scenes.py                 un dessin animé par phrase
│   ├── dessins.py                les dessins de base réutilisés
│   └── build/                    travail intermédiaire — non versionné
├── cours-<chapitre>.mp4          la vidéo produite — non versionnée (hébergée sur YouTube)
├── index.html, figures.html      générés par build-index.py
└── assets/site.css               (à la racine du dépôt) CSS des pages d'index
```

Exemple existant : `S6FR/physique/champ/`. Les niveaux sont des sections (`S6FR` = S6 section
française). `build-index.py` balaie ces trois niveaux de répertoires et régénère tous les index.

## 3. Prérequis

| Outil | Rôle | Sans lui |
|---|---|---|
| `pandoc` (≥ 2.17) | Markdown → HTML | bloquant |
| `python3` | les deux générateurs | bloquant |
| `node` | rendu KaTeX au build | repli automatique sur MathML (rendu inférieur) |
| `inkscape` | rendre un SVG en PNG pour **le regarder** | on ne peut plus vérifier les figures |
| `pdftotext`, `pdftoppm` (poppler) | extraire le manuel source | pas d'adaptation d'exercices |
| `ffmpeg`, `ffprobe` | montage de la vidéo | pas de vidéo |
| `latex` + `dvisvgm` (TeX Live) | composer les formules de la vidéo | pas de vidéo |
| `gcloud` (ADC) | synthèse vocale Google Cloud | pas de bande son |

**Le manuel est un prérequis à installer à part.** *Advanced Physics for You* (K. Johnson,
S. Hewett, S. Holt, J. Miller, Oxford University Press, 2ᵉ éd., 2015) est sous copyright : il
**n'est pas dans ce dépôt et ne doit jamais y être ajouté** (`.gitignore` exclut `*.pdf`). Pour
travailler avec lui, poser le fichier à côté du `.md`, sous le nom
`Advanced Physics for You - 2ndEdition - book.pdf`, et l'extraire dans un répertoire temporaire :

```bash
pdftotext -f 250 -l 275 "Advanced Physics for You - 2ndEdition - book.pdf" /tmp/book.txt
```

Ce qu'on en tire : les **situations**, les **valeurs numériques**, l'ordre pédagogique. Ce qu'on
n'en reprend pas : son texte, ses figures, ses corrigés. Les énoncés sont **réécrits en français**,
les corrigés **rédigés et recalculés** (voir §8).

## 4. Structure attendue du Markdown

```markdown
---
title: "Champ électrique"          ← repris par build-index.py
subtitle: "Physique – S6 · ..."    ← idem
author: "..."
date: "2026–2027"
lang: fr
---

# Titre du chapitre
# Partie A — Comprendre avant de calculer     ← les bases, écrites pour un élève de 15 ans
# Partie B — Le cours                          ← le polycopié d'origine, intact
# Partie C — Exercices                         ← les exercices du polycopié
# Partie D — Annexe                            ← sujet de Bac + corrigé
# Partie E — ... au travail                    ← applications concrètes
# Partie F — Méthode, erreurs et auto-test
# Partie G — Entraînement supplémentaire       ← exercices adaptés du manuel
## Formulaire — récapitulatif
```

Règles de rédaction :

- **Le texte d'origine du polycopié ne se réécrit pas.** On ajoute autour (partie A, encadrés
  « En clair »), on ne retouche pas la partie B. Après toute modification, vérifier qu'aucune ligne
  d'origine n'a disparu (comparer avec la version précédente du fichier).
- **Chaque page de cours commence par un `> **TL;DR.**` et finit par un
  `> **À retenir pour les exercices**`** (liste à puces). C'est ce qui donne aux pages leur en-tête
  gris-bleu et leur encadré orange final.
- Les encadrés sont des *blockquotes* dont le premier mot en gras décide de la couleur, via
  `classify()` dans `build-site.py` :

  | Premier mot en gras | Classe CSS | Couleur |
  |---|---|---|
  | `TL;DR.` | `tldr` | gris-bleu, en haut de page |
  | `En clair.` | `enclair` | bleu — traduit une formule en français courant |
  | `À retenir.`, `L'idée clé.`, `Astuce…`, `Moyen mnémotechnique.` | `retenir` | orange |
  | `À retenir pour les exercices`, `Comment choisir sa formule`, `Par où commencer` | `pourexos` | encadré orange, en bas de page |
  | `Exemple résolu…`, `Corrigé.` | `exemple` | vert |
  | tout le reste | `note` | beige |

- Les maths sont en LaTeX, `$...$` et `$$...$$`. **Ne pas utiliser `\boxed`** : il produit un
  `<menclose>` mal rendu ; `build-site.py` le retire, donc il ne sert à rien.
- Virgule décimale à la française : `$1{,}60 \times 10^{-19}$`.
- Les figures s'insèrent comme des images : `![Légende.](figures/nom.svg)`. Une légende qui commence
  par `**Animation.**` signale une figure animée (repris dans la galerie).
- Partie G : un exercice = une ligne `**n.** énoncé…` suivie d'un `> **Corrigé.**`. Le générateur
  en fait automatiquement **deux pages** (énoncé `g-n`, corrigé `gsol-n`) reliées par des boutons.

## 5. Ce que fait `build-site.py`

- **Découpage** : une page par `##` de chaque partie (par `###` si la partie n'a qu'un seul `##`,
  cas de la partie B). Les ids viennent du titre (`slug()`), sauf partie G (`g-n` / `gsol-n`).
- **Rubriques du menu** : `GROUPORDER = ["Pour commencer", "Les bases", "Le cours", "Au travail",
  "Méthode", "Exercices", "Solutions", "Mémo"]`.
- **Pandoc** est appelé avec `--wrap=none`. **C'est obligatoire** : sans cette option, pandoc coupe
  ses lignes à 72 colonnes, y compris au milieu de `<span class="math inline">`, et le
  post-traitement KaTeX rate ces formules — elles s'affichent en LaTeX brut.
- **KaTeX au build** : un passage `node` remplace chaque `<span class="math …">` par du HTML+MathML.
  Les erreurs sont affichées à la fin ; une sortie saine se termine par `KaTeX : N formules rendues`
  et aucune ligne d'erreur.
- **SVG inlinés** : `inline_svg()` retire le `<style>` interne de chaque figure (il contient un
  `@media (prefers-color-scheme: dark)` qui rendrait la figure invisible sur la page claire) et
  garde `width`/`height` (le CSS fait le reste avec `max-width:100%;height:auto`).
- **Ids uniques** : les titres générés par pandoc sont dédoublonnés automatiquement (deux
  « Exercice 5 » dans deux parties différentes).
- **Encadrés des pages d'exercices** : les dictionnaires `EXO_TLDR` (haut des énoncés) et
  `SOL_RETENIR` (bas des corrigés) en début de fichier, indexés par id de page. Ces pages sont
  assemblées morceau par morceau, elles n'ont donc pas d'ancre dans le Markdown.
- **Figures des corrigés** : `FIGMAP`, indexé par numéro d'exercice de la partie G.

## 6. Les figures SVG

Écrites à la main ou par un petit script Python jetable (gardé dans le répertoire de travail, pas
dans le dépôt). Les contraintes, apprises à la dure :

- **La frame statique doit être lisible.** Les attributs du SVG sont écrits à un instant
  représentatif de l'animation, que SMIL (`<animate>`, `<animateMotion>`, `<animateTransform>`)
  écrase à l'exécution. Conséquence : à l'impression ou en PDF, la figure reste compréhensible.
  Pour un `<animateMotion>`, placer l'élément sur le point de départ du chemin et exprimer le chemin
  relativement à ce point, sinon tous les points se superposent en (0,0) dans la frame statique.
- Faire **commencer et finir la boucle sur une frame représentative** (pas sur un cas dégénéré :
  vecteur nul, point au bord, cas limite).
- Pas de texte coupé par le `viewBox` : élargir le `viewBox` plutôt que réduire la police.
- **Toujours regarder la figure** avant de la valider :
  `inkscape --export-type=png --export-dpi=140 figures/xx.svg` puis ouvrir le PNG. Les
  chevauchements d'étiquettes ne se voient pas dans le source.
- Accents en UTF-8 directement dans le SVG (pas d'entités).

## 7. Ajouter un chapitre

```bash
NIV=S6FR MAT=physique CHAP=induction
mkdir -p $NIV/$MAT/$CHAP/figures
cp S6FR/physique/champ/{build-site.py,site-template.html} $NIV/$MAT/$CHAP/
cp -r S6FR/physique/champ/vendor $NIV/$MAT/$CHAP/
# écrire $NIV/$MAT/$CHAP/$CHAP.md (cf. §4), puis :
cd $NIV/$MAT/$CHAP && python3 build-site.py && cd -
python3 build-index.py
python3 check-site.py
```

Pour la vidéo du chapitre, voir §8.

Dans `build-site.py`, les points à adapter pour un nouveau chapitre : le nom du `.md` et du `.html`
en tête de fichier, le titre dans `site-template.html` (`<header id="top">`), `FIGMAP`,
`EXO_TLDR`, `SOL_RETENIR`, et les noms de parties s'ils diffèrent.

## 8. La vidéo du chapitre

Le site a une vidéo d'environ vingt minutes, non référencée sur YouTube et intégrée dans la page
d'accueil du chapitre. Elle est fabriquée entièrement en ligne de commande : **aucun montage à la
main**, tout est reproductible depuis les sources.

### Le principe

Une **phrase = un plan**. On écrit d'abord le texte parlé, puis le dessin qui l'accompagne ; la
durée de chaque plan est celle du fichier audio correspondant, donc l'image et la voix ne peuvent
pas se désynchroniser. La chaîne complète :

```
script.py  ──▶ synthese.py ──▶ build/audio/*.mp3 + build/narration.json
                                        │
scenes.py  ──▶ montage.py  ◀────────────┘
                  │  SVG (1920×1080) ─ inkscape ─▶ PNG ─ ffmpeg ─▶ un segment par plan
                  └─▶ concaténation + bande son + sous-titres ─▶ cours-<chapitre>.mp4
```

Le moteur est dans `outils/video/` et ne dépend pas du chapitre :

| Fichier | Rôle |
|---|---|
| `canvas.py` | la feuille 1920×1080 et les primitives (`rect`, `arrow`, `charge`, `card`, `txt`…), la palette, le bandeau de titre |
| `tex.py` | une formule LaTeX → du SVG vectoriel (`latex` → `dvisvgm`), mis en cache et placé à la bonne échelle |
| `gtts.py` | synthèse vocale Google Cloud en REST, authentifiée par les identifiants ADC de `gcloud` |
| `synthese.py` | lit `script.py`, produit un mp3 par phrase et le manifeste des durées |
| `montage.py` | lit `scenes.py` + le manifeste, rend les images, assemble la vidéo, écrit les sous-titres |

### Écrire la vidéo d'un nouveau chapitre

```bash
NIV=S6FR MAT=physique CHAP=induction
mkdir -p $NIV/$MAT/$CHAP/video
# s'inspirer de S6FR/physique/champ/video/{script.py,scenes.py,dessins.py}
```

`script.py` déclare le nom du fichier produit, la voix, et la liste des scènes :

```python
SORTIE = "cours-induction.mp4"
VOIX = "fr-FR-Chirp3-HD-Charon"      # voix masculine posée, la plus naturelle en français
RATE = 0.92                          # un peu plus lent que la normale : c'est un cours
SCENES = [
 ("titre", "Induction", [
   "Première phrase lue, qui donne le premier plan.",
   "Deuxième phrase, deuxième plan.",
 ]),
]
```

`scenes.py` expose un dictionnaire `SCENES` qui associe chaque identifiant à une fonction
`f(c, pi, t)` : `c` est la feuille, `pi` l'indice de la phrase en cours (le dessin se construit au
fur et à mesure du texte), `t` la phase de l'animation entre 0 et 1.

```python
def s01(c, pi, t):
    head(c, "Induction", 1)                     # bandeau + barre de progression
    if pi >= 1:
        c.arrow(400, 500, 900, 500, col=POS)
    tex.put(c, r"\Phi = B\,S\,\cos\theta", 960, 700, pt=50)
SCENES = {"titre": s01}
```

Puis :

```bash
gcloud services enable texttospeech.googleapis.com     # une fois par projet
python3 outils/video/synthese.py $NIV/$MAT/$CHAP/video
python3 outils/video/montage.py  $NIV/$MAT/$CHAP/video
```

### Les règles apprises en fabriquant la première

- **Un exemple chiffré après chaque notion**, et un fil directeur unique qui traverse tout le
  chapitre (ici la gouttelette d'une imprimante à jet d'encre, reprise six fois). C'est ce qui
  distingue une vidéo d'un diaporama lu.
- **Les formules passent par `tex.py`**, jamais par du texte : `E = U/d` écrit en caractères
  ordinaires est illisible, la même composée par LaTeX se lit immédiatement.
- **Rien n'est écrit en toutes lettres dans la narration qui ne soit pas prononçable** : « dix
  puissance moins quinze », pas « 10⁻¹⁵ ». Le texte de `script.py` sert aussi de sous-titres.
- **Un plan fixe ne coûte qu'une image** : `montage.py` compare les 36 images d'un plan et, si
  elles sont identiques, n'en rend qu'une. Garder les animations là où elles expliquent quelque
  chose.
- **Les identifiants SVG des formules sont déterministes** (empreinte du contenu et de la
  position). S'ils dépendaient d'un compteur, deux images successives d'un plan fixe différeraient
  et tous les plans seraient rendus comme animés.
- **La bande son est concaténée en PCM**, pas en mp3 : enchaînés tels quels, les remplissages
  d'encodage des mp3 décalent la voix de plusieurs secondes sur vingt minutes. Le nombre d'images
  de chaque segment est calculé sur le temps cumulé, pour que l'image et le son finissent ensemble
  (vérifier : les durées des pistes dans `ffprobe` doivent coïncider à moins de 0,1 s).
- **Relire les images avant de monter.** Pas de navigateur ici : on rend une image par plan en PNG
  et on assemble des planches contact à regarder.

```bash
cd $NIV/$MAT/$CHAP/video && python3 -c "
import sys; sys.path[:0]=['.','../../../../outils/video']
import canvas, scenes, script, os
os.makedirs('build/apercu', exist_ok=True)
for i,(sid,t,ph) in enumerate(script.SCENES):
    c = canvas.C(); scenes.SCENES[sid](c, len(ph)-1, 0.42)
    open('build/apercu/%02d.svg'%i,'w').write(c.svg())
"
ls build/apercu/*.svg | xargs -P 8 -I{} inkscape --export-type=png --export-width=1280 {}
montage build/apercu/*.png -tile 3x -geometry 640x+5+5 -background '#ddd' build/planche.png
```

Les collisions de texte, les flèches hors cadre et les étiquettes superposées ne se voient que
comme ça. C'est l'étape la plus longue, et la seule qui fasse la différence.

### Publier

La vidéo (≈ 30 Mo) **n'est pas versionnée** : elle est envoyée sur YouTube en **non répertorié**,
et la page d'accueil du chapitre l'intègre dans un lecteur `youtube-nocookie.com`. C'est la seule
ressource externe tolérée par `check-site.py`. Les sous-titres `.srt` produits à côté du `.mp4`
sont à charger dans YouTube (ils ne sont pas extraits automatiquement de la vidéo).

## 9. Avant de pousser

```bash
python3 check-site.py       # équilibre des balises, ids, liens, formules non rendues, PDF
git status --short
```

- `check-site.py` doit sortir **sans aucune anomalie**. En particulier `formules non rendues : 0` :
  toute valeur non nulle signifie du LaTeX brut visible dans la page.
- **Aucun PDF ne doit être suivi par git**, jamais (`git ls-files | grep -i pdf` → vide).
- Les corrigés sont **recalculés** (en Python, pas de tête) avant d'être écrits. Un corrigé faux est
  pire qu'un exercice absent.
- Pas de navigateur dans l'environnement de travail : la vérification du HTML est programmatique
  (`check-site.py`) et celle des figures se fait en PNG via inkscape. Ne pas prétendre avoir
  « ouvert la page ».

## 10. Droits

Voir [LICENSE](LICENSE). En résumé : le polycopié transcrit appartient à ses auteurs ; les exercices
de la partie G sont *adaptés* du manuel (prérequis non versionné) et leur provenance est citée sur
la page des exercices ; les ajouts, figures et scripts sont sous CC BY-NC-SA 4.0 / MIT.
