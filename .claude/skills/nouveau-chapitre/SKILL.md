---
name: nouveau-chapitre
description: Ajouter un chapitre de cours à ce dépôt (eelm) — créer l'arborescence, rédiger le Markdown source, dessiner les figures SVG, générer le site HTML autonome et les index, puis vérifier avant de pousser. À utiliser dès qu'on veut mettre un nouveau cours, chapitre ou matière en ligne dans ce dépôt.
---

# Ajouter un chapitre

Lire d'abord `AGENTS.md` à la racine : il contient les règles de fond (structure du Markdown,
classes d'encadrés, contraintes des SVG, droits). Cette *skill* en est la procédure exécutable.

## Étape 0 — ce qu'il faut savoir avant de commencer

Demander à l'utilisateur, si ce n'est pas déjà clair :

- le **niveau** (ex. `S6FR`), la **matière** (ex. `physique`), le **nom court du chapitre**
  (ex. `induction`) ;
- la **source** du cours : un polycopié scanné, un PDF, des photos, du texte ? Cette source est le
  squelette : son texte **ne se réécrit pas**, on ajoute autour ;
- si le manuel *Advanced Physics for You* doit servir de source d'exercices. Il est **sous
  copyright, non versionné** : vérifier sa présence à côté du `.md`, sinon demander à
  l'utilisateur de l'y déposer. Ne jamais le committer (`.gitignore` exclut `*.pdf`).

Vérifier l'outillage : `pandoc`, `python3`, `node` (KaTeX), `inkscape` (relecture des figures).

## Étape 1 — squelette

```bash
NIV=S6FR; MAT=physique; CHAP=<nom-court>
mkdir -p $NIV/$MAT/$CHAP/figures
cp S6FR/physique/champ/{build-site.py,site-template.html} $NIV/$MAT/$CHAP/
cp -r S6FR/physique/champ/vendor $NIV/$MAT/$CHAP/
```

Adapter dans `build-site.py` : le nom du `.md` et du `.html` de sortie, et vider `FIGMAP`,
`EXO_TLDR`, `SOL_RETENIR`. Adapter le titre dans `site-template.html` (`<header id="top">`).

## Étape 2 — le Markdown

Transcrire la source **à l'identique** dans les parties B/C/D, puis écrire autour :

- **Partie A** — tout ce qu'il faut pour comprendre, en partant de zéro, pour un élève de 15 ans :
  chaque notion nouvelle est définie, chaque symbole est nommé, aucune étape n'est sautée.
- **Partie E** — où ça sert dans la vraie vie.
- **Partie F** — méthode en 5 étapes, erreurs classiques, auto-test corrigé.
- **Partie G** — exercices d'entraînement, énoncés **réécrits** et corrigés **rédigés**, avec la
  provenance citée en tête de partie.
- **Formulaire** final.

Sur **chaque** section de cours : un `> **TL;DR.**` juste après le titre, et un
`> **À retenir pour les exercices**` (liste à puces) à la fin, avant le `---`. Dans le cours, les
encadrés `> **En clair.**` traduisent chaque formule en français courant.

**Tous les résultats numériques se calculent en Python avant d'être écrits**, corrigés compris.

## Étape 3 — les figures

Une figure par idée qui se dessine. SVG écrit à la main ou par un script Python jetable, animé en
SMIL quand le mouvement explique quelque chose (un vecteur qui s'allonge, une somme construite pas
à pas, une charge qui s'éloigne).

Contraintes impératives (détail dans `AGENTS.md` §6) : la **frame statique doit être lisible**
(l'animation ne fait que l'écraser), la boucle commence et finit sur une frame représentative, rien
ne dépasse du `viewBox`. **Regarder chaque figure** avant de la valider :

```bash
inkscape --export-type=png --export-dpi=140 figures/<nom>.svg
```

puis ouvrir le PNG avec l'outil de lecture d'images. Les chevauchements d'étiquettes ne se voient
jamais dans le source.

## Étape 4 — générer et vérifier

```bash
cd $NIV/$MAT/$CHAP && python3 build-site.py && cd -
python3 build-index.py
python3 check-site.py
```

`build-site.py` doit afficher `KaTeX : N formules rendues` **sans ligne d'erreur**, et
`check-site.py` doit se terminer par `tout est bon.`

## Étape 5 — publier

```bash
git add -A && git status --short      # relire : aucun PDF, aucun fichier temporaire
git commit -m "<matière> <niveau> : <chapitre>"
git push
```

Le site se met à jour tout seul (GitHub Pages, branche `main`). Vérifier ensuite l'URL publiée et
annoncer le lien à l'utilisateur.
