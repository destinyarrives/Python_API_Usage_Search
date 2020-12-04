from pathlib import Path
import os
from shutil import copy2 
from random import sample

result = {}
new_location = Path.cwd()/"manual_analysis"
new_location.mkdir(exist_ok = True)
input_file = sys.argv[1]
with open(str(Path.cwd()) + "/" + input_file, "r") as f:
    contents = f.read()
    contents = contents.split("----------------")[1:]
    for item in sample(contents, 100):
        filepath = item.partition("File path: ")[2].partition("\nAPI Invocation")[0]
        filename1 = filepath.partition("--")[2].partition("/")[0]
        filename2 = filepath.split("/")[-1]
        filename = filename1 + "--" + filename2
        result[filename] = filepath

i = 0
with open("manualAnalysis.txt", "w") as outfile:
    for fn, fp in result.items():
        copy2(fp, new_location/fn)    
        outfile.write(fp + "\n\n")
