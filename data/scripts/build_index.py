import ahocorasick, json
import numpy as np
import pandas as pd

"""
I've chose to do the index twice for the following reason: given a FQN "tensorflow.python.keras.engine.base_layer.Metric.call()", one import the api with
"from tensorflow.python.keras.engine.base_layer.Metric import call", or call it with the FQN itself. 

Hence, I first search for the library name "tensorflow", then from the results that contain the string "tensorflow" I search for the substring "call("
to generate candidates to iterate through using main.py. 
"""

def acsearch_library_level(haystacks, needles):
    output = {}
    for lib in needles:
        output[lib] = []

    A = ahocorasick.Automaton()
    for idx, key in enumerate(needles):
        A.add_word(key, (idx, key))
    A.make_automaton()

    ct = 0
    for f in haystacks:
        if (ct % 10000) == 0:
            print(f"processed {ct} files...")
        with open(f, "r") as haystack:
            haystack = haystack.read()
            for end_index, (insert_order, original_value) in A.iter(haystack):
                if f not in output[original_value]:
                    output[original_value].append(f)
        ct += 1

    return output

def acsearch(haystacks, needles):
    output = {}

    for k, v in haystacks.items():
        print(f"evaluating {k}")
        A = ahocorasick.Automaton()
        for idx, key in enumerate(needles[k]):
            A.add_word(key, (idx, key))
        A.make_automaton()

        for haystack in v:
            with open(haystack) as codefile:
                code = codefile.read()
                for end_index, (insert_order, original_value) in A.iter(code):
                    if haystack not in output[k][original_value]:
                        output[k][original_value].append(haystack)
    
    return output

def clean_final_json(): # this function is such a dirty fix but it'll have to do for now... :')
    with open("../testdata/final_search.json") as jfile:
        data = json.load(jfile) # data = {library:{truncated function:[file names]}}
    with open("../py_functions.json") as tfile:
        functions = json.load(tfile) # functions = default python functions json from Divya
    
    output = {}

    for library, list_functions in functions.items():
        output[library] = {}
        for functions in list_functions:
            list_files = reverse_match_fqn(functions[2], data[library])
            if not list_files:
                continue
            if functions[1][0].isupper():
                temp_key = ".".join(functions)
            else:
                temp_key = functions[0] + "." + functions[2]
            output[library][temp_key] = list_files
    
    return output

    #! previous erroneous version that only assigns the list to the first instance of an api name; thus missing out on a lot of possible matches
    # for library, dicts in data.items(): # dicts = {truncated function:[file names]}
    #     output[library] = {} 
    #     for function, files in dicts.items(): # function eg: "get_include("; files eg: ["/media/haoteng/python/Theano--Theano/theano/gpuarray/linalg.py", etc ...]
    #         if not files: # check if files list is empty- which happens if string matching doesn't find hits for a given api
    #             continue
    #         fqn = match_fqn(functions, library, function) # fqn = "lxml.lxml.get_include"
    #         output[library][fqn] = files
    
    # return output

# get list of relevant files using the fqn from py_functions.json
def reverse_match_fqn(string_fragment, datadict):
    for key, value in datadict.items():
        if key[:-1] == string_fragment:
            return value

# get the fqn using the partial api string 
def match_fqn(fdict, lib, fun):
    """
    Because of the possibility that function might originate from a modeule or class, match_fqn checks to see if the second term in the py_functions.json
    list is capitalised; if it is, it's assumed that the method belongs to a class and the second term will be included in the type search. Otherwise, 
    it's assumed that the function belongs to a module and the api will only consist of library name + function name in the type search. 
    """
    templist = fdict[lib] # templist = list of lists, each list consists of three parts, eg: ["numpy", "numpy", "zeros_like"]
    for item in templist: # item = three-element list identifying function
        if item[-1] == fun[:-1]:
            if item[1][0].isupper():
                return (".".join(item))
            else:
                return item[0] + "." + item[2]

#TODO up to you to activate which part of the functions
if __name__ == '__main__':
    with open("../final_search_v4.json", "w") as outfile:
        output = clean_final_json()
        json.dump(output, outfile, indent = 4)

    # with open("../verified_python_files.txt", "r") as python_files:
    #     python_files = python_files.read().split("\n")
    # with open("../py_libraries_processed.txt", "r") as python_libraries:
    #     python_libraries = python_libraries.read().split("\n")
    # result = acsearch_library_level(haystacks = python_files, needles = python_libraries)

    # with open("../library_results.json", "w") as outfile:
    #     json.dump(result, outfile, indent = 4)

    

