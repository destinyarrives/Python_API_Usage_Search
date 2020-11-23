from pathlib import Path
import os
from shutil import copy2 
from random import sample

result = {}
new_location = Path.cwd()/"manual_analysis"
new_location.mkdir(exist_ok = True)
with open("add_November-17-2020_0713AM.txt", "r") as f:
    contents = f.read()
    contents = contents.split("----------------")[1:]
    for item in sample(contents, 50):
        filepath = item.partition("File path: ")[2].partition("\nAPI Invocation")[0]
        filename1 = filepath.partition("--")[2].partition("/")[0]
        filename2 = filepath.split("/")[-1]
        filename = filename1 + "--" + filename2
        result[filename] = filepath

i = 0
for fn, fp in result.items():
    i += 1
    # print(fn, fp)
    # print(new_location/fn)
    copy2(fp, new_location/fn)    
    if i > 5:
        break
