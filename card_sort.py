from pathlib import Path
import os, sys
from shutil import copy2 
from random import sample

def find_files_from_result(c):
    """
    based on the output from the main.py function, this function parses the individual text file and finds all the files that contain results,
    plus the filepath to access the relevant file. 

    output: dictionary of {filename:filepath}
    """
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
    #TODO change this to where the results snippets from main.py are stored in
    DIRECTORY = Path.cwd()/"1_260121"

    new_location = Path.cwd()/"manual_analysis" # path for putting results into
    new_location.mkdir(exist_ok = True)
    random.seed("lol if you're seeing this, I hope I was helpful :')") # optional seed to make repeating the api-sampling repeatable

    # extract all the text files from DIRECTORY to run find_files_from_result on:
    all_apis = []
    for subdir, dirs, files in os.walk(DIRECTORY): 
        for filename in files:
            filepath = subdir + os.sep + filename
            all_apis.append(filepath)
    
    # sampling strategy: pick 50 random apis, for each api choose 10 mentions and manually evaluate
    for api in sample(all_apis, 50):
        print(f"choosing {api}")
        ct = 0 

        folder = api.split("/")[5].split(".")[0]
        with open(api, "r") as f:
            contents = f.read()
            output_dict = find_files_from_result(contents)
        with open(f"manualAnalysis_{ct}.txt", "w") as outfile:
            for fn, fp in output_dict.items():
                tempfolder = Path.cwd()/"manual_analysis"/folder
                tempfolder.mkdir(exist_ok = True)
                copy2(fp, new_location/folder/fn) 
                outfile.write(fp + "\n\n")
        ct += 1
