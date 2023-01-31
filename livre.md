# Sujet

Peut-on déterminer la paternité de l’implémentation (et l’évolution) d’une fonctionnalité variable à partir du code 
en appliquant les méthodes de détermination de paternité aux endroits où la variabilité est implémentée ?

##### Option :
Nous nous concentrerons sur les variables d'environnement.

# Introduction - contexte et motivations

Dans de nombreux projets de grande envergure, nous retrouvons de la variabilité. Afin d'illustrer au mieux ce qu'est
la variabilité, nous allons prendre un exemple concret. JetBrains est l'entreprise qui a créée la suite d'IDE Intellij,
WebStorm, Clion ... Ils ont une suite logicielle très vaste, et très développé. Si vous avez déjà utilisé plus de 2 
de ces IDE, vous aurez surement remarqué que l'affichage, la forme du logiciel, les paramètres, se ressemblent énormément,
voir sont les mêmes dans la majorité des cas. 

Ces différents IDE utilisent de la variabilité pour fonctionner. C'est-à-dire ? Quand JetBrains veut créer un nouvel IDE, 
il ne repart pas de 0, il va réutiliser une base qu'il a déjà faite auparavant, pour économiser de l'argent notamment, car
pourquoi réinventer la roue alors que l'on a quelque chose qui fonctionne déjà très bien, et qui est testé à grande échelle ?

Donc quand JetBrains va créer un nouvel IDE, qui s'appelle par exemple JetRimel, il va prendre la base de Intellij, et va
y insérer de la variabilité. Voici un exemple :

`.env`
```.dotenv
MY_CURRENT_IDE="JetRimel"
```

`myClass.js`
```javascript
if (process.env.MY_CURRENT_IDE === "JetRimel") {
    // Show the header in black
}
if (process.env.MY_CURRENT_IDE === "IntelliJ") {
    // Show the header in white and add the Git Extenssion
}
if (process.env.MY_CURRENT_IDE === "DataSpell") {
    // When right click, allow only to create Jupyter Notebook files
}
```

Ceci est un exemple très simplifié, mais relativement parlant. JetBrains va, dans son fichier `.env` insérer des variables
d'environnement, notamment une, nommé `MY_CURRENT_IDE` qui donne le type d'IDE sur lequel il fonctionne, et au moment du
runtime, le logiciel va savoir quoi faire. En faisant ceci, nous avons inséré de la variabilité au logiciel. 

Maintenant que nous savons ce qu'est la variabilité, revenons en à la paternité. Si nous pourrions comparer la paternité
en informatique à quelque chose de la vraie vie, nous pourrions dire que la paternité, c'est un arbre généalogique.
En bas de cet arbre, nous avons les enfants, ici, l'enfant serait le code `if (process.env.MY_CURRENT_IDE === "JetRimel") {}`,
et les parents de cet enfant, serait les personnes qui ont écrit / éditer / supprimer cette ligne de code.

Mais pourquoi la paternité nous intéresse ? Il est légitime de se poser cette question. En effet, du point de vue de 
notre exemple précédent, ce n'est pas très utile, cependant, dans un gros projet, si nous détectons qu'une minorité
de développeurs sont à l'origine de cette variabilité, selon le contexte, nous pourrions supposer qu'il y a un problème 
dans ce projet. Mais un exemple plus parlant, imaginez-vous arriver dans un nouveau projet, similaire à JetBrains, et que
vous êtes confronté à de la variabilité, mais que vous n'avez aucune idée de pourquoi cette variabilité est présente et
à quoi elle sert. Là, vous aimeriez un outil qui vous permet de remonter la paternité de cette variabilité (donc de remonter
à travers les commits ou cette variabilité a été édité), afin de, soit lire le message du commit dans le but de se faire une idée
du pourquoi, ou même de potentiellement contacter le développeur qui a intégré quelque chose que vous ne comprenez pas.

En plus d'avoir un aspect pratique, cet outil permettrait aussi de faire des statistiques intéressantes, afin de savoir
qui est majoritairement a l'origine de la variabilité, qui créé le plus de variabilité, pour permettre, potentiellement,
a du management d'avoir un métrique globale et une vue d'ensemble sur le projet en cours. 

Cette introduction peut, potentiellement paraître barbante pour des personnes initiés à la variabilité, mais, dans mon cas,
avant ce projet, je n'étais pas sensibilisé à ce qu'étais vraiment la variabilité et la paternité. Et donc, en faire
une explication volontairement simpliste et une bonne manière de comprendre sur quoi nous allons travailler. Car, comme
dirait M. Mortara, si vous ne comprenez pas ce que vous faites, en l'expliquant avec des mots simples, vous aurez du mal à avancer. 


