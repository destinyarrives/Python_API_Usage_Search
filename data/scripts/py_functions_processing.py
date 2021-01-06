from pandas.io.json._normalize import nested_to_record
import json

def detect_spaces(api_name):
    if api_name.find(" ") != -1 and len(api_name.split(".")) > 1: # spaces detected
        tokens = api_name.split(".")
        return tokens[0] + "." + ".".join(tokens[2:])
    return False # returns false if api name is well-structured

# change path to where py_functions.json is stored
with open("data/py_functions.json") as datafile:
    data = json.load(datafile)
 
flat = nested_to_record(data, sep = '.') # flattens dictionary to the last level of indentation but without handling lists
output = []
for key, value in flat.items():
    output += [key + "." + item for item in value]

# if no spaces are detected, then item; if spaces detected, replace item with detect_spaces(item)
output = [item if not detect_spaces(item) else detect_spaces(item) for item in output]
# change path to where processed output is stored
with open("data/py_functions_processed.txt", "w") as outfile:
    for api in output:
        outfile.write(api + "\n")