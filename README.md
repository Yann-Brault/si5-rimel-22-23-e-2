
# si5-rimel-22-23-e

## Sujet de recheche :

```
Peut-on déterminer la paternité de l’implémentation (et l’évolution) d’une fonctionnalité variable à partir du code en appliquant les méthodes de détermination de paternité aux endroits où la variabilité est implémentée ?
```

et en particulier :

```
Se concentrer sur la chaîne complète (depuis des outils de construction qui exploitent les variables d’environnement jusqu’au code)
```

Suite à une première analyse du sujet, on se propose de poser la question suivante:

> Peut-on trouver, à gros grain, la paternité et la date d'introduction de tout ou partie des variables d'environnement ?

A la suite du développement d'un premier outil nous permettant de répondre à cette question et fonction des résultats nous nous proposons d'explorer toutes les questions suivantes:

- Quand ont été modifiée les variables ?
- Est-ce que la paternité change ? Est-ce qu'une variable est toujours modifiée par la même personne ?
- Est-ce que c'est toujours la même personne qui modifie les variables d'un package ?

- Une fois qu'on aura eu nos premiers résultats, est-ce qu'on se concentre sur les outils ou sur le code ? Est-ce qu'on reste sur une analyse à gros grains "tout terrain" ?

- En fonction de la propreté des commits, est-ce que c'est la même personne qui introduit pour la prmeière fois une variable et qui introduit aussi sa première utilisation.

## Support de travail :

Nous allons développer un premier MVP en python qui aura pour but de retourner tous les commits qui concernent l'introduction ou la modification d'une variable d'environnement, le commiteur et la date.


# Evolution du projet

### 1. Recherche de l'auteur et la date du moment ou une variable d'environnement est ajouté dans un code
###### Semaine 48 -> 49

Le but de cette première version est de créer un script qui a pour objectif de trouver à quel commit (et donc d'avoir
les détails de ce commit - date / auteur) a été ajouter une variable d'environnement dans un projet.

Pour cela, nous faisons la supposition qu'une variable d'environnement ne peux être ajouté dans un projet que de deux manières :
* dans un fichier `.env`
* dans un fichier `docker-compose.yml`

Afin de réaliser cette tâche, nous avons développé un script python qui va parcourir les commits d'un projet, ensuite parcourir les fichiers modifiés durant ce commit, ensuite regarder (via une expression régulière)
si des variables d'environnements sont incluse dedans. Il va ensuite regarder si la variable d'environnement a été ajouté ou supprimé, et générer un dictionnaire qui respecte le modèle de donnée ci-dessous :

```python
{    
    '3b223df56c04cf25925571eef32095eac9b2f983': {
        'author': "William D'Andrea - williapile@gmail.com", 
        'date': 1663790890, 
        'addition': [
            {   
                'APP_PORT': {
                    'file': 'module-life-service/.env', 
                    'value': '4003'
                }
            },
        ],
        'deletion': [
            {
                'APP_PORT': {
                    'file': 'module-life-service/.env',
                    'value': '4003'
                }
            },
        ],
    }
}
 ```

En analysant des projets complexes, nous pouvons nous apercevoir que notre alternative soulève déjà quelque problèmes.

Dans les fichiers docker-compose, nous nous apercevons que, pour un projet micro-service, il y a souvent des variables
d'environnement qui ont le même nom, mais qui sont défini dans plusieurs services, notre script ne permet pas de déterminer
à quel micro-service cette variable d'environnement appartient. La paternité peut donc être difficile à être remonté.

Quand un fichier est supprimé, notre script ne détecte pas quelles variables d'environnement ont été supprimé.

Notre script génère pour l'instant qu'un dictionnaire contenant toutes les informations importantes relatives à notre projet, 
il serait utile de créer un autre script qui va analyser ce dictionnaire afin de remonter l'arborescence de création / suppression
de variable d'environnement dans le fichier `.env` ou `docker-compose.yml`