# Questions auxquelles nous allons tenter d'apporter des solutions.

Maintenant que nous avons notre "pourquoi", nous devons nous concentrer sur le "quoi". Il est important de décomposer 
le travail, et d'aller répondre à un problème bien particulier car la variabilité et la paternité sont des domaines très vaste.

### Sur quoi travaillons-nous ?

Voici notre **sujet initial** : 

> Peut-on déterminer la paternité de l’implémentation (et l’évolution) d’une fonctionnalité variable à partir du code
en appliquant les méthodes de détermination de paternité aux endroits où la variabilité est implémentée ?

***

En analysant la question, nous pouvons la résumée à ceci : 
> En détectant ou la variabilité est implémentée, comment déterminer la paternité de celle-ci ? 

Ce petit résumé correspond à notre introduction, et aux potentiels use-cases associées. Notre but est donc de :
>1) Détecter la variabilité
>2) Analyser la paternité de cette variabilité

***

Il y a plusieurs façons de détecter de la variabilité, nous pouvons la trouver grâce aux `#ifdef`, grâce a du code 
orienté object, mais aussi grâce à des variables d'environnements. C'est ce dernier point qui nous intéresse. Nous
pouvons donc compléter notre but : 
>1) Détecter la variabilité grâce aux variables d'environnements
>2) Analyser la paternité de cette variabilité

***

### Comment allons-nous procéder ?

Nous sommes fâce à un problème relativement générique, afin de réaliser au mieux notre étude, il est necéssaire de 
décomposer ces questions générales en sous-questions, pour avoir un plan d'action. Un plan d'action est voué à évoluer
au fil du projet, car, comme toute étude, il y a une part d'empirique dedans. Dans le but de ne pas vous perdre, nous y avons
recensé toutes les étapes par lesquelles nous sommes passés. 

Nous allons reformuler une nouvelle fois notre problème, mais cette fois-ci c'est la question que nous allons essayer de répondre

> Peut-on identifier, à gros grain, la paternité des variables d'environnement dans un code ?

Cette question implique 2 sous-questions : 

> 1. Qui a créé pour la première fois la variable d’environnement ?
> 2. Qui a édité cette variable d’environnement dans le code ?
> 3. Comment mesurer la paternité d'une variabilité à l'instant T et au fil du temps ?


À la base du projet, nous voulions aller encore plus loin que ces 2 sous-questions, comme connaître les
impacts liés à l'utilisation / modifications des variables d'environnement, cependant, après discussion avec plusieurs intervenants,
nous nous sommes rendus-compte que cette ambition était bien trop grande, et qu'il valait mieux se cantonner aux 2 sous-questions
énoncées précédemment, et pousser l'analyse plus loin. 

### Challenges associés à cette étude

#### Challenge 1 - Détecter les variables d'environnements
A première vu, il peut sembler simple de trouver des variables d'environnements dans un projet, cependant, ce n'est pas
si simple que ça. EN effet, chaque langage a se manière de fonctionner. Les variables d'environnements sont souvent
injectés dans un code, par différents mécanismes relatifs aux langages de programmation et framework. 

Nous détaillerons plus tard la démarche, mais il est clair que ce problème est la particularité sensible de ce projet,
qui nous a demandé beaucoup de temps et beaucoup de reflection. De plus, c'est un point central de notre projet, si nous
n'arrivons pas à détecter les variables d'environnements correctement, comment faire une analyse de celles-ci ? 

#### Challenge 2 - Mesurer le pourcentage de variabilité associé à chaques développeurs d'un projet

Une fois que nous aurons détecté les variables d'environnements dans le code, nous devrons déterminer la paternité de 
celles-ci aux différents endroits où la variabilité associé a été implémenté. Pour cela, nous ferons une première passe
relativement simpliste, c'est-à-dire d'associer à chaque développeur du projet, un pourcentage de variabilité associé.

Un exemple sera plus simple. Admettons que nous avons un projet qui contient 3 implémentations de variabilité, par exemple :

`myClass.js`
```javascript
1 if (process.env.MY_CURRENT_IDE === "JetRimel") {
2     // Show the header in black
3 }
4 if (process.env.MY_CURRENT_IDE === "IntelliJ") {
5     // Show the header in white and add the Git Extenssion
6 }
7 if (process.env.MY_CURRENT_IDE === "DataSpell") {
8     // When right click, allow only to create Jupyter Notebook files
9 }
```

Admettons que la ligne 1 a été écrite par George, et que la ligne 4 et 7 par Moris. Dans ce cas-là, Moris aura un pourcentage
de responsabilité de variabilité de 66% tandis que George aura un score de 33%. 

