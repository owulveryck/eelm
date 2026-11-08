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

Dans `build-site.py`, les points à adapter pour un nouveau chapitre : le nom du `.md` et du `.html`
en tête de fichier, le titre dans `site-template.html` (`<header id="top">`), `FIGMAP`,
`EXO_TLDR`, `SOL_RETENIR`, et les noms de parties s'ils diffèrent.

## 8. Avant de pousser

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

## 9. Droits

Voir [LICENSE](LICENSE). En résumé : le polycopié transcrit appartient à ses auteurs ; les exercices
de la partie G sont *adaptés* du manuel (prérequis non versionné) et leur provenance est citée sur
la page des exercices ; les ajouts, figures et scripts sont sous CC BY-NC-SA 4.0 / MIT.
