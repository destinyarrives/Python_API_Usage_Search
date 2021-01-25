import ahocorasick, json
import numpy as np
import pandas as pd

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

# with open("data/py_libraries_processed.txt") as lf:
#     libraries = lf.read().split("\n")[:-1]
# with open("data/view.json") as jsonfile:
#     haystacks = json.load(jsonfile)
# with open("data/lib2func.json") as jsonfile:
#     needles = json.load(jsonfile)

# output = {}
# for lib, funcs in needles.items():
#     output[lib] = {}
#     for fun in funcs:
#         output[lib][fun] = []

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

# with open('final_search.json', 'w') as indexfile:
#     json.dump(output, indexfile, indent = 4) 

def clean_final_json():
    # this function is such a dirty fix but it'll have to do for now... :')
    with open("../testdata/final_search.json") as jfile:
        data = json.load(jfile) # data = {library:{truncated function:[file names]}}
    with open("../py_functions.json") as tfile:
        functions = json.load(tfile) # functions = default python functions json from Divya
    
    output = {}
    for library, dicts in data.items(): # dicts = {truncated function:[file names]}
        output[library] = {} 
        for function, files in dicts.items(): # function eg: "get_include("; files eg: ["/media/haoteng/python/Theano--Theano/theano/gpuarray/linalg.py", etc ...]
            if not files: # check if files list is empty- which happens if string matching doesn't find hits for a given api
                continue
            fqn = match_fqn(functions, library, function) # fqn = "lxml.lxml.get_include"
            output[library][fqn] = files
    
    return output

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

if __name__ == '__main__':
    with open("../final_search_v3.json", "w") as outfile:
        output = clean_final_json()
        json.dump(output, outfile, indent = 4)

    # with open("../verified_python_files.txt", "r") as python_files:
    #     python_files = python_files.read().split("\n")
    # with open("../py_libraries_processed.txt", "r") as python_libraries:
    #     python_libraries = python_libraries.read().split("\n")
    # result = acsearch_library_level(haystacks = python_files, needles = python_libraries)

    # with open("../library_results.json", "w") as outfile:
    #     json.dump(result, outfile, indent = 4)

    