Mais à quoi cette statistique peut bien t-elle servir ? Malgré le fait qu'elle soit très abstraite, elle permet à des chefs
de projet de savoir qui est responsable en majorité de la variabilité, et de potentiellement prendre des dispositions par rapport
à cela. Les développeurs, malgré le fait qu'ils soient assis derrière un écran, veulent aussi prendre leur retraite un jour.
De ce fait, imaginez que vous êtes chef de projet chez JetBrains, et que vous vous rendez compte que sur tous les développeurs
de votre équipe, il y en a un, qui est à 2 ans de la retraite (nous ne donnerons pas d'age, car l'age de départ peut-être, ...,
fluctuant ...) et qui a 80% de responsabilité de variabilité. C'est problématique, parce qu'une fois parti, 
il ne pourra plus vous aider. Donc là en tant que chef de projet, vous pouvez prendre les reines et lui faire faire des
interviews pour préparer la suite, ou même essayer de splitter cette responsabilité sur des nouveaux développeurs. 

Nous pouvons ensuite aller faire cette mesure pour chaque commit, et donc avoir une vue globale du pourcentage de responsabilité
de variabilité au fil du temps. 

#### Challenge 3 - Créer "l'arbre généalogique" de la paternité des variables d'environnements

Notre challenge 2 permettait d'avoir une vision globale de la variabilité. La paternité était associée à un pourcentage.
Cependant, ce pourcentage est globalement utile pour un manager, mais admettons vous êtes développeur et vous tombez
face à une variabilité que vous ne comprennez pas. Là, vous pouvez aller remonter les commits à la main. Mais
un outil permettant de remonter les commits et d'avoir une arborescence serez de grande utilité. Vous pourriez y consulter
les messages associés aux commits, ou même contacter les développeurs originaires de cette variabilité. C'est en sorte
un git blame, mais qui vous permettrait d'avoir la personne qui a le plus contribuer à cette variabilité.




# Partie 1 - Détecter les variables d'environnements

Cette section aura pour ligne de conduite la détection de variables d'environnements dans un projet. C'est une partie
relativement complexe car l'utilisation des variables d'environnement dans un code est très dépendant de son langage de
programmation. Alors oui, cela peut-être un réel avantage si l'on souhaite trouver les variables d'environnements 
dans un projet, mais si l'on cherche à analyser une variété de projets dans des langages particuliers, cela est 
compliqué.

La première étape est de faire un état de l'art de ce qu'il existe déjà. Nous avons procédé à 2 méthodes, la première
recherche est via Google Scholar ensuite faire des recherches plus générales sur le web. 

Nous avons trouvé un article intéressant nommé "A framework for creating custom rules for static analysis tools" [^1].
Cet article est intéressant et décrit comment créer des règles personnalisées pour faire de l'analyse statique de code via
l'outil `Fortify Software Source Code Analyzer`. Un outil comme celui-ci serait parfait pour nous, car on pourrait lui donner
des règles, et il irai faire l'analyse statique du code. Cependant, ce logiciel est sous license, nous ne pouvons donc
pas l'utiliser, de plus, nous n'avons pas trouvé sa version en open-source. 

Un outil réalisant une analyse de code statique est SonarQube, nous pouvons également lui donner des règles personnalisées,
cependant nous n'avons pas trop bien compris comment cela fonctionne. Nous avons donc fait le choix de créer notre propre
outil, sous Python, qui irait explorer les fichiers et trouverait directement les variables d'environnements. 

***


### Hypothèse 1

Avant de continuer, revenons à notre problème. Nous cherchons à trouver des variables d'environnements dans un code. Notre
première idée fut d'utiliser des projets qui sont dockerisées via un docker-compose. En effet, dans les docker-compose,
en général nous trouvons les variables d'environnement qui seront injectés. Par-dessus cette hypothèse, nous avons supposé
que la première introduction d'une variable d'environnement dans un projet au niveau du code se faisait dans le même 
commit que celui ou nous avons placé notre variable d'environnement dans le docker-compose. 


