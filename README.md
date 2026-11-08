# EELM — ressources de révision

Cours de l'École européenne remis au propre : texte relu, **figures redessinées en SVG** (certaines
animées), explications ajoutées pour qu'un élève puisse travailler seul, et exercices corrigés.

👉 **Site : <https://owulveryck.github.io/eelm/>**

Chaque chapitre produit une page HTML autonome : pas de serveur, pas de connexion, pas de
JavaScript nécessaire pour lire les formules. Le fichier s'ouvre aussi bien depuis une clé USB.

## Contenu

| Niveau | Matière | Chapitre | |
|---|---|---|---|
| S6FR | Physique | Champ électrique | [lire](https://owulveryck.github.io/eelm/S6FR/physique/champ/) |

```
S6FR/physique/champ/
├── champ-electrique.md          source unique du cours (Markdown + LaTeX)
├── cours-champ-electrique.html  site du chapitre, autonome (78 pages, menu, exercices, solutions)
├── figures/                     39 figures SVG, dont 11 animées (SMIL)
├── build-site.py                génère le HTML à partir du Markdown
├── site-template.html           gabarit (CSS et navigation)
└── vendor/                      KaTeX (JS + CSS avec polices intégrées)
```

## Reconstruire

Prérequis : `pandoc`, `python3`, et `node` (pour le rendu des formules par KaTeX ;
sans lui, le script retombe automatiquement sur MathML).

```bash
cd S6FR/physique/champ
python3 build-site.py      # Markdown  ->  cours-champ-electrique.html
cd ../../..
python3 build-index.py     # régénère les pages d'index et la galerie de figures
```

Les figures sont du SVG écrit à la main (ou produit par de petits scripts) : elles se modifient
dans n'importe quel éditeur de texte, et restent lisibles en mode sombre.

## Sources et droits

- Le **cours** (parties B, C et l'annexe Bac) est la transcription d'un polycopié de
  l'**École européenne Jacques Delors**, dont les droits appartiennent à ses auteurs. Il est
  reproduit ici à des fins de révision personnelle.
- Les **explications ajoutées** (partie A), les **applications** (partie E), la **méthode**
  (partie F), les **figures SVG** et les **scripts** sont de l'auteur de ce dépôt.
- Les **exercices de la partie G** sont *adaptés* — énoncés réécrits en français, corrigés
  entièrement rédigés — du chapitre 21 d'*Advanced Physics for You* (K. Johnson, S. Hewett,
  S. Holt, J. Miller, Oxford University Press, 2<sup>e</sup> éd., 2015) et des questions
  d'examen (OCR, AQA, Edexcel) que ce manuel reproduit. La provenance est rappelée sur la page
  des exercices. Aucun extrait du livre, aucune de ses illustrations et aucun PDF ne sont
  republiés ici ; `.gitignore` exclut d'ailleurs tout fichier PDF du dépôt.

## Licence

- Explications ajoutées, corrigés rédigés, figures SVG, pages d'index :
  [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.fr)
- Scripts (`build-site.py`, `build-index.py`, `site-template.html`, `assets/`) : MIT
- Le polycopié transcrit et les exercices adaptés du manuel restent la propriété de leurs
  auteurs et ne sont pas couverts par ces licences.

Le détail est dans [LICENSE](LICENSE). Toute demande de retrait de la part d'un ayant droit
sera honorée.
