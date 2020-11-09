import git
from pathlib import Path
import pandas as pd

def generate_list_of_urls_to_download(csv_file):
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

def get_repos(d):
    return d.keys()

def get_urls(d):
    return d.values()


if __name__ == "__main__":

    repo_urls = generate_list_of_urls_to_download("projects.csv")

    # creates folder to contain repos, if it doesn't already exist
    p = Path.cwd()/"engineered"
    try:
        Path(p).mkdir()
    except:
        print("Folder already exists, moving on to the next step...")

    current_time = datetime.now().strftime("%B-%d-%Y_%H%M%p")
    output_file_name =  "errorCloning_" + current_time + ".txt"
    outfile = open(output_file_name, 'w', encoding="utf-8")

    successes, failures = 0, 0
    for url in get_urls(repo_urls):
        try:
            print(f"Cloning {url}")
            git.Git(p).clone(url)
            successes += 1
        except:
            outfile.write(url)
            failures += 1

    outfile.close()
    print(f"Repositories were cloned from Github! Sucess:{successes} Fail:{failures}")