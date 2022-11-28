from git import Repo
import git
import re

repository = Repo.init('./')

# print(repository.git.log("--patch", "8d9fd97773fa90a568024151126abe1399a48c7d"))
# print(repository.git.show("8d9fd97773fa90a568024151126abe1399a48c7d"))
# git show ed5927e45d0a5cb60251b84e7a1faa5ed1a328b5

commits = {}

for commit in repository.iter_commits():
    # print(commit, commit.author, commit.committed_date)
    commit_name = commit.__str__()
    commits[commit_name] = {}
    commits[commit_name]['author'] = commit.author
    commits[commit_name]['date'] = commit.committed_date
    commits[commit_name]['addition'] = []
    commits[commit_name]['deletion'] = []

    for commit_file in commit.stats.files.keys():

        if '.env' in commit_file or 'docker-compose' in commit_file:
            # print(commit_file)

            try:
                result = repository.git.log("--patch", f"{commit}", commit_file)
            except:
                # print("Cannot read the commit file ", commit_file, " in the commit ", commit_name)
                print("File ", commit_file, " was deleted in the commit ", commit_name)
                continue

            for line in result.splitlines():
                if len(line) > 0:
                    if line[0] == '+' or line[0] == '-':
                        all_env_variables_in_the_line = re.findall("(^[A-Z0-9_]+)(\=)(.*\n(?=[A-Z])|.*$)", line[1:])
                        for reg in all_env_variables_in_the_line:
                            (name, eq, value) = reg
                            if line[0] == '+':
                                commits[commit_name]['addition'].append({name: {'file': commit_file, 'value': value}})
                            if line[0] == '-':
                                commits[commit_name]['deletion'].append({name: {'file': commit_file, 'value': value}})

print(commits)
