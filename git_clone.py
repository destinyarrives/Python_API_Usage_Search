from git import Repo
import pandas as pd

def generate_list_of_urls_to_download(csv_file):
    """
    input: output file from main.py
    output: list of urls that can be fed into download_raw_file function
    """
    #results_file = codecs.open("sklearn-cluster-KMeans_October-21-2020_1426PM.txt", "r", encoding="utf-8")

    df = pd.read_csv(csv_file)
    df = df[df["Final Label"] == "Y"]
    list_of_urls = df["GitHub Repo"].tolist()
    return list_of_urls

generate_list_of_urls_to_download("projects.csv")
