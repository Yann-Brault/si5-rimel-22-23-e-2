# si5-rimel-22-23-e-

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

A la suite du développement d'un premier outils nous permettant de répondre à cette question et fonction des résultats nous nous proposons d'explorer toutes les questions suivantes:

- Quand ont été modifiée les variables ?
- Est-ce que la paternité change ? Est-ce qu'une variable est toujours modifiée par la même personne ?
- Est-ce que c'est toujours la même personne qui modifie les variables d'un package ?

- Une fois qu'on aura eu nos premiers résultats, est-ce qu'on se concentre sur les outils ou sur le code ? Est-ce qu'on reste sur une analyse à gros grains "tout terrain" ?

- En fonction de la propreté des commits, est-ce que c'est la même personne qui introduit pour la prmeière fois une variable et qui introduit aussi sa première utilisation.

## Support de travail:

Nous allons développer un premire MVP en python qui aura pour but de retourner tous les commits qui concernent l'introduction ou la modification d'une variable d'environnement, le commiteur et la date.
