from pandas.io.json._normalize import nested_to_record
import json
 
with open("data/py_functions.json") as datafile:
data = json.load(datafile)
 
flat = nested_to_record(data, sep='.')
output = []
for key, value in flat.items():
output += [key + “.” + item for item in value]
print(output)