from bs4 import BeautifulSoup
import requests, itertools, sys
import pandas as pd
from numpy import random
from time import sleep

def analyse_scraped_csv(csv_file, lang, stars):
    df = pd.read_csv(csv_file)
    df["cscore"] = df["Org Score Based"] + df["Org Random Forest"] + df["Util Score Based"] + df["Util Random Forest"]
    df = df[(df["cscore"] >= stars) & (df["Language"] == lang)]
    df.to_csv(f"{lang}_{stars}.csv", index = False)

# current page is at 100
# max = 4497
start, end = sys.argv[1], sys.argv[2]
pages = [f"https://reporeapers.github.io/results/{i}.html" for i in range(int(start), int(end))]

list_output = []
outfile = open("ghscraperlog.txt", 'w', encoding="utf-8") # open file to write down pages that produced errors
for page in pages: 
    try:
        page_contents = requests.get(page) # query the current page
        print(f"Processing {page}...")
        soup = BeautifulSoup(page_contents.content, 'html.parser') # parse the current page
        result = soup.find_all(name = "tr") 

        for tr in result[2:]: # retrieve the rows from the table, excluding the header (Repository, Links, Language ... Timestamp)
            temp = []
            for td in tr.children: # iterate through the columns in each row
                if td.string != "\n": # skip the escape sequences
                    if td.string != None: # access the navigablestring portion contained within the tag 
                        temp.append(td.string) 
                    else: # to account for the <Links> column, where the API | Web links are given
                        temp.append(td.a.next_sibling.next_sibling["href"]) 
            list_output.append(temp) 
        
        sleeptime = random.uniform(4, 6)
        sleep(sleeptime)
    except:
        outfile.write(page + "\n")
outfile.close()

df = pd.DataFrame(list_output, columns = ["Repo", "Web", "Language", "Architecture", "Community", "CL", "Documentation", "History",
                                          "Issues", "License", "Size", "Unit Test", "State", "Stars", "Org Score Based", "Org Random Forest",
                                          "Util Score Based", "Util Random Forest", "Timestamp"])
df["Size"] = df["Size"].str.replace(",", "").astype(int)
df.to_csv("reaper_results.csv", mode = "a", index = False, header = False)