Afin de tester cette hypothèse, nous avons réaliser un programme python qui va itérer parmi les fichiers docker-compose
d'un projet, et en extraire, pour chaque variable d'environnement, les développeurs qui ont mis cette variable d'environnement
une première fois dans le code, et les développeurs qui ont supprimé une variable d'environnement. Nous sommes
donc parti à la recherche de projets open-source, dockerisé et gérer via docker-compose. Cela fut relativement
dur, mais nous avons trouvé un projet intéressant nommé `Rocket.Chat` disponible [ici](https://github.com/RocketChat/Rocket.Chat/tree/alpine-base)
qui est un outil de messagerie et de collaboration open-source pour les équipes. 

Il contient à ce jour 22k commits, et le fichier docker-compose ressemble à ceci : 
```yaml
services:
  rocketchat:
    image: rocketchat/rocket.chat:latest
    restart: unless-stopped
    volumes:
      - ./uploads:/app/uploads
    environment:
      - PORT=3000
      - ROOT_URL=http://localhost:3000
      - MONGO_URL=mongodb://mongo:27017/rocketchat
      - MONGO_OPLOG_URL=mongodb://mongo:27017/local
      - MAIL_URL=smtp://smtp.email
#       - HTTP_PROXY=http://proxy.domain.com
#       - HTTPS_PROXY=http://proxy.domain.com
    depends_on:
      - mongo
    ports:
      - 3000:3000
    labels:
      - "traefik.backend=rocketchat"
      - "traefik.frontend.rule=Host: your.domain.tld"
```

Au niveau des variables d'environnement, la norme est que les variables d'environnements soient nommé
par des mots en majuscules, séparé par des underscores. Nous retrouvons cette syntaxe dans ce fichier docker-compose. 

Nous allons donc, via une fonction regex qui doit reconnaitre ces variables d'environnements, remontrer
les commits, afin de voir au fil du temps qui à ajouter / supprimer une de ces variables d'environnement. La fonction
REGEX que nous utilisons dans le fichier docker-compose est celle-ci : `^\s*-\s(\w+)=(.*)$`

En analysant le projet `Rocket.Chat` sous la branche `alpine-base` (15k commits), nous arrivons à trouver une patternité
très large. Nous avons analysé ce projet grâce à l'algorithme `hypothese_1.py`, et nous avons regardé qui a le plus modifié
des variables d'environnement dans le fichier `docker-compose.yml` (nous avons regardé les additions et les deletions). 
Globalement, notre résultat montre que le développeur `Gabriel Engel` a fait le plus de modifications de variables d'environnement dans le fichier docker-compose, il a donc une 
forte paternité au niveau de l'ajout ou retrait de variabilité dans le code (à la source)

```json
{
  "Gabriel Engel": {
    "addition": 406,
    "deletion": 213
  },
  "Guilherme Gazzo": {
    "addition": 272,
    "deletion": 184
  },
  "pkgodara": {
    "addition": 34,
    "deletion": 23
  },
  "Pradeep Kumar": {
    "addition": 68,
    "deletion": 46
  },
  "D\u00e1vid Balatoni": {
    "addition": 34,
    "deletion": 23
  },
  "Rodrigo Nascimento": {
    "addition": 268,
    "deletion": 150
  },
  "Peter Lee": {
    "addition": 34,
    "deletion": 23
  }, ...
}
```

Cette première implémentation, relativement grossière, nous a permis de réorienter notre étude, mais globalement,
donne déjà une vision très large de la paternité de l'ajout / retrait de variable d'environnement dans un projet dockerisé. 


#### Analyse et limites

Nous avons fait le choix d'invalider cette hypothèse à ce stade du projet,car nous nous sommes rendu compte de
plusieurs choses :

* La première étant que le nombre de fichiers open-source dockerisé est en réalité très faible. 
* De plus, nous nous sommes basés sur l'idée qu'une variable d'environnement est injecté via le fichier docker-compose, mais nous
nous sommes aperçus grâce à plusieurs projets qu'en réalité, les fichiers docker-compose ne contiennent qu'une petite
partie des variables d'environnements, surtout sur des projets Java Spring, ou celles-ci sont pour la majorité écrite
dans les fichiers ".properties". 
* De plus, dans nos hypothèses, nous partions sur la supposition que le moment où un développeur ajoute une variable 
d'environnement à un fichier docker-compose, il utilise cette variable d'environnement quelque part dans 
le code. Sauf que cette idée ne peut pas être poursuivie pour 2 raisons. 
  * La première étant qu'en général, notamment sur les gros projets, nous ne l'ajoutons pas au code au moment du même commit
  * La seconde raison est que nous supposons que la variable d'environnement est injecté dans le code sous la même syntaxe, c'est-à-dire sous la forme
  majuscule et underscore. Cependant, nous avons vu que ce n'étais pas toujours le cas, nottament dans les projets
  java spring ou la variable d'environnement peut être appelée dans le code sous la forme `ma.variable.environement` plutôt
  que `MA_VARIABLE_ENVIRONNEMENT`






# Références
[^1]: A framework for creating custom rules for static analysis tools, Eric Dalci John Steven, https://www.academia.edu/download/30668250/SP500_262.pdf#page=49














