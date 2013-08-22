OBSOLETTE
*********

L'application Tirelire
======================

Tirelire est une application dédiée à la gestion domestique mensuelle.
Elle est là pour vous aider à prévoir vos dépenses en simulant des
mini-tirelires, appellées Cochons, dans lesquelles vous irez chercher l'argent
en fonction du type de dépense. Pour approvisionner vos cochons, vous pouvez
mettre en place un versement automatique depuis votre Cagnote, soit effectuer
des versements ponctuels. Toutes les transactions sont loggées, de sorte de
garder une trace de sa trésorerie.

Pour l'heure, l'application ne fonctionne qu'en ligne de commande. Vous
trouverez les explications tout au long de cette documentation

La Tirelire
-----------
Voyons un peu plus précisement comment fonctionne une Tirelire.

Une Tirelire va représenter tout votre argent et vos champs de dépenses.
Elle est constituées de Comptes et de Cochons et peut prendre en compte des 
Distributions.

Pour créer un compte, tappez l'une des commande suivante ::
    
    ./tirelire-cli --creer maTirelire
    ./tirelire-cli -c maTirelire

Les Comptes
-----------
Les Comptes de votre Tirelire vont représenter vos vrais comptes en banques.
Les comptes sont classés en deux types :
* les comptes "courant"
* les comptes "épargne"

L'argent contenu dans les premiers va allimenter votre Cagnote.
Les seconds pourront être alimentés à partir de l'argent de vos cochons.

Les Comptes sont caractérisés par un nom et un type, pour en ajouter un a votre
Tirelire, tappez une des commandes suivantes ::

    ./tirelire-cli maTirelire --ajoutecompte monCompte sonType
    ./tirelire-cli maTirelire -A monCompte sonType

Les Cochons
-----------
Imaginez des petites tirelires en forme de cochons dans lesquelles vous mettriez
de l'argent en prévision ... du loyer, de telle ou telle facture... Eh bien, les Cochons de votre Tirelire sont là pour ça !

Il existe deux types de Cochons. Certains pensent à mettre de l'argent de côté
pour les coups durs : ce sont les Cochons "Fourmis" ! ils vous serviront à déplacer
de l'argent d'un compte courant vers un compte épargne.

Les autres ne pensent qu'à dépenser : ce sont les Cochons "Cigales" ! Ce sont eux
qui payeront vos dépenses.

Les Cochons sont caractérisés par un nom et un type, pour en ajouter un a votre
Tirelire, tappez une des commandes suivantes ::

    ./tirelire-cli maTirelire --ajoutecochon monCochon sonType
    ./tirelire-cli maTirelire -a monCochon sonType
    ./tirelire-cli maTirelire -a loyer fourmi 
    
Chaque Cochon "Fourmis" place l'argent dans un unique endroit (il serait
dangeureux de risquer d'en perdre), aussi, lors de la création sa création, il
vous sera demandé à quel compte épargne l'associer. Le "virement" s'effectue en
fin de mois.

Déposer de l'argent sur un compte
---------------------------------
Rien de plus simple, il suffit de préciser quel montant vous voulez déposer sur
quel compte et pourquoi (un petit commentaire pour laisser une trace). 

Chacune des commandes suivantes vous permettrons de le faire ::

    ./tirelire-cli maTirelire --deposecompte monCompte monMontant monBlabla
    ./tirelire-cli maTirelire -D monCompte monMontant monBlabla

(Vous aurez noté que les commandes liées aux Comptes sont abrégée par une lettre
majuscule alors que celles liées aux Cochons sont en minuscule ;) )

Cette action vous permet d'indiquer combien vous avez d'argent au moment de la
création de votre Tirelire, mais vous permettra aussi d'ajouter vos revenus
(salaire, remboursements, Père Noël...)

Mettre un peu d'argent dans un Cochon
-------------------------------------
Pour mettre des pièces dans un Cochon, il faut en avoir. Vous allez alimenter
les Cochons avec l'argent des comptes courants.

Pour cela, il faudra préciser depuis quel compte vous prenez l'argent, quel
montant et vers quel Cochon. Ici, nul besoin de mettre un commentaire : il ne
s'agit pas d'une dépense réelle, juste de mettre de l'argent de côté pour
quelque chose de précis, le nom de votre Cochon doit suffire à vous y retrouver.

Chacune des commandes suivantes vous permettrons de le faire ::

    ./tirelire-cli maTirelire --transfert monCompte monCochon monMontant
    ./tirelire-cli maTirelire -t monCompte monCochon monMontant

Enregistrer une dépense
-----------------------
Pour enregistrer dans votre Tirelire une dépense que vous venez d'effectuer, il
vous faut indiquer dans quel Cochon vous avez pris l'argent, quel montant et
pourquoi (toujours pour garder une trace).

Chacune des commandes suivantes vous permettrons de le faire ::

    .tirelire-cli maTirelire --depenseCochon monCochon monMontant monBlabla
    .tirelire-cli maTirelire -d monCochon monMontant monBlabla

L'enregistrement des transactions étant daté, il est conseillé de s'en occuper
le jour même pour simplifier au possible la comptabilité.

Automatiser l'alimentation des Cochons
--------------------------------------
Un certain nombre des dépenses du mois sont prévisibles (loyer, factures...) et
il va être rapidement fastidieux de mettre à la main cet argent de côté tous les
mois. Alors pourquoi ne pas décrire tous ces transferts dans un fichier et le
faire lire à votre Tirelire ? 

Le format de fichier choisi pour ça est le format INI. Voici un exemple de
fichier (appellons le monFichier.ini) qui décrit le transfert de 20 euros depuis
le Compte monCompte vers le Cochon monCochonCigale et 50 euros vers le Cochon
monCochonFourmi qui sera reversé dans le Compte monCompteEpargne ::

    [monCochonCigale]
    montant = 20
    origine = monCompte

    [monCochonFourmi]
    montant = 50
    origine = monCompte
    destination = monCompteEpargne

Chaque Cochon ne peut porter qu'un seul transfert automatique.

Pour intégrer ces transferts automatiques à la tirelire ::

    ./tirelire-cli maTirelire --fichier monFichier.ini
    ./tirelire-cli maTirelire -F monFichier.ini

Si lors de l'intégration du fichier, le Cochon n'existe pas, il est créé (Cochon
Fourmi si une destination est précisée, Cochon Cigale sinon). Si le Cochon
existe déjà mais que le type ne semble pas être bon, le programme s'arrêtera. Il
vous faudra corriger le fichier et le reproposer entièrement à la Tirelire.

Les Comptes, eux, doivent déjà exister.

Visualiser le contenu d'une Tirelire
------------------------------------
Mettre de l'argent de côté, le dépenser... c'est une chose, mais de temps à
autre, vous voudrez vérifier l'état de vos Comptes et Cochons.

Pour cela, utilisez une des commandes suivante ::

    ./tirelire-cli maTirelire --voir
    ./tirelire-cli maTirelire -v
    <sortie>
