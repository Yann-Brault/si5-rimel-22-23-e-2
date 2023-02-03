
## Sujet : Peut-on déterminer la paternité de l’implémentation (et l’évolution) d’une fonctionnalité variable à partir du code en appliquant les méthodes de détermination de paternité aux endroits où la variabilité est implémentée ?

Afin de répondre au mieux à cette question, nous avons fait le choix de décomposer le projet en plusieurs sous-questions :

### 1️⃣ - Peut-on identifier, à gros grain,  la paternité des variables d'environnement dans un code ?
**Objectif :** Trouver le premier créateur d’une variable d’environnement, et ensuite suivre qui l’a édité au fur et à mesure du temps (jusqu’à sa potentielle suppression)

#### 1️⃣ 1️⃣ - Qui a créé pour la première fois la variable d’environnement ?

**Hypothèses :** Quand un utilisateur ajoute une variable d’environnement au projet, il l’ajoute en premier lieu dans un fichier de configuration


**Scope de la sous-question :** Détecter qui est le créateur d’une variable d’environnement en regardant les fichiers docker-compose.yaml et les fichiers .env


#### 1️⃣ 2️⃣ - Qui a utilisé cette variable d’environnement dans le code ?

**Hypothèses :** Quand un utilisateur ajoute une variable d’environnement au projet, il l’ajoute en premier lieu dans un fichier de configuration ET il l’implémente quelque part dans le code

**Scope de la sous-question :**
* Quand une variable d’environnement est ajouté dans les fichiers docker-compose.yaml et les fichiers .env, dans le même commit, regarder ou cette variable d’environnement a été ajouté dans le code
* Suivre et remonter les éditeurs de cette variable d’environnement à travers les commits.



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

# Limite de la solution actuelle

Pour l'instant, nous avons posé l'hypothèse que les variables d'environnement introduites sont utilisées avec leur nom d'origine. 
Cette hypothèse peut entraîner une perte d'information en cas de renommage de cette variable lors de sa récupération/utilisation. Effectivement, nous avons observé que dans certains projets, les variables déclarées dans un docker-compose.yml peuvent être renommées lorsqu'elles sont récupérées dans l'application dockerisée. 
Ce phénomène entraîne une perte de tracabilité sur l'utilisation de cette variable.
Dans le cadre de notre MVP, nous ne nous occuperons pas de ce cas particulier, cependant, il sera intéréssant par le futur de trouver un moyen de continuer de tracer cette variable malgrès son renommage.

