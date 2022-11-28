from git import Repo
import git
import re

repository = Repo.init('./')

# print(repository.git.log("--patch", "8d9fd97773fa90a568024151126abe1399a48c7d"))
# print(repository.git.show("8d9fd97773fa90a568024151126abe1399a48c7d"))

# repository.git.log()

for commit in repository.iter_commits():
    # print(commit, commit.author, commit.committed_date)

    for commit_file in commit.stats.files.keys():

        if ('.env' in commit_file or 'docker-compose' in commit_file):
            # print(commit_file)
            result = repository.git.log("--patch", f"{commit}", commit_file)

            for line in result.splitlines():
                if (len(line) > 0):
                    if (line[0] == '+' or line[0] == '-'):
                        regexxx = re.findall("(^[A-Z0-9_]+)(\=)(.*\n(?=[A-Z])|.*$)", line[1:])
                        print(regexxx)




            # regexxx = re.findall("(^[A-Z0-9_]+)(\=)(.*\n(?=[A-Z])|.*$)", result)
            # print(regexxx)


    break


    # files = repository.git.show(f"{commit} --patch")
    # print(files)

    # for t in commit.list_items():
    #     print(t)
    # print(commit.stats.files)
    # print("==============================")

# repository.logs
