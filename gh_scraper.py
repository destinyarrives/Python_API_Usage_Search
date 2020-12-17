from bs4 import BeautifulSoup
import requests, itertools
import pandas as pd
from numpy import random
from time import sleep

pages = [f"https://reporeapers.github.io/results/{i}.html" for i in range(1, 4497)]

list_output = []
for page in pages:
    page_contents = requests.get(page)
    print(f"Processing {page}...")
    soup = BeautifulSoup(page_contents.content, 'html.parser')
    result = soup.find_all(name = "tr")

    for tr in result[2:]:
        temp = []
        for td in tr.children:
            if td.string != "\n":
                if td.string != None:
                    temp.append(td.string)
                else:
                    temp.append(td.a.next_sibling.next_sibling["href"])
        list_output.append(temp)
    
    sleeptime = random.uniform(1, 5)
    sleep(sleeptime)

df = pd.DataFrame(list_output, columns = ["Repo", "Web", "Language", "Architecture", "Community", "CL", "Documentation", "History",
                                          "Issues", "License", "Size", "Unit Test", "State", "Stars", "Org Score Based", "Org Random Forest",
                                          "Util Score Based", "Util Random Forest", "Timestamp"])
df["Size"] = df["Size"].str.replace(",", "").astype(int)
df.to_csv("reaper_results.csv")
