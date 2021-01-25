import ahocorasick, json
import numpy as np
import pandas as pd

def acsearch_library_level(haystacks, needles):
    output = {}
    for lib in haystacks:
        output[lib] = []

    A = ahocorasick.Automaton()
    for idx, key in enumerate(needles):
        A.add_word(key, (idx, key))
    A.make_automaton()

    for f in haystacks:
        with open(f, "r") as haystack:
            haystack = haystack.read()
            for end_index, (insert_order, original_value) in A.iter(haystack):
                if f not in output[original_value]:
                    output[original_value].append(f)

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

# with open('final_search.json', 'w') as indexfile:
#     json.dump(output, indexfile, indent = 4) 

def clean_final_json():
    # this function is such a dirty fix but it'll have to do for now... :')
    with open("final_search.json") as jfile:
        data = json.load(jfile)
    with open("py_functions.json") as tfile:
        functions = json.load(tfile)
    
    output = {}
    for library, dicts in data.keys():
        output[library] = {} 
        for function, files in dicts.keys():
            if not files:
                continue
            fqn = match_fqn(functions, library, function)
            output[library][fqn] = files
    
    return output

def match_fqn(fdict, lib, fun):
    templist = fdict[lib]
    for item in templist:
        if item[-1] == func[:-1]:
            return (".".join(item))

if __name__ == '__main__':
    # with open("final_search_v2.json") as outfile:
    #     output = clean_final_json()
    #     json.dump(output, outfile, indent = 4)

    with open("../verified_python_files.txt", "r") as python_files:
        python_files = python_files.read().split("\n")
    with open("../py_libraries_processed.txt", "r") as python_libraries:
        python_libraries = python_libraries.read().split("\n")
    result = acsearch_library_level(python_files, python_libraries)

    with open("../library_results.json", "w") as outfile:
        json.dump(result, outfile, indent = 4)

    

