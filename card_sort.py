from pathlib import Path
import os
from shutil import copy2 

result = []
with open("add_November-17-2020_0713AM.txt", "r") as f:
    contents = f.read()
    contents = contents.split("----------------")
    for item in contents:
        result.append(item.partition("File path: ")[2].partition("\nAPI Invocation")[0])
for fpath in result:
    copy2.()