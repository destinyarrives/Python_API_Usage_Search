from pandas.io.json._normalize import nested_to_record
import json

def detect_spaces(api_name):
    """
    no longer used; the json structure used to be that the package name would sometimes include spaces (eg, "Flask Library")
    function will detect spaces in the package name and skip the problematic levels, example:

    input : "Flask" : {"Flask Library" : ["abort", "after this request"]}
    output : "Flask" : ["abort", "after this request"]
    """
    if api_name.find(" ") != -1 and len(api_name.split(".")) > 1: # spaces detected
        tokens = api_name.split(".")
        return tokens[0] + "." + ".".join(tokens[2:])
    return False # returns false if api name is well-structured

def process_dict(datadict):
    """
    input : 

    library/package name:
    {
        "IPython": [
            [
                "IPython.core.ultratb",
                "AutoFormattedTB",
                "format_record"
            ], 
            ...
        ],
        ...
    }

    output: ['IPython.core.ultratb.AutoFormattedTB.format_record', 'IPython.utils.decorators.pylabtools.flag_calls', ...]
    """
    output = []
    for package, detail in datadict.items(): # detail being a list of lists
        for item in detail:
            output.append(".".join(item))
    return output

# change path to where py_functions.json is stored
with open("data/py_functions.json") as datafile:
    data = json.load(datafile)

# writes list of methods to search for in a textfile
with open("data/py_functions_processed.txt", "w") as outfile:
    data = process_dict(data)
    for item in data:
        outfile.write(item + "\n")


# flat = nested_to_record(data, sep = '.') # flattens dictionary to the last level of indentation but without handling lists
# output = []
# for key, value in flat.items():
#     output += [key + "." + item for item in value]

# # if no spaces are detected, then item; if spaces detected, replace item with detect_spaces(item)
# output = [item if not detect_spaces(item) else detect_spaces(item) for item in output]
# # change path to where processed output is stored
# with open("data/py_functions_processed.txt", "w") as outfile:
#     for api in output:
#         outfile.write(api + "\n")