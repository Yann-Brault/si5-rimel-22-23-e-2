import glob
import os
import re
from typing import List

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

    # word = "${MY_VARIABLE_ENV}"
    word_without_special_characters = [''.join(e for e in r if e.isalnum() or e == '_') for r in word]
    # word_without_special_characters = ['', '', 'M', 'Y', '_', 'V', 'A', 'R', 'I', 'A', 'B', 'L', 'E', '_', 'E', 'N', 'V', '']
    only_majs = flatten([re.findall(r"(^[A-Z0-9_]+)", x) for x in word_without_special_characters])
    # only_majs = ['M', 'Y', '_', 'V', 'A', 'R', 'I', 'A', 'B', 'L', 'E', '_', 'E', 'N', 'V']
    word_filtered = ''.join([x for x in only_majs])
    # word_filtered = MY_VARIABLE_ENV

    if word_filtered != '' and len(word_filtered) > 1 and not word_filtered.isnumeric():
        return word_filtered
    else:
        return ''


def recover_environment_variable_in_a_file(url_file: str) -> List[str]:
    result = []
    with open(url_file) as file:
        for line in file:
            # print('zzzzzz ', item)
            # print(item)
            # matches = re.findall("(^[A-Z0-9_]+)", item)
            words_in_line = line.split()

            for word in words_in_line:
                env_variable = extract_environment_variable(word)
                if env_variable != '':
                    result.append(env_variable)

    return result


files = glob.glob(f'{WORKING_REPOSITORY}/**/*.yml', recursive=True)
files = [f for f in files if os.path.isfile(f)]

result = {}
for file_url in files:
    result[file_url] = recover_environment_variable_in_a_file(file_url)

print(result)
