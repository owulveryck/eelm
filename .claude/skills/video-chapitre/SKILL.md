---
name: video-chapitre
description: Fabriquer la vidéo explicative d'un chapitre de ce dépôt (eelm) — écrire la narration, dessiner les plans animés en SVG, composer les formules en LaTeX, synthétiser la voix avec Google Cloud, monter le fichier mp4 avec ffmpeg, puis le publier en non répertorié sur YouTube et l'intégrer dans la page du chapitre. À utiliser dès qu'on veut une vidéo, une capsule ou une bande son pour un cours du dépôt.
---

# Faire la vidéo d'un chapitre

Lire d'abord **§8 de `AGENTS.md`** : principe, moteur, règles de fond. Cette *skill* en est la
procédure exécutable. Le moteur (`outils/video/`) est générique ; seuls `script.py`, `scenes.py`
et `dessins.py` du chapitre sont à écrire.

## Étape 0 — vérifier l'outillage

```bash
for o in ffmpeg ffprobe inkscape latex dvisvgm gcloud montage; do
  command -v $o >/dev/null || echo "manquant : $o"
done
gcloud services enable texttospeech.googleapis.com     # une fois par projet
```

Sans `latex`/`dvisvgm`, pas de formules : ne pas se rabattre sur du texte ordinaire, c'est
illisible à l'écran. Corriger l'outillage d'abord.

## Étape 1 — le fil directeur, avant d'écrire une ligne

Choisir **un objet concret** qui traverse tout le chapitre et qu'on retrouvera cinq ou six fois :
pour le champ électrique, c'est la gouttelette d'encre d'une imprimante à jet d'encre, posée en
énigme au début et calculée entièrement à la fin. Une vidéo sans fil directeur est un diaporama lu.

Puis la trame : une notion, **un exemple chiffré résolu en entier**, la notion suivante. Les
exemples sont la colonne vertébrale, pas une annexe. Vérifier chaque valeur numérique en Python
avant de l'écrire — un calcul faux dans une vidéo ne se corrige pas d'un commit.

## Étape 2 — `script.py` : le texte parlé

Une phrase = un plan. Le texte est lu tel quel par la synthèse vocale **et** sert de sous-titres.

```python
SORTIE = "cours-<chapitre>.mp4"
VOIX = "fr-FR-Chirp3-HD-Charon"
RATE = 0.92
SCENES = [("identifiant", "Titre du bandeau", ["Phrase un.", "Phrase deux."])]
```

- Tout s'écrit **prononçable** : « dix puissance moins quinze coulombs », jamais « 10⁻¹⁵ C ».
- Les apostrophes s'écrivent normalement : `synthese.py` les convertit en `ʼ` (U+02BC) avant
  l'envoi, sans quoi la voix Chirp3 coupe une demi-seconde à chaque élision. Ne pas défaire ça.
- Des phrases courtes. Une idée par phrase, puisqu'une phrase est un plan.
- Viser 15 à 25 minutes ; le découpage en scènes doit rester lisible dans le sommaire mental de
  l'élève (une notion, un exemple, une notion…).

## Étape 3 — `scenes.py` : un dessin par phrase

```python
import canvas, tex
import dessins
from canvas import C, W, H, INK, MUT, POS, NEG, ACC, SOFT, OR, PALE, BG

def s01(c, pi, t):
    head(c, "Titre", 1)          # bandeau + barre de progression
    if pi >= 1:                  # le dessin se construit au fil du texte
        c.arrow(400, 500, 900, 500, col=POS)
    tex.put(c, r"E = \frac{U}{d}", 960, 700, pt=50)
SCENES = {"identifiant": s01}
```

`pi` = indice de la phrase en cours dans la scène, `t` = phase d'animation entre 0 et 1. Le
troisième argument de `head` est l'**identifiant** de la scène : son rang et le nombre total de
plans se lisent dans `script.py`, il n'y a donc jamais de numéro à mettre à jour à la main.

