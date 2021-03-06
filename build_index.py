import ahocorasick, json

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

def clean_final_json():
    # this function is such a dirty fix but it'll have to do for now... :')
    with open("../final_search.json") as jfile:
        data = json.load(jfile)
    with open("../py_functions.json") as tfile:
        functions = json.load(tfile)
    
    output = {}
    for library, dicts in data.items():
        output[library] = {} 
        for function, files in dicts.items():
            if not files:
                continue
            fqn = match_fqn(functions, library, function)
            output[library][fqn] = files
    
    return output

def match_fqn(fdict, lib, fun):
    templist = fdict[lib]
    for item in templist:
        if item[-1] == fun[:-1]:
            return (".".join(item))

if __name__ == '__main__':
    with open("../final_search_v2.json", "w") as outfile:
        output = clean_final_json()
        json.dump(output, outfile, indent = 4)

