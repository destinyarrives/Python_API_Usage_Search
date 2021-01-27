from pathlib import Path
import os, sys
from shutil import copy2 
from random import sample

def find_files_from_result(c):
    result = {}
    c = c.split("----------------")[1:]
    if len(c) > 10:
        c = sample(c, 10)
    for item in c: 
        fpath = item.partition("File path: ")[2].partition("\nAPI Invocation")[0]
        filename1 = fpath.partition("--")[2].partition("/")[0]
        filename2 = fpath.split("/")[-1]
        filename = filename1 + "--" + filename2
        result[filename] = fpath
    return result

if __name__ == '__main__':
    new_location = Path.cwd()/"manual_analysis"
    new_location.mkdir(exist_ok = True)
    DIRECTORY = "data/testdata/temp_results/1_260121"
    random.seed("hope this was useful lol")

    all_apis = []
    for subdir, dirs, files in os.walk(DIRECTORY): 
        for filename in files:
            filepath = subdir + os.sep + filename
            all_apis.append(filepath)
    
    for api in sample(all_apis, 50):
        print(f"choosing {api}")
        ct = 0 #TODO possibly automate this for average accuracy computation using pandas?

        folder = api.split("/")[4].split(".")[0]
        with open(api, "r") as f:
            contents = f.read()
            output_dict = find_files_from_result(contents)
        with open(f"manualAnalysis_{ct}.txt", "w") as outfile:
            for fn, fp in output_dict.items():
                copy2(fp, new_location/folder/fn) #! need to further organise by api 
                outfile.write(fp + "\n\n")
        ct += 1
