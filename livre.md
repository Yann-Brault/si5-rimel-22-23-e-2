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
il ne repart pas de 0, il va réutiliser une base qu'il a déjà fait auparavant, pour économiser de l'argent notamment, car
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

