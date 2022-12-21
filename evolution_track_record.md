

# Recherche de variable d'environnements dans les fichiers d'un projet
###### 21 décembre 2022 - D'Andréa William

```python
WORKING_REPOSITORY: str = "./test_repositories/sagan-master"


def flatten(A):
    rt = []
    for i in A:
        if isinstance(i, list):
            rt.extend(flatten(i))
        else:
            rt.append(i)
    return rt


def extract_environment_variable(word: str) -> str:
    """
    >>> extract_environment_variable("Bonjour")
    >>> ''
    >>> extract_environment_variable("${MY_VARIABLE_ENV}aaa")
    >>> 'MY_VARIABLE_ENV'
    :param word: the word you want to check
    :return: '' if the word is not an envionment variable, else the filtered environment variable
    """

    temp_word: str = word

    # Remove the prefix in the word
    for letter in temp_word:
        if letter.isupper():
            break
        word = word[1:]

    temp_word = word
    # Remove the suffix in the word
    for letter in temp_word[::-1]:
        if letter.isupper():
            break
        word = word[:-1]

    filtered_regex = flatten(re.findall(r"(^[A-Z0-9_]+)", word))
    if len(filtered_regex) == 0 or len(filtered_regex[0]) == 1:
        return ''

    if len(filtered_regex[0]) == len(word):
        return word


    return ''


def recover_environment_variable_in_a_file(url_file: str) -> List[str]:
    result = []
    with open(url_file) as file:
        for line_number, line in enumerate(file, 1):
            words_in_line = line.split()

            for word in words_in_line:
                env_variable = extract_environment_variable(word)
                if env_variable != '':
                    result.append({"line_number": line_number, "env_variable": env_variable, "line_content": line})

    return result


types = ('yml', 'java', 'js') # the tuple of file types
files = []
for file_type in types:
    files.extend(glob.glob(f'{WORKING_REPOSITORY}/**/*.{file_type}', recursive=True))

files = [f for f in files if os.path.isfile(f)]

result = {}
for file_url in files:
    result[file_url] = recover_environment_variable_in_a_file(file_url)
```

Afin de suivre au mieux la patternité de l'utilisation des variables d'envrionnements dans le code
il est nécessaire de les détecter dans un fichier. C'est ce a quoi répond cette implémentation. 

A partir d'un projet composé de fichiers situé à l'emplacement `WORKING_REPOSITORY`, nous allons
parcourir tous les fichiers ayant comme extenssion `types = ('yml', 'java', 'js')`.

Ensuite, nous allons parser chaques lignes, puis chaques mots. Le but est de découvrir des variables
d'environnements. Nous supponsons qu'une variable d'environnement est un mot composé uniquement de
lettre majuscules, sans caractères speciaux ni de nombre.

En sortie de cet alorithme, nous avons un résultat de ce type : 
```
[
    ./projects/ReleaseTests.java': [
        {'line_number': 6, 'env_variable': 'ROOT', 'line_content': '    ROOT: INFO\n'},
        {'line_number': 6, 'env_variable': 'INFO', 'line_content': '    ROOT: INFO\n'},
        {'line_number': 7, 'env_variable': 'WARN', 'line_content': '    org.apache.http: WARN\n'},
        {'line_number': 9, 'env_variable': 'INFO', 'line_content': '    sagan.renderer: INFO\n'},
        {'line_number': 18, 'env_variable': 'API', 'line_content': '      # API, even for operations that do not require authorization (e.g. Getting Started\n'},
        {'line_number': 23, 'env_variable': 'GITHUB_ACCESS_TOKEN', 'line_content': '      token: ${GITHUB_ACCESS_TOKEN:}'}
  ],
    ./projects/MainTests.java': [
        {'line_number': 7, 'env_variable': 'WARN', 'line_content': '    org.apache.http: WARN\n'},
    ],
]
       
```

Nous pouvons retrouver pour chaques fichier les variables d'environnement pottentielles, avec le numéro
de la ligne, ainsi que le contenu de la ligne. 

Nous voyons ici la première limite de cette implémentation, en effet, dans cette ligne ci `{'line_number': 6, 'env_variable': 'ROOT', 'line_content': '    ROOT: INFO\n'}`
il est très peu probable que `ROOT` soit une variable d'environnement. 

Pour faire un rapide rappel, l'objectif de cet algorithme est de trouver les variables d'environnements
dans tous les fichiers, il faudrai cependant avoir une vérification que nos variables qui sortent de cet
algorithme soient vraiment des variables d'environnements. Pour cela, plusieurs solutions sont possibles
- avoir une confirmation de l'auteur que ces variables d'environnements ont bien été créé
- avoir une liste de nom "classiques" de variables d'environnement et regarder si la variable d'environnement trouvé par notre algorithme est dans cette liste.


