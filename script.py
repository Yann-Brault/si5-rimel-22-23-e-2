import subprocess
from git import Repo
import re
import glob
import os
from typing import List

repository = Repo.init('./')

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

names = []

for commit in repository.iter_commits():
    commit_name = commit.__str__()

    for commit_file in commit.stats.files.keys():

        if '.properties' in commit_file:

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

# print(commits)

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


# types = ('yml', 'java') # the tuple of file types
# files = []
# for file_type in types:
#     files.extend(glob.glob(f'{WORKING_REPOSITORY}/**/*.{file_type}', recursive=True))

# files = [f for f in files if os.path.isfile(f)]

# result = {}
# for file_url in files:
#     env_var = recover_environment_variable_in_a_file(file_url)
#     if len(env_var) > 0:
#         print("file", file_url, ":\n")

#         for line in env_var:
#             print("\t", line)
#             line = str(line["line_number"])

#             git_blame = subprocess.check_output(["git", "blame", file_url, "-L", line + "," + line, "--incremental"]).decode("utf-8").split("\n")
#             print("\t\t", git_blame[1])
#             print("\t\t", git_blame[2], "\n")
#         print("\n")



#print(result)
