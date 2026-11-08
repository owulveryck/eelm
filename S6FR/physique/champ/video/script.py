# -*- coding: utf-8 -*-
"""Narration du chapitre « Champ électrique ».

Fil directeur : la gouttelette d'encre d'une imprimante à jet d'encre, et un
exemple chiffré résolu après chaque notion. Les formules sont écrites en toutes
lettres : ce texte est lu tel quel par la synthèse vocale, et sert aussi de
sous-titres. Une entrée de SCENES = (identifiant de la scène dans scenes.py,
titre du bandeau, liste des phrases) ; une phrase = un plan.
"""

SORTIE = "cours-champ-electrique.mp4"   # nom du fichier produit, à côté du chapitre
VOIX = "fr-FR-Chirp3-HD-Charon"
RATE = 0.92

SCENES = [
 ("titre", "Champ électrique", [
   "Une imprimante à jet d'encre projette dix mille gouttelettes par seconde.",
   "Chacune doit arriver sur le papier à un dixième de millimètre près, sans que rien ne la touche.",
   "Comment fait-elle pour viser ?",
   "La réponse, c'est tout ce chapitre. Nous allons la construire morceau par morceau, et à la fin, nous ferons le calcul complet.",
 ]),
 ("enigme", "Le fil directeur", [
   "Voici le dispositif. Un canon produit les gouttes. Chacune passe devant une électrode qui lui dépose une charge, plus ou moins grande, à la demande de l'ordinateur.",
   "Puis la goutte traverse deux plaques métalliques entre lesquelles règne un champ électrique.",
   "Elle en ressort déviée, et vient se poser sur le papier, exactement là où il faut.",
   "Pour comprendre ça, il nous manque quatre choses : ce qu'est une charge, comment deux charges s'attirent, ce qu'est un champ, et comment on le fabrique entre deux plaques.",
   "Prenons-les dans l'ordre. À chaque étape, nous ferons un exemple chiffré, en entier.",
 ]),
 ("charge", "La charge électrique", [
   "Toute la matière est faite d'atomes : un noyau, avec des protons positifs, et autour, des électrons négatifs.",
   "Dans un atome normal, il y a autant d'électrons que de protons. Les charges se compensent exactement : l'atome est neutre.",
   "Mais les électrons extérieurs sont mal retenus. En frottant deux matériaux, on en arrache à l'un pour les donner à l'autre.",
   "L'objet qui perd des électrons devient positif, puisqu'il lui manque du négatif. Celui qui en gagne devient négatif.",
   "On ne fabrique donc jamais de charge : on la déplace. Ce qui est positif quelque part manque ailleurs.",
   "La charge se note q et se mesure en coulombs. La plus petite qui existe est celle de l'électron : la charge élémentaire e.",
   "Elle vaut un virgule six zéro fois dix puissance moins dix-neuf coulombs. Et toute charge est un multiple entier de celle-là.",
 ]),
 ("ex1", "Exemple 1 — la charge d'une goutte", [
   "Premier exemple, et il fait déjà partie de notre fil directeur.",
   "L'électrode de charge dépose cinquante mille électrons en trop sur une gouttelette. Quelle charge porte-t-elle ?",
   "On écrit la formule en lettres : q égale n fois e.",
   "On remplace : cinquante mille, c'est cinq fois dix puissance quatre. Multiplié par un virgule six fois dix puissance moins dix-neuf.",
   "Les puissances de dix s'additionnent : quatre moins dix-neuf, ça fait moins quinze.",
   "Résultat : huit fois dix puissance moins quinze coulombs. Négative, puisque ce sont des électrons.",
   "Retiens ce nombre, nous le réutiliserons à la fin.",
 ]),
 ("regles", "Les deux règles d'or", [
   "Deuxième brique : comment deux charges agissent l'une sur l'autre.",
   "Première règle : deux charges de même signe se repoussent, deux charges de signes opposés s'attirent.",
   "Deuxième règle, moins intuitive : les deux forces ont toujours exactement la même valeur, même si une charge est mille fois plus grande que l'autre.",
   "Et le cas qui gêne tout le monde : pourquoi une règle chargée attire-t-elle du papier, qui n'est ni positif ni négatif ?",
   "Parce que le papier se polarise : sous l'influence de la règle, les charges se déplacent un tout petit peu à l'intérieur. Les positives se tournent vers la règle, les négatives s'en écartent.",
   "Les positives sont donc plus proches, et comme nous allons le voir, ce qui est plus proche compte beaucoup plus. L'attraction l'emporte.",
 ]),
 ("coulomb", "La loi de Coulomb", [
   "Maintenant, la valeur de cette force. C'est la loi de Coulomb.",
   "F égale k, fois la valeur absolue de Q, fois la valeur absolue de q, le tout divisé par r au carré.",
   "Q et q sont les deux charges, en coulombs. r est la distance qui les sépare, en mètres. Et k est une constante qui vaut neuf fois dix puissance neuf.",
   "Les valeurs absolues servent à obtenir un nombre positif : la valeur de la force. Le sens, lui, est donné par les signes, avec les deux règles d'or.",
   "Fais bien attention à une chose : la distance est au carré. C'est ce carré qui fait tout le caractère de cette force.",
 ]),
 ("ex2", "Exemple 2 — deux sphères chargées", [
   "Deuxième exemple, en entier.",
   "Deux petites sphères portent, l'une plus trois virgule zéro nanocoulombs, l'autre moins cinq virgule zéro nanocoulombs. Elles sont distantes de quatre virgule zéro centimètres. Quelle force subissent-elles ?",
   "Étape une : la formule en lettres. F égale k Q q sur r au carré.",
   "Étape deux : tout convertir en unités du système international. Un nanocoulomb, c'est dix puissance moins neuf coulombs. Quatre centimètres, c'est quatre fois dix puissance moins deux mètres.",
   "Étape trois : on remplace. Au numérateur, neuf fois dix puissance neuf, fois trois fois dix puissance moins neuf, fois cinq fois dix puissance moins neuf.",
   "Au dénominateur, attention au piège le plus fréquent : le carré porte aussi sur la puissance de dix. Quatre fois dix puissance moins deux, au carré, ça fait un virgule six fois dix puissance moins trois.",
   "Étape quatre : on calcule. Huit virgule quatre fois dix puissance moins cinq newtons.",
   "Étape cinq : on vérifie et on interprète. Les charges sont de signes opposés, donc les deux forces sont attractives, dirigées l'une vers l'autre, et elles valent chacune la même chose.",
 ]),
 ("carre", "Le poids du carré", [
   "Revenons sur ce carré, parce qu'il permet de répondre à beaucoup de questions sans calculatrice.",
   "Deux charges d'un microcoulomb, à un centimètre l'une de l'autre, se repoussent avec quatre-vingt-dix newtons. C'est le poids d'un sac de neuf kilos, pour un millionième de coulomb.",
   "On double la distance : la force n'est pas divisée par deux, mais par quatre. On la triple : elle est divisée par neuf.",
   "C'est la technique du rapport : si la distance est multipliée par n, la force est divisée par n au carré. Si une charge est multipliée par n, la force est multipliée par n.",
   "Pourquoi un carré ? Pense à une ampoule : sa lumière s'étale sur une sphère. Deux fois plus loin, la même lumière couvre une sphère quatre fois plus grande, donc tu en reçois quatre fois moins.",
 ]),
 ("vecteur", "Vecteurs", [
   "Troisième brique : les flèches.",
   "Dire que la force vaut quatre-vingt-dix newtons ne suffit pas. Il faut savoir vers où elle pousse. C'est le rôle du vecteur.",
   "Il faut distinguer deux écritures. Le vecteur force, avec une flèche au-dessus : c'est une flèche, avec une valeur et une orientation. Et sa norme, sans flèche : un nombre, toujours positif.",
   "Une norme n'est jamais négative. C'est le vecteur qui porte le sens, jamais le nombre.",
   "Dans les formules du cours apparaît aussi le vecteur u : une flèche de longueur un, sans unité, qui pointe de la charge source vers l'autre charge. Elle ne sert qu'à donner la direction.",
   "Son intérêt : avec elle, une seule formule suffit pour l'attraction et pour la répulsion, parce que le signe du produit Q fois q s'occupe du sens tout seul.",
 ]),
 ("ex3", "Exemple 3 — additionner deux flèches", [
   "Troisième exemple : additionner deux vecteurs. C'est l'opération qui revient dans tous les exercices à plusieurs charges.",
   "On ne additionne surtout pas les longueurs. On met les flèches bout à bout : la somme est la flèche qui va du départ de la première à la pointe de la seconde.",
   "Par le calcul, c'est plus sûr : on additionne les coordonnées séparément, en x puis en y.",
   "Puis on retrouve la longueur avec Pythagore : racine de x au carré plus y au carré.",
   "Prends deux champs perpendiculaires, de trois et quatre volts par mètre. Trois et quatre ne font pas sept : la résultante vaut racine de neuf plus seize, c'est-à-dire cinq.",
 ]),
 ("champ", "Le champ électrique", [
   "Nous arrivons au cœur du chapitre.",
   "Pose une charge d'essai quelque part et mesure la force : le résultat dépend de la charge que tu as choisie. Prends une charge deux fois plus grande, tu obtiens une force deux fois plus grande.",
   "Ce n'est donc pas une bonne description de l'espace lui-même. La solution tient en un geste : on divise la force par la charge d'essai.",
   "Ce rapport, lui, ne dépend plus de ce qu'on a posé. C'est le champ électrique : E égale F divisé par la valeur absolue de q.",
   "Le champ, c'est la force par unité de charge. Et la relation se retourne : une charge q posée dans un champ E subit une force égale à q fois E.",
   "L'analogie la plus utile du chapitre, c'est la pesanteur. Une masse crée un champ de pesanteur, et un objet posé dedans subit son poids, m fois g. Ici, une charge crée un champ électrique, et une charge posée dedans subit q fois E.",
   "Et retiens bien ceci : le champ existe déjà, même si on ne pose rien dedans. La charge d'essai ne fait que le révéler.",
 ]),
 ("radial", "Le champ d'une charge seule", [
   "Si c'est une charge ponctuelle Q qui crée le champ, on connaît déjà la force, par Coulomb. Il suffit de diviser par q.",
   "Et q disparaît. Il reste : E égale k, valeur absolue de Q, divisé par r au carré.",
   "Ce champ est radial : ses flèches sont portées par les rayons qui partent de la charge, comme les rayons d'une roue.",
   "Si la charge est positive, il fuit le centre : on dit centrifuge. Si elle est négative, il pointe vers le centre : centripète.",
   "Et comme la force, il décroît en un sur r au carré. À deux fois plus loin, il est quatre fois plus faible.",
 ]),
 ("ex4", "Exemple 4 — le dôme de Van de Graaff", [
   "Quatrième exemple. Le dôme d'un générateur de Van de Graaff est une sphère de rayon vingt centimètres, qui porte une charge de quinze microcoulombs. Quel est le champ à sa surface ?",
   "Première remarque, qui vaut des points : pour une sphère chargée, tout se passe, à l'extérieur, comme si toute la charge était concentrée en son centre. On peut donc utiliser la formule de la charge ponctuelle, avec r mesuré depuis le centre.",
   "On écrit en lettres, on convertit, on remplace : quinze microcoulombs, c'est quinze fois dix puissance moins six. Vingt centimètres, c'est zéro virgule vingt mètre, et au carré, quatre fois dix puissance moins deux.",
   "On obtient trois virgule quatre fois dix puissance six volts par mètre.",
   "Maintenant, l'interprétation, c'est elle qui compte. L'air sec devient conducteur au-delà de trois fois dix puissance six volts par mètre.",
   "Nous sommes au-dessus. Donc des étincelles vont jaillir du dôme : c'est exactement ce qu'on observe.",
 ]),
 ("lignes", "Les lignes de champ", [
   "Dessiner une flèche en chaque point serait illisible. On trace donc des lignes de champ : des courbes qui suivent les flèches.",
   "Cinq règles de lecture, et elles tombent toutes en contrôle.",
   "Un : le vecteur champ est tangent à la ligne en chaque point. Deux : les lignes sortent des charges positives et entrent dans les charges négatives.",
   "Trois : elles ne se croisent jamais, sinon le champ aurait deux directions au même endroit.",
   "Quatre : là où les lignes sont serrées, le champ est intense ; là où elles s'écartent, il est faible.",
   "Cinq : elles arrivent perpendiculairement à la surface d'un conducteur chargé.",
   "Attention à un piège : ces points qui défilent sur l'animation ne sont pas des charges qui se déplacent. C'est seulement une façon de montrer le sens du champ.",
 ]),
 ("ex5", "Exemple 5 — deux charges, un point", [
   "Cinquième exemple : le principe de superposition, en chiffres.",
   "Quand il y a plusieurs charges, chacune crée son champ comme si les autres n'existaient pas, et on additionne les flèches.",
   "Deux charges, plus quatre virgule zéro nanocoulombs et plus deux virgule zéro nanocoulombs, sont distantes de six virgule zéro centimètres. Que vaut le champ au milieu du segment ?",
   "Le milieu est à trois centimètres de chacune. On calcule les deux champs séparément.",
   "Le premier vaut quatre fois dix puissance quatre volts par mètre, le second deux fois dix puissance quatre.",
   "Les deux charges sont positives, donc au milieu, leurs champs pointent en sens contraires : l'un vers la droite, l'autre vers la gauche. On les soustrait.",
   "Résultat : deux fois dix puissance quatre volts par mètre, dirigé vers la charge la plus faible. Et quelque part, plus près de la petite charge, il existe un point où le champ s'annule complètement.",
 ]),
 ("potdef", "Qu'est-ce que le potentiel ?", [
   "Il reste une notion, et c'est la plus abstraite du chapitre : le potentiel. Construisons-la lentement, parce que tout le monde la confond avec le champ.",
   "Souviens-toi de ce qu'on a fait pour le champ. La force dépend de deux choses : de la charge qu'on pose, et de l'endroit. En divisant la force par la charge, on a supprimé la charge d'épreuve ; il ne restait que l'endroit. C'est ça, le champ.",
   "Le potentiel, c'est exactement la même opération, mais avec l'énergie à la place de la force.",
   "Une charge posée quelque part possède une énergie, comme une pierre tenue en l'air possède une énergie de position. Et si je double la charge, je double cette énergie : elle dépend donc encore de ce que j'ai posé là.",
   "Alors on divise par la charge. L'énergie par unité de charge, elle, ne dépend plus que de l'endroit : c'est le potentiel, noté V.",
   "Son unité est le joule par coulomb, et on lui a donné un nom : le volt. Un volt, c'est un joule par coulomb, rien de plus.",
   "C'est exactement ce qu'annonce une pile de douze volts : chaque coulomb qui la traverse reçoit douze joules. Le volt n'est pas une quantité d'électricité, c'est une énergie par charge.",
   "Retiens les deux divisions côte à côte. Le champ, c'est la force par unité de charge ; le potentiel, c'est l'énergie par unité de charge. Le premier est une flèche, le second un simple nombre.",
 ]),
 ("potentiel", "Le potentiel", [
   "Maintenant qu'on sait ce que V mesure, une analogie rend tout le reste simple : le relief.",
   "Le potentiel d'un point, noté V, c'est son altitude électrique, en volts. La tension entre deux points, notée U, c'est la dénivelée : U égale V en A moins V en B.",
   "Les surfaces équipotentielles sont les courbes de niveau : tous les points à la même altitude électrique. Et le champ, c'est la pente.",
   "Deux conséquences qu'il faut savoir énoncer. Le champ est toujours perpendiculaire aux équipotentielles, comme la ligne de plus grande pente coupe les courbes de niveau à angle droit. Et il pointe vers les potentiels décroissants : ça descend.",
   "Autour d'une charge ponctuelle, le potentiel vaut k Q sur r. Attention : sur r, pas sur r au carré. Le potentiel décroît moins vite que le champ.",
   "Et c'est un simple nombre, avec un signe : pour additionner les potentiels de plusieurs charges, on additionne des nombres, pas des flèches. C'est bien plus facile.",
 ]),
 ("ex6", "Exemple 6 — le potentiel d'une sphère", [
   "Sixième exemple, très court. Une sphère conductrice isolée, de rayon douze centimètres, reçoit une charge de zéro virgule seize nanocoulomb. Quel est son potentiel ?",
   "On applique V égale k Q sur r, avec r depuis le centre, comme tout à l'heure.",
   "Neuf fois dix puissance neuf, fois zéro virgule seize fois dix puissance moins neuf, divisé par zéro virgule douze.",
   "Cela fait douze volts.",
   "Et tout le métal est à douze volts : dans un conducteur, le potentiel est le même partout, et le champ à l'intérieur est nul. C'est le principe de la cage de Faraday.",
 ]),
 ("plaques", "Entre deux plaques", [
   "Dernière brique, et c'est celle qu'il nous manquait pour l'imprimante.",
   "Deux plaques parallèles reliées à un générateur forment un condensateur plan. Entre elles, le champ est uniforme : même direction, même sens, même valeur partout.",
   "Il vaut E égale U divisé par d, où U est la tension et d l'écartement des plaques.",
   "Cela se lit comme une pente : on descend de U volts en parcourant d mètres.",
   "Double la tension, le champ double. Rapproche les plaques, le champ augmente aussi. C'est pour cela qu'un petit condensateur avec des plaques très proches produit un champ énorme avec une pile ordinaire.",
   "Exemple sept, immédiat : deux cents volts sur dix centimètres donnent deux fois dix puissance trois volts par mètre.",
 ]),
 ("energie", "Travail et énergie", [
   "Une dernière relation, pour relier tout cela à l'énergie.",
   "Par définition du volt, un coulomb qui passe sous un volt échange un joule. Donc le travail vaut q fois la variation de potentiel.",
   "Exemple huit : une charge de deux coulombs passe d'un point à cinquante volts à un point à trente-cinq volts. Elle perd deux fois quinze, soit trente joules, convertis en énergie cinétique.",
   "Et la conséquence la plus utile : si la charge se déplace le long d'une équipotentielle, la variation de potentiel est nulle, donc le travail est nul.",
   "Exactement comme marcher à flanc de colline en suivant une courbe de niveau : ça ne coûte rien.",
 ]),
 ("fil1", "Retour à la goutte — le champ", [
   "Nous avons toutes les pièces. Revenons à notre imprimante, et faisons le calcul complet.",
   "Les plaques de déviation sont distantes de douze millimètres, et la tension entre elles est de mille deux cents volts.",
   "Premier calcul : le champ entre les plaques. E égale U sur d.",
   "Mille deux cents divisé par zéro virgule zéro douze mètre. Attention aux millimètres : douze millimètres, c'est douze fois dix puissance moins trois mètres.",
   "Cela donne un fois dix puissance cinq volts par mètre. Un champ considérable, obtenu avec une alimentation de laboratoire tout à fait ordinaire.",
 ]),
 ("fil2", "Retour à la goutte — la force", [
   "Deuxième calcul : la force sur notre gouttelette.",
   "Elle porte la charge trouvée au premier exemple : huit fois dix puissance moins quinze coulombs.",
   "La force vaut q fois E : huit fois dix puissance moins quinze, multiplié par un fois dix puissance cinq.",
   "Huit fois dix puissance moins dix newtons. Un nombre minuscule… mais tout est minuscule, ici.",
   "La bonne question, c'est : est-ce beaucoup, pour une goutte ? Comparons à son poids. La goutte pèse environ un virgule trois fois dix puissance moins onze kilogrammes, donc son poids vaut un virgule trois fois dix puissance moins dix newtons.",
   "La force électrique est plus de six fois plus grande que le poids. C'est elle qui commande la trajectoire : la gravité est négligeable devant elle.",
 ]),
 ("fil3", "Retour à la goutte — viser", [
   "Troisième et dernière étape : viser.",
   "Le champ entre les plaques ne change jamais. La seule chose qui change d'une goutte à l'autre, c'est la charge que l'électrode lui a déposée.",
   "Et comme la force vaut q fois E, la déviation est proportionnelle à la charge. L'ordinateur n'a donc qu'à choisir la charge pour choisir le point d'arrivée.",
   "Les gouttes qui ne doivent pas être imprimées, celles des espaces entre les mots, ne reçoivent aucune charge : elles filent tout droit et sont récupérées dans une gouttière.",
   "Voilà la réponse à la question du début. Elle tient en trois formules que tu connais maintenant : q égale n e, E égale U sur d, et F égale q E.",
 ]),
 ("millikan", "Le même montage, à l'envers", [
   "Une remarque pour finir, parce qu'elle est belle.",
   "Le même dispositif, deux plaques et une gouttelette chargée, a servi à Millikan en mille neuf cent neuf pour mesurer la charge de l'électron.",
   "Au lieu de dévier la goutte, il règle la tension jusqu'à ce qu'elle reste parfaitement immobile.",
   "À l'équilibre, la force électrique compense exactement le poids : q fois E égale m g. Et comme E vaut U sur d, on en tire q égale m g d divisé par U.",
   "Avec une goutte de quatre fois dix puissance moins quinze kilogrammes, des plaques à vingt millimètres et mille deux cents volts, on trouve six virgule sept fois dix puissance moins dix-neuf coulombs. C'est-à-dire environ quatre fois la charge élémentaire : jamais trois et demi, jamais quatre et quart. La charge est quantifiée.",
 ]),
 ("methode", "La méthode, et les pièges", [
   "Tous les exemples de cette vidéo ont suivi la même méthode. La voici en cinq étapes.",
   "Un : faire un schéma, avec les charges, leurs signes, et le point où l'on cherche quelque chose.",
   "Deux : reconnaître la situation. Il n'y en a que trois dans ce chapitre : une charge ponctuelle, deux plaques, ou plusieurs charges à superposer.",
   "Trois : écrire la formule en lettres, et seulement ensuite remplacer par les nombres. C'est ce que paie le barème.",
   "Quatre : convertir en unités du système international, avant de calculer. Les centimètres, les millimètres et les nanocoulombs ne se mettent jamais dans une formule.",
   "Cinq : vérifier. L'unité est-elle la bonne ? L'ordre de grandeur est-il plausible ? Le sens de la flèche est-il cohérent avec les signes ?",
   "Et trois pièges à connaître : le carré qui porte aussi sur la puissance de dix, les normes qu'on additionne au lieu des vecteurs, et la charge négative, pour laquelle force et champ sont de sens opposés.",
 ]),
 ("final", "Ce qu'il faut retenir", [
   "Résumons. Tout le chapitre tient dans cinq relations.",
   "La loi de Coulomb, pour la force entre deux charges.",
   "La définition du champ, force par unité de charge, et sa réciproque : la force vaut q fois E.",
   "Le champ d'une charge ponctuelle, qui décroît en un sur r au carré.",
   "Le champ uniforme entre deux plaques, qui vaut U sur d.",
   "Et le travail, qui vaut q fois la variation de potentiel.",
   "Cinq relations, une méthode en cinq étapes, et une gouttelette d'encre pour tout relier. Bon travail.",
 ]),
]

if __name__ == "__main__":
    n = sum(len(s[2]) for s in SCENES)
    mots = sum(len(p.split()) for s in SCENES for p in s[2])
    print("%d scènes, %d phrases, %d mots → environ %.1f min"
          % (len(SCENES), n, mots, mots / 168.0))
