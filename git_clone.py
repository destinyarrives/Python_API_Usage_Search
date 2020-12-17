import git
from pathlib import Path
from datetime import datetime
import pandas as pd

def generate_list_of_urls_from_csv(csv_file):
    """
    input: output file from main.py
    output: dict of urls that can be fed into download_raw_file function 
            eg - "Project-MONAI/MONAI":"https://github.com/Project-MONAI/MONAI"
    """
    #results_file = codecs.open("sklearn-cluster-KMeans_October-21-2020_1426PM.txt", "r", encoding="utf-8")

    df = pd.read_csv(csv_file)
    df = df[df["Final Label"] == "Y"]
    df["GitHub Link"] = "https://github.com/" + df["GitHub Repo"]
    dict_of_urls = dict(zip(df["GitHub Repo"], df["GitHub Link"]))
    return dict_of_urls

if __name__ == "__main__":

    repo_urls = generate_list_of_urls_from_csv("projects.csv")

    # creates folder to contain repos, if it doesn't already exist
    Path(Path.cwd()/"engineered").mkdir(exist_ok = True)

    # opens file to record repos that encountered errors
    current_time = datetime.now().strftime("%B-%d-%Y_%H%M%p")
    output_file_name =  "errorCloning_" + current_time + ".txt"
    outfile = open(output_file_name, 'w', encoding="utf-8")

    successes, failures = 0, 0
    for repo, url in repo_urls.items():
        try:
            r = repo.replace("/", "--")
            p = Path.cwd()/"engineered"/r
            Path(p).mkdir(parents = True, exist_ok = True)
            print(f"Cloning {url}")
            git.Git(p).clone(url)
            successes += 1
        except:
            outfile.write(url + "\n")
            failures += 1

    outfile.close()
    print(f"Repositories were cloned from Github! Sucess:{successes} Fail:{failures}")