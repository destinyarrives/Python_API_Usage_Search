import git, sys
from pathlib import Path
from datetime import datetime
import pandas as pd

def generate_list_of_urls_from_csv(csv_file, mode):
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
        dict_of_urls = dict(zip(df["Repo"], df["Web"]))
    return dict_of_urls

# def do_git_clone(dict_of_urls):
#     """
#     uses list of github urls and clones them into a folder- the naming structure will be ../engineered/<project name>/

#     input: output from generate_list_of_urls_from_csv function 
#     output: 
#     """
    
if __name__ == "__main__":
    csv = sys.argv[1]
    repo_urls = generate_list_of_urls_from_csv(csv, sys.argv[2]) # second argument represents mode

    # creates folder to contain repos, if it doesn't already exist
    Path(Path.cwd()/"python").mkdir(exist_ok = True)

    # opens file to record repos that encountered errors
    current_time = datetime.now().strftime("%B-%d-%Y_%H%M%p")
    output_file_name =  "errorCloning_" + current_time + ".txt"
    outfile = open(output_file_name, 'w', encoding="utf-8")

    successes, failures = 0, 0
    commit_hashes = {}
    for repo, url in repo_urls.items():
        print(repo, url)
        if repo and url:
            try:
                r = repo.replace("/", "--")
                p = Path("/media/haoteng")/"python"/r
                Path(p).mkdir(parents = True, exist_ok = True)

                print(f"Cloning {url}")
                gitrepo = git.Repo.clone_from(url = url, to_path = p)
                sha = gitrepo.head.commit.hexsha
                short_sha = gitrepo.git.rev_parse(sha, short=4)
                commit_hashes[url] = short_sha

                successes += 1

            except:
                outfile.write(url + "\n")
                failures += 1

    d = pd.DataFrame.from_dict(commit_hashes)
    d.to_csv("python_commit_hashes.csv", index = False)

    outfile.close()
    print(f"Repositories were cloned from Github! Sucess:{successes} Fail:{failures}")