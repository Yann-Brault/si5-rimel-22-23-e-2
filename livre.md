# Sujet

Peut-on déterminer la paternité de l’implémentation (et l’évolution) d’une fonctionnalité variable à partir du code 
en appliquant les méthodes de détermination de paternité aux endroits où la variabilité est implémentée ?

##### Option :
Nous nous concentrerons sur les variables d'environnement. 

# Abstract

@TODO : en fin de livre, a compléter

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

#### Challenge 3 - Créer "l'arbre généalogique" de la patternité des variables d'environnements

Notre challenge 2 permettait d'avoir une vision globale de la variabilité. La paternité était associée à un pourcentage.
Cependant, ce pourcentage est globalement utile pour un manager, mais admettons vous êtes développeur et vous tombez
face à une variabilité que vous ne comprennez pas. Là, vous pouvez aller remonter les commits à la main. Mais
un outil permettant de remonter les commits et d'avoir une arborescence serez de grande utilité. Vous pourriez y consulter
les messages associés aux commits, ou même contacter les développeurs originaires de cette variabilité. C'est en sorte
un git blame, mais qui vous permettrait d'avoir la personne qui a le plus contribuer à cette variabilité.






















