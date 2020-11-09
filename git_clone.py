import git
from pathlib import Path
import pandas as pd

def generate_list_of_urls_to_download(csv_file):
    """
    input: output file from main.py
    output: list of urls that can be fed into download_raw_file function 
            eg - "https://github.com/Project-MONAI/MONAI"
    """
    #results_file = codecs.open("sklearn-cluster-KMeans_October-21-2020_1426PM.txt", "r", encoding="utf-8")

    df = pd.read_csv(csv_file)
    df = df[df["Final Label"] == "Y"]
    df["GitHub Repo"] = "https://github.com/" + df["GitHub Repo"]
    list_of_urls = df["GitHub Repo"].tolist()
    return list_of_urls

urls = generate_list_of_urls_to_download("projects.csv")

# creates folder to contain repos, if it doesn't already exist
p = Path.cwd()/"engineered"
try:
    Path(p).mkdir()
except:
    print("Folder already exists, moving on to the next step...")

for url in urls:
    git.Git(p).clone(url)