- **Toute formule passe par `tex.put`.** Jamais `c.txt("E = U/d")`.
- **Un exemple se dessine autant qu'il se calcule** : passer `fig=` à `exemple()` met la situation
  à gauche et le calcul à droite. Un exemple qui n'est qu'une suite de lignes est raté.
- Le dessin doit rester lisible **à l'arrêt** sur n'importe quelle image.
- Animer seulement ce qui explique quelque chose (un champ qui s'établit, une charge qui dévie).
  Un plan fixe ne coûte qu'une image au rendu, un plan animé en coûte trente-six.
- Réutiliser les dessins de base (`dessins.py`) plutôt que redessiner : une même figure vue sous
  plusieurs angles, c'est du repérage gratuit pour l'élève.

## Étape 4 — relire les images (l'étape qui fait la différence)

Il n'y a **pas de navigateur** ici. On regarde des PNG.

```bash
cd <niveau>/<matière>/<chapitre>/video && python3 -c "
import sys, os; sys.path[:0]=['.','../../../../outils/video']
import canvas, scenes, script
os.makedirs('build/apercu', exist_ok=True)
for i,(sid,t,ph) in enumerate(script.SCENES):
    c = canvas.C(); scenes.SCENES[sid](c, len(ph)-1, 0.42)
    open('build/apercu/%02d.svg'%i,'w').write(c.svg())
"
ls build/apercu/*.svg | xargs -P 8 -I{} inkscape --export-type=png --export-width=1280 {} 2>/dev/null
montage build/apercu/*.png -tile 3x -geometry 640x+5+5 -background '#ddd' build/planche.png
```

Ouvrir `build/planche.png` et **la lire vignette par vignette**. Ce qu'on y trouve à chaque fois :
étiquettes superposées, flèches hors cadre, encadré qui recouvre un schéma, formule trop large.
Corriger, re-rendre, relire. Recommencer jusqu'à ce que chaque vignette tienne debout seule.

## Étape 5 — la voix, puis le montage

```bash
python3 outils/video/synthese.py <niveau>/<matière>/<chapitre>/video   # ~3 min, facturé
python3 outils/video/montage.py  <niveau>/<matière>/<chapitre>/video   # ~15 min de CPU
```

`synthese.py` ne refait pas un mp3 déjà présent : corriger une phrase dans `script.py` et relancer
ne coûte que cette phrase (supprimer le mp3 correspondant dans `build/audio/`). Après un changement
de dessin, effacer `build/frames/<si>-<pi>` et le segment correspondant dans `build/segs/`.

Contrôler la synchronisation à la fin :

```bash
ffprobe -v 0 -show_entries stream=codec_type,duration -of csv=p=0 <chapitre>.mp4
```

Les durées vidéo et audio doivent coïncider **à moins de 0,1 s**. Un écart de plusieurs secondes
signifie que la bande son a été enchaînée en mp3 au lieu de PCM.

Puis extraire quelques images du fichier final et les regarder, pour vérifier que le bon plan
tombe au bon moment :

```bash
for s in 40 300 600 900 1200; do ffmpeg -v 0 -ss $s -i <chapitre>.mp4 -frames:v 1 /tmp/t$s.png; done
```

## Étape 6 — publier

La vidéo n'est **pas versionnée** (`.gitignore` exclut `*.mp4`). Elle va sur YouTube en
**non répertorié** (`privacyStatus: unlisted`), puis dans la page du chapitre :

```bash
gws auth login --scopes ...,https://www.googleapis.com/auth/youtube.upload   # l'utilisateur
gws "youtube:v3" videos insert --params '{"part":"snippet,status"}' \
    --json '{"snippet":{"title":"…","description":"…","categoryId":"27"},
             "status":{"privacyStatus":"unlisted","selfDeclaredMadeForKids":false}}' \
    --upload <chapitre>.mp4 --upload-content-type video/mp4
```

Renseigner ensuite l'identifiant dans `build-site.py` (`VIDEO_YT`), régénérer la page, et
relancer `python3 check-site.py` : le lecteur `youtube-nocookie.com` est la **seule** ressource
externe tolérée. Charger aussi le `.srt` produit à côté du `.mp4` comme sous-titres YouTube.
