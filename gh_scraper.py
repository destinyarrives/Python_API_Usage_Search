from bs4 import BeautifulSoup
import requests, itertools
import pandas as pd
from numpy import random
from time import sleep

pages = [f"https://reporeapers.github.io/results/{i}.html" for i in range(1, 4497)]

list_output = []
i = 0
for page in pages:
    i += 1
    if i == 5:
        sleeptime = random.uniform(5, 10)
        sleep(sleeptime)
        i = 0
        print(f"Sleeping for {sleeptime} seconds...")
    page_contents = requests.get(page)
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

df = pd.DataFrame(list_output, columns = ["Repo", "Web", "Language", "Architecture", "Community", "CL", "Documentation", "History",
                                          "Issues", "License", "Size", "Unit Test", "State", "Stars", "Org Score Based", "Org Random Forest",
                                          "Util Score Based", "Util Random Forest", "Timestamp"])
df["Size"] = df["Size"].str.replace(",", "").astype(int)
df.to_csv("reaper_results.csv")
