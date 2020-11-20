from pathlib import Path
import os

result = []
with open("add_November-17-2020_0713AM.txt", "r") as f:
    contents = f.read()
    contents = contents.split("----------------")
    for item in contents:
        result.append(item.partition("File path: ")[2].partition("\nAPI Invocation")[0])
print(*result[:5], sep = "\n")