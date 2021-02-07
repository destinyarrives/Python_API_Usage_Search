import git, sys
from pathlib import Path
from datetime import datetime
import pandas as pd

"""
Simple script to help you clone a list of repos- for our purposes this would generally be the output from the RepoReapers project, or projects that
have been "engineered". It'll also save the current commit hash to recover a snapshot of the project status later on.
"""

def generate_list_of_urls_from_csv(csv_file, mode = 2):
    """
    input: output file from main.py
    output: dict of urls that can be fed into download_raw_file function 
            eg - "Project-MONAI/MONAI":"https://github.com/Project-MONAI/MONAI"
    """
    #results_file = codecs.open("sklearn-cluster-KMeans_October-21-2020_1426PM.txt", "r", encoding="utf-8")
    if int(mode) == 1:
        df = pd.read_csv(csv_file)
        df = df[df["Final Label"] == "Y"]
        df["GitHub Link"] = "https://github.com/" + df["GitHub Repo"]
        dict_of_urls = dict(zip(df["GitHub Repo"], df["GitHub Link"]))
    elif int(mode) == 2:
        df = pd.read_csv(csv_file)
        df.dropna(how="all", inplace=True) 
        dict_of_urls = dict(zip(df["Repo"], df["Web"]))
    return dict_of_urls
    
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: first argument = source of csv file, second argument = mode")
    csv = sys.argv[1]
    repo_urls = generate_list_of_urls_from_csv(csv, sys.argv[2]) # second argument represents mode

    # # creates folder to contain repos, if it doesn't already exist
    # Path(Path.cwd()/"java").mkdir(exist_ok = True)

    # opens file to record repos that encountered errors
    current_time = datetime.now().strftime("%B-%d-%Y_%H%M%p")
    errors_file_name =  "errorCloning_" + current_time + ".txt"
    errors_file = open(errors_file_name, 'w', encoding="utf-8")

    successes, failures = 0, 0
    commit_hashes = {}
    for repo, url in repo_urls.items():
        try:
            r = repo.replace("/", "--")
            p = Path("/media/haoteng")/"java"/r
            Path(p).mkdir(parents = True, exist_ok = True)

            print(f"Cloning {url}")
            gitrepo = git.Repo.clone_from(url = url, to_path = p)
            sha = gitrepo.head.commit.hexsha
            short_sha = gitrepo.git.rev_parse(sha, short=4)
            commit_hashes[url] = short_sha

            successes += 1
        except:
            errors_file.write(url + "\n")
            failures += 1

    d = pd.DataFrame.from_dict(commit_hashes, orient = "index", columns = ["Hash"])
    d.to_csv("java_commit_hashes.csv")

    errors_file.close()
    print(f"Repositories were cloned from Github! Success: {successes} Fail: {failures}")