import json

from git import Repo
from git import Actor
import git
import re

repository = Repo.init('../selene-22-23-soa-selene-22-23-c')

# print(repository.git.log("--patch", "8d9fd97773fa90a568024151126abe1399a48c7d"))
# print(repository.git.show("8d9fd97773fa90a568024151126abe1399a48c7d"))

# repository.git.log()

commits = dict()

# commits = {
#       commit_id: {
#           author: string
#           date: string
#           addition: [{ENV_VARIABLE: value},]
#           deletion: [{ENV_VARIABLE: value},]
#       }
#
#
# }

# git show ed5927e45d0a5cb60251b84e7a1faa5ed1a328b5
# Names of all the commits that modify environnment variables
names = []
for commit in repository.iter_commits():
    commit_name = commit.__str__()

    for commit_file in commit.stats.files.keys():

        if '.env' in commit_file or 'docker-compose' in commit_file:

            try:
                result = repository.git.log(
                    "--patch", f"{commit}", commit_file)
            except:
                # print("Cannot read the commit file ", commit_file, " in the commit ", commit_name)
                print("File ", commit_file,
                      " was deleted in the commit ", commit_name)
                continue
            names.append(commit_name)
            for line in result.splitlines():
                if len(line) > 0:
                    if line[0] == '+' or line[0] == '-':

                        commits[commit_name] = {}
                        commits[commit_name]['author'] = commit.author
                        commits[commit_name]['date'] = commit.committed_date
                        commits[commit_name]['addition'] = []
                        commits[commit_name]['deletion'] = []

                        all_env_variables_in_the_line = re.findall(
                            "(^[A-Z0-9_]+)(\=)(.*\n(?=[A-Z])|.*$)", line[1:])
                        for reg in all_env_variables_in_the_line:
                            # ('APP_PORT', '=', '3000')
                            (name, eq, value) = reg
                            if line[0] == '+':
                                commits[commit_name]['addition'].append(
                                    {name: {'file': commit_file, 'value': value}})
                            if line[0] == '-':
                                commits[commit_name]['deletion'].append(
                                    {name: {'file': commit_file, 'value': value}})

#print(commits)

# Get Paternity users
paternals = {}
for name in names:
    #We get the attributes names coz 1 user can use different email address but the same Username
    author = commits[name]['author'].name
    if author in paternals.keys():
        paternals[author] = paternals[author] + 1
    else:
        paternals[author] = 1

sorted_paternals = {k: v for k, v in sorted(paternals.items(), key=lambda item: item[1], reverse=True)}
print(sorted_paternals)
# # Writing to sample.json
# with open("commits.json", "w") as outfile:
#     outfile.write(json_object)
#
#
#     var_utils = dict()
#     if commit_name in commits.keys():
#         for commit_file in commit.stats.files.keys():
#             try:
#                 result = repository.git.show(commit_name)
#             except:
#                 print(
#                     f"file {commit_file} was deleted in the commit {commit_name}")
#                 continue
#             var_utils[commit_name] = {"file": commit_file, "result": result}
#             print(
#                 f"commit_name : {commit_name}, file : {commit_file}, result : {result}")
# print(var_utils)
# # json_object = json.dumps(var_utils)
# #
# # # Writing to sample.json
# # with open("var_utils.json", "w") as outfile:
# #     outfile.write(json_object)