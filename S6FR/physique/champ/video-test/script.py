# -*- coding: utf-8 -*-
"""Narration de la vidéo de révision « spécial test » du chapitre Champ électrique.

Les six points annoncés par le professeur, dans l'ordre : force de Coulomb,
champ uniforme dans un condensateur, lignes de champ (condensateur, puis deux
charges), expérience de Millikan, et la méthode d'analyse des données qui montre
qu'une grandeur est quantifiée. Fil directeur : la goutte d'huile immobile.

Une phrase = un plan. Le texte est lu tel quel par la synthèse vocale et sert
aussi de sous-titres : tout doit être prononçable.
"""

SORTIE = "revision-test-champ-electrique.mp4"
VOIX = "fr-FR-Chirp3-HD-Charon"
RATE = 0.92

SCENES = [
 ("titre", "Révision", [
   "Tu as un test sur le champ électrique, et tu sais déjà ce qui tombe.",
   "Six points, pas un de plus : la force de Coulomb, le champ uniforme dans un condensateur, les lignes de champ, l'expérience de Millikan, et la méthode qui prouve que la charge est quantifiée.",
   "Cette vidéo les reprend dans l'ordre, avec les calculs faits en entier et les schémas tels qu'il faut les tracer sur la copie.",
   "Un fil directeur : une goutte d'huile immobile entre deux plaques. Presque tout le test tient autour d'elle.",
 ]),
 ("prog", "Le programme du test", [
   "Voici le programme. Garde-le en tête : à la fin, tu dois pouvoir cocher les six cases.",
   "Un : la force de Coulomb, sa formule, et le rôle du carré de la distance.",
   "Deux : le champ uniforme dans un condensateur, et la relation E égale U sur d.",
   "Trois : les lignes de champ à l'intérieur d'un condensateur, loin des bords.",
   "Quatre : l'allure des lignes de champ entre deux charges de même valeur, de signes opposés puis de même signe.",
   "Cinq : l'expérience de Millikan, son dispositif et sa démonstration.",
   "Six : l'analyse des données, c'est-à-dire la méthode qui montre qu'une grandeur est quantifiée. C'est là qu'on perd le plus de points, nous y passerons le plus de temps.",
 ]),
 ("coulomb", "La force de Coulomb", [
   "Premier point : la force de Coulomb.",
   "Deux charges ponctuelles exercent l'une sur l'autre une force dont la valeur est : F égale k, fois la valeur absolue de Q, fois la valeur absolue de q, le tout divisé par r au carré.",
   "k est une constante, qui vaut neuf fois dix puissance neuf en unités du système international. Et r est la distance entre les deux charges, en mètres.",
   "Les valeurs absolues donnent un nombre positif : la valeur de la force. Le sens, lui, se lit sur les signes.",
   "Même signe : elles se repoussent. Signes opposés : elles s'attirent. C'est tout ce qu'il faut pour orienter les flèches sur un schéma.",
   "Et une phrase que les correcteurs attendent : les deux forces ont toujours la même valeur, même si une charge est mille fois plus grande que l'autre. C'est la troisième loi de Newton.",
 ]),
 ("exC", "Exemple — la force de Coulomb", [
   "Prenons l'exemple type, et faisons-le exactement comme sur la copie.",
   "Deux charges ponctuelles, plus deux virgule zéro microcoulombs et moins trois virgule zéro microcoulombs, sont distantes de cinq virgule zéro centimètres. Que vaut la force ?",
   "Étape une : la formule en lettres, avant le moindre chiffre.",
   "Étape deux : les unités. Un microcoulomb, c'est dix puissance moins six coulombs ; cinq centimètres, c'est cinq fois dix puissance moins deux mètres.",
   "Étape trois : le dénominateur, et c'est là qu'on perd des points. Cinq fois dix puissance moins deux, au carré, cela fait deux virgule cinq fois dix puissance moins trois. Le carré porte aussi sur la puissance de dix.",
   "Étape quatre : le numérateur. Neuf fois dix puissance neuf, fois deux fois dix puissance moins six, fois trois fois dix puissance moins six : cinq virgule quatre fois dix puissance moins deux.",
   "On divise, et on trouve vingt et un virgule six newtons.",
   "Étape cinq : on interprète. Vingt et un newtons pour deux poussières de microcoulombs, c'est le poids d'un sac de deux kilos. Et comme les signes sont opposés, les deux forces sont attractives, dirigées l'une vers l'autre.",
 ]),
 ("carre", "Le carré de la distance", [
   "Avant de passer au condensateur, deux réflexes autour de ce carré. Ils permettent de répondre sans calculatrice.",
   "Premier réflexe, la technique du rapport. Si la distance est multipliée par deux, la force n'est pas divisée par deux, mais par quatre.",
   "Multipliée par trois, elle est divisée par neuf. La force varie comme un sur r au carré.",
   "Deuxième réflexe : si une seule des deux charges est multipliée par deux, la force est simplement multipliée par deux. Le carré ne porte que sur la distance.",
   "Et le piège qui revient à chaque copie : on ne met jamais des centimètres ni des nanocoulombs dans une formule. Tout en mètres et en coulombs, d'abord.",
 ]),
 ("champ", "Champ et force", [
   "Deuxième point : le champ. Un rappel de trente secondes, parce que tout le reste en dépend.",
   "Le champ électrique en un endroit, c'est la force par unité de charge : E égale F divisé par la valeur absolue de q.",
   "Et la relation se retourne. C'est celle qu'on utilise le plus : une charge q placée dans un champ E subit une force égale à q fois E.",
   "L'unité du champ est le volt par mètre, ou le newton par coulomb. Les deux sont justes, et ce sont exactement les mêmes unités.",
   "Pour une charge positive, la force est dans le sens du champ ; pour une charge négative, elle est dans le sens opposé. Cette phrase vaut des points à chaque test.",
 ]),
 ("condo", "Le condensateur plan", [
   "Troisième point : le condensateur plan, et c'est le dispositif de toute la fin de cette vidéo.",
   "Deux plaques métalliques parallèles, reliées à une alimentation. Entre elles, le champ est uniforme.",
   "Uniforme est un mot précis : même direction, même sens, et même valeur en tout point. Dis les trois, pas seulement le mot.",
   "Sa valeur : E égale U divisé par d, où U est la tension entre les plaques, en volts, et d leur écartement, en mètres.",
   "Conséquence très utile : une charge placée entre les plaques subit la même force où qu'elle soit. En haut, en bas, au milieu, c'est pareil.",
   "Et cela se lit comme une pente : on descend de U volts en parcourant d mètres. Rapproche les plaques, et le champ augmente sans toucher à la tension.",
 ]),
 ("lignescondo", "Les lignes dans le condensateur", [
   "Quatrième point, et c'est une question de cours qui tombe presque toujours : les lignes de champ dans un condensateur, loin des bords.",
   "Trois caractéristiques à savoir énoncer. Le barème donne souvent un point pour chacune.",
   "Une : elles sont perpendiculaires aux plaques.",
   "Deux : elles sont orientées de la plaque positive vers la plaque négative.",
   "Trois : elles sont parallèles entre elles et régulièrement espacées. C'est la traduction graphique du mot uniforme.",
   "Les équipotentielles, elles, sont parallèles aux plaques, donc perpendiculaires aux lignes de champ. On les trace en pointillés, pour ne pas les confondre avec les lignes de champ.",
   "Et maintenant, pourquoi l'énoncé précise loin des bords ? Parce qu'au bord des plaques, les lignes s'évasent et débordent : là, le champ n'est plus uniforme. Seule la région centrale l'est.",
 ]),
 ("exE", "Exemple — le champ uniforme", [
   "Exemple chiffré, et il est court.",
   "Deux plaques distantes de huit virgule zéro millimètres, sous une tension de deux cent quarante volts. Que vaut le champ entre elles, et quelle force subit une charge de plus cinq virgule zéro nanocoulombs placée dedans ?",
   "Le champ : E égale U sur d, donc deux cent quarante divisé par huit millimètres.",
   "Attention à la conversion : huit millimètres, c'est huit fois dix puissance moins trois mètre. On trouve trois virgule zéro fois dix puissance quatre volts par mètre.",
   "La force : F égale q E, donc cinq fois dix puissance moins neuf, multiplié par trois fois dix puissance quatre.",
   "Cela fait un virgule cinq fois dix puissance moins quatre newtons, dirigée de la plaque positive vers la plaque négative, puisque la charge est positive.",
 ]),
 ("cartes", "Tracer une carte de champ", [
   "Cinquième point : les lignes de champ entre deux charges. Avant de dessiner, les cinq règles de tracé.",
   "Une : les lignes sortent des charges positives et entrent dans les charges négatives.",
   "Deux : le vecteur champ est tangent à la ligne, et la flèche en donne le sens.",
   "Trois : deux lignes ne se croisent jamais, sinon le champ aurait deux directions au même endroit.",
   "Quatre : là où les lignes se serrent, le champ est plus intense ; là où elles s'écartent, il est plus faible.",
   "Cinq : elles partent et arrivent perpendiculairement à la surface des charges et des conducteurs.",
   "Ces cinq règles suffisent à dessiner les deux cas du test. Les voici, l'un après l'autre.",
 ]),
 ("dipole", "Deux charges de signes opposés", [
   "Premier cas : deux charges de même valeur et de signes opposés.",
   "Toutes les lignes partent de la charge positive et finissent sur la charge négative. Aucune ne s'arrête dans le vide.",
   "Celle qui joint les deux charges est un segment de droite, et c'est le long de cet axe que le champ est le plus fort.",
   "Les autres s'écartent de part et d'autre, en boucles de plus en plus larges, qui contournent les deux charges.",
   "La figure est symétrique par rapport à l'axe des deux charges, et il n'existe nulle part de point où le champ s'annule.",
   "Au milieu du segment, les deux charges donnent des champs dans le même sens : ils s'additionnent. Le champ y est maximal, et dirigé du plus vers le moins.",
 ]),
 ("memesigne", "Deux charges de même signe", [
   "Deuxième cas : deux charges de même valeur et de même signe. Prenons-les positives toutes les deux.",
   "Les lignes sortent des deux charges, et aucune ne va de l'une à l'autre : elles s'écartent vers l'extérieur, comme si elles se repoussaient.",
   "Entre les deux charges, l'image a une particularité qu'il faut savoir nommer : il existe un point où le champ est nul.",
   "Il est exactement au milieu, parce que les deux charges ont la même valeur : les deux champs y sont égaux et opposés, donc leur somme est nulle.",
   "Et cela se voit sur le dessin : la région du milieu est vide de lignes, et celles qui s'en approchent s'écartent de part et d'autre.",
   "Si les deux charges étaient négatives, le dessin serait identique, avec toutes les flèches inversées : les lignes entreraient dans les charges au lieu d'en sortir.",
 ]),
 ("cartespieges", "Les deux cartes côte à côte", [
   "Mets les deux cartes côte à côte : c'est ainsi qu'on les retient.",
   "Signes opposés : les lignes relient les deux charges, et le champ est maximal au milieu.",
   "Même signe : les lignes se repoussent, et le champ est nul au milieu.",
   "Les trois erreurs qui coûtent des points : oublier les flèches, faire se croiser deux lignes, et laisser une ligne s'arrêter en plein milieu du papier.",
   "Et si l'énoncé demande aussi les équipotentielles, souviens-toi qu'elles coupent toujours les lignes de champ à angle droit.",
 ]),
 ("mdisp", "L'expérience de Millikan", [
   "Sixième point, le gros morceau : l'expérience de Millikan, en mille neuf cent neuf.",
   "La question qu'elle pose est simple à énoncer : quelle est la plus petite charge électrique qui existe ?",
   "Le dispositif. Un pulvérisateur envoie un brouillard de gouttelettes d'huile au-dessus de deux plaques horizontales.",
   "Quelques gouttes tombent par un petit trou percé dans la plaque du haut, et se retrouvent entre les deux plaques.",
   "Là, une source de rayons X ionise l'air de la chambre, et un microscope permet de suivre une goutte à l'œil.",
   "Enfin, une alimentation réglable fixe la tension U entre les plaques. C'est le seul bouton de l'expérience, et c'est lui qu'on tourne.",
 ]),
 ("mroles", "Le rôle de chaque pièce", [
   "Le barème demande presque toujours le rôle de chaque pièce. Trois réponses à savoir donner.",
   "Les rayons X : ils ionisent l'air, c'est-à-dire qu'ils arrachent des électrons à ses molécules. Chaque gouttelette en capte ou en perd quelques-uns, et porte donc une charge. Sans eux, les gouttes seraient neutres et le champ n'aurait aucune prise sur elles.",
   "Le microscope : les gouttes mesurent quelques micromètres, on ne les voit pas à l'œil nu. Il sert à observer une goutte isolée, à mesurer son rayon, donc sa masse, et à voir si elle monte, descend ou reste immobile.",
   "Et les trois situations, pour une goutte négative avec la plaque du haut positive. Si la force électrique est plus grande que le poids, la goutte monte.",
   "Si la force électrique est plus petite que le poids, la goutte descend.",
   "Et si les deux sont exactement égales, la goutte reste en suspension, parfaitement immobile. C'est ce cas, et seulement celui-là, qui permet de calculer la charge.",
 ]),
 ("mdemo", "La démonstration à savoir", [
   "La démonstration à savoir refaire. Trois points au barème, trois lignes de calcul.",
   "La goutte est immobile, donc les deux forces qu'elle subit se compensent exactement : la force électrique est égale au poids.",
   "Ligne une : q E égale m g.",
   "Ligne deux : entre deux plaques, E vaut U sur d. On remplace, et il vient q fois U sur d égale m g.",
   "Ligne trois : on isole q. On obtient q égale m g d divisé par U.",
   "Chaque ligne est une formule du cours : rien n'est deviné. Et retiens le sens physique : plus la goutte est lourde, plus il faut de charge pour la tenir ; plus la tension est forte, moins il en faut.",
 ]),
 ("mgraphe", "Interpréter les résultats", [
   "Millikan recommence sur des milliers de gouttes. Voici le résultat pour cinquante d'entre elles, et c'est ce graphique qu'on demande d'interpréter.",
   "Ce qu'il faut voir, et le dire avec ces mots : les points ne sont pas répartis au hasard, ils s'alignent sur des droites horizontales.",
   "Autrement dit, certaines valeurs de charge se rencontrent, et les valeurs intermédiaires ne se rencontrent jamais.",
   "Toutes les charges mesurées sont des multiples entiers d'une même petite charge : q égale n fois e, avec n entier.",
   "Cette charge e est la charge élémentaire : un virgule six fois dix puissance moins dix-neuf coulombs. Les petits écarts autour de chaque palier viennent des incertitudes de mesure.",
   "La comparaison qui fait tout comprendre : si tu pèses des sachets de pièces de deux euros, tu trouveras deux, quatre, six euros, jamais trois euros quarante. L'existence de paliers prouve l'existence d'une pièce élémentaire.",
 ]),
 ("mtable", "L'analyse des données", [
   "Passons au sixième point : l'analyse des données. C'est la correction que nous avons vue en classe, et c'est une méthode, donc elle s'apprend.",
   "On a mesuré six gouttelettes, avec des plaques distantes de deux virgule soixante-seize millimètres. Pour chacune, on connaît la tension qui l'immobilise et sa masse.",
   "Première étape : calculer la charge de chaque goutte, avec la formule démontrée tout à l'heure.",
   "Faisons la première en entier. La masse vaut six virgule seize fois dix puissance moins seize kilogrammes, g vaut neuf virgule quatre-vingt-un, d vaut deux virgule soixante-seize fois dix puissance moins trois mètres, et U vaut cinquante-deux volts.",
   "On remplace, on calcule, et on obtient trois virgule vingt-un fois dix puissance moins dix-neuf coulombs.",
   "Deux pièges d'unités, et ce sont les seuls : la masse est donnée en dix puissance moins seize kilogrammes, et la distance en millimètres. Les deux sont à convertir avant de taper sur la calculatrice.",
 ]),
 ("mresult", "Trouver la charge élémentaire", [
   "On refait ce calcul pour les six gouttes. Voici les charges obtenues, en dix puissance moins dix-neuf coulombs.",
   "Trois virgule vingt-un ; un virgule cinquante-neuf ; quatre virgule soixante-quatorze ; un virgule soixante-trois ; trois virgule vingt-huit ; six virgule quarante-sept.",
   "Deuxième étape : repérer la plus petite valeur. Ici, deux gouttes sont au même niveau, la deux et la quatre : un virgule cinquante-neuf et un virgule soixante-trois.",
   "Comme elles sont sur le même palier, on prend leur moyenne, ce qui réduit l'erreur de mesure. On obtient un virgule soixante et un fois dix puissance moins dix-neuf coulombs.",
   "Troisième étape, et c'est celle qu'on te demande d'expliquer : diviser toutes les charges par cette valeur, puis regarder les résultats.",
   "On trouve un virgule quatre-vingt-dix-neuf ; zéro virgule quatre-vingt-dix-neuf ; deux virgule quatre-vingt-quatorze ; un virgule zéro un ; deux virgule zéro quatre ; quatre virgule zéro deux.",
   "Quatrième étape : conclure. Dans la marge d'erreur, ce sont tous des entiers : deux, un, trois, un, deux, quatre.",
   "Donc toutes les charges mesurées sont des multiples entiers de un virgule soixante et un fois dix puissance moins dix-neuf coulombs. Cette valeur est la charge élémentaire.",
   "Et le contrôle qui ne coûte rien : la valeur admise est un virgule six cent deux fois dix puissance moins dix-neuf coulombs. Nous sommes à moins d'un pour cent.",
 ]),
 ("quant", "Quantifié, au sens précis", [
   "Mettons maintenant un mot propre sur ce qu'on vient de montrer, parce que c'est la question de cours qui accompagne toujours ce tableau.",
   "Une grandeur est quantifiée quand elle ne peut prendre que certaines valeurs isolées, par paquets, et jamais les valeurs intermédiaires.",
   "L'image à retenir : une rampe est continue, on peut s'arrêter à n'importe quelle hauteur. Un escalier est quantifié : on ne peut se tenir que sur les marches.",
   "Et voici la formulation complète, celle qui vaut tous les points. La grandeur ne prend que les valeurs x égale a fois f de n, où n est un nombre entier et a une constante.",
   "Pour la charge électrique, f de n, c'est tout simplement n : la charge vaut n fois e. C'est ce que nous venons de vérifier sur les six gouttes.",
   "Mais ce n'est pas toujours n. Dans d'autres situations, la fonction est n au carré, ou un sur n, ou un sur n au carré. Et on peut te demander de trouver laquelle.",
 ]),
 ("famille", "Quelle fonction de n ?", [
   "La méthode est mécanique, et c'est une bonne nouvelle.",
   "On range les valeurs mesurées dans l'ordre, et on leur attribue les entiers n égale un, deux, trois, quatre.",
   "Puis, pour chaque fonction candidate, on divise chaque mesure par f de n, et on regarde si on retombe toujours sur le même nombre.",
   "La bonne fonction est celle qui donne une colonne constante. Et ce nombre constant, c'est la constante a.",
   "Un exemple vrai, que tu reverras en physique quantique. Les énergies des niveaux de l'atome d'hydrogène valent treize virgule six, trois virgule quarante, un virgule cinquante et un, et zéro virgule quatre-vingt-cinq électronvolts.",
   "On divise par n : treize virgule six, un virgule sept, zéro virgule cinq, zéro virgule deux. Cela diminue, donc ce n'est pas n.",
   "On divise par n au carré : cela diminue encore plus vite. Ce n'est pas n au carré non plus.",
   "On divise par un sur n, ce qui revient à multiplier par n : treize virgule six, six virgule huit, quatre virgule cinq, trois virgule quatre. Toujours pas constant.",
   "On divise par un sur n au carré, ce qui revient à multiplier par n au carré : treize virgule six, treize virgule six, treize virgule six, treize virgule six. Constant.",
   "Conclusion, et c'est la phrase à écrire : l'énergie ne prend que des valeurs discrètes, et elle est proportionnelle à un sur n au carré. Même méthode et même rédaction que pour la charge.",
 ]),
 ("pourquoi", "Pourquoi c'est important", [
   "Dernière question du barème, et deux lignes suffisent : pourquoi l'expérience de Millikan compte-t-elle autant ?",
   "Parce qu'en physique classique, on supposait toutes les grandeurs continues : on pensait pouvoir couper n'importe quelle quantité en morceaux aussi petits qu'on veut.",
   "Millikan montre que la charge, elle, est un escalier. C'est la première grandeur dont on prouve expérimentalement la quantification.",
   "Cela a ouvert l'idée que d'autres grandeurs pourraient l'être aussi. Et c'est exactement ce qu'on a trouvé : l'énergie de la lumière, avec les photons, puis les niveaux d'énergie des atomes.",
   "La différence importante entre physique classique et physique quantique, c'est ce mot : la quantification. Millikan, prix Nobel mille neuf cent vingt-trois, en est le premier exemple.",
 ]),
 ("fiche", "La fiche de révision", [
   "La fiche de révision, en cinq lignes. Si tu ne retiens que cette image, tu as l'essentiel.",
   "La force de Coulomb : F égale k Q q sur r au carré, avec k égale neuf fois dix puissance neuf.",
   "Le champ et la force : E égale F sur q, et la force vaut q fois E.",
   "Le champ uniforme entre deux plaques : E égale U sur d.",
   "La goutte en suspension : q E égale m g, qui donne q égale m g d sur U.",
   "Et la quantification : q égale n fois e, avec e égale un virgule six zéro fois dix puissance moins dix-neuf coulombs.",
 ]),
 ("final", "Avant de rendre la copie", [
   "Pour finir, la liste de contrôle à relire cinq minutes avant le test.",
   "Les unités du système international avant tout calcul : mètres, kilogrammes, coulombs, volts.",
   "Le carré de la distance porte aussi sur la puissance de dix.",
   "Sur un schéma de lignes de champ : des flèches partout, aucun croisement, et perpendiculaires aux plaques et aux conducteurs.",
   "Pour le mot uniforme, dire les trois : même direction, même sens, même valeur.",
   "Et pour l'analyse de données : trouver la plus petite valeur, diviser toutes les mesures par elle, montrer que les rapports sont des entiers, puis conclure.",
   "Tu as les six points. Bon test.",
 ]),
]

if __name__ == "__main__":
    n = sum(len(s[2]) for s in SCENES)
    mots = sum(len(p.split()) for s in SCENES for p in s[2])
    print("%d scènes, %d phrases, %d mots → environ %.1f min"
          % (len(SCENES), n, mots, mots / 168.0))
