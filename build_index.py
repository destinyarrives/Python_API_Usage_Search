import ahocorasick
import numpy as np
import pandas as pd

def acsearch(haystacks, needles):
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

with open("data/py_libraries_processed.txt") as lf:
    libraries = lf.read().split("\n")[:-1]

with open("data/view.json") as jsonfile:
    haystacks = json.load(jsonfile)

with open("data/lib2func.json") as jsonfile:
    needles = json.load(jsonfile)

output = {}
for lib, funcs in needles.items():
    output[lib] = {}
    for fun in funcs:
        output[lib][fun] = []



with open('final_search.json', 'w') as indexfile:
    json.dump(output, indexfile, indent = 4) 
