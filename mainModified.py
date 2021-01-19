import os
import utils
import sys
from datetime import datetime
import queue
from api_formatter import *
import pandas as pd
from pathlib import Path
from shutil import copy2 
import json

#from git import Repo

# File wide constant
WRITE_QUEUE = queue.Queue()
CODE_QUEUE = queue.Queue()
FORMATTED_QUERY_NAME = ""
FORMATTED_QUERY_KEYS = []
# PYTHON_FILEPATHS = utils.get_all_py_files("/media/haoteng/python")
# APIS = process_list_of_apis("data/py_functions_processed_short.txt")
APIS = process_list_of_libraries("data/py_libraries_processed.txt")
with open("data/new_python_files.txt") as datafile:
    PYTHON_FILEPATHS = datafile.read().split("\n")[:-1]

def build_index():
    index = {}
    # temp_api = [i[0] + "." + i[1] for i in APIS]
    temp_api = APIS
    for api in temp_api:
        print(f"Indexing {api}...")
        index[api] = []
        for pyfile in PYTHON_FILEPATHS:
            with open(pyfile, "r") as pf:
                code = pf.read()
                if code.find(api) != -1:
                    index[api].append(pyfile)

def processFunction(result):
    file_count, api_instance_count = 0, 0
    try:
        global WRITE_QUEUE
        global CODE_QUEUE

        try:
            decoded_file_content = get_file_contents(result) #opens and reads .py file coming in
        except:
            return None
        try:
            tree = ast.parse(decoded_file_content)
        except:
            return

        api_name = FORMATTED_QUERY_NAME.split(".")[-1] #takes the method name in the api call, eg "relu" from "tf.nn.relu"
        list_processed_api = process_api_format(tree, api_name) #returns list of dict objects
        is_api_found = False
        list_api_location = []
        for entry in list_processed_api:
            current_name = entry["name"]
            current_keys = entry["key"]
            current_line = entry["line_no"]
            current_keys.append('')

            if FORMATTED_QUERY_NAME in current_name:
                # Then check the keys
                key_is_correct = True
                isNone = False
                for key in FORMATTED_QUERY_KEYS:
                    if key == "None":
                        isNone = True
                    if key not in current_keys:
                        key_is_correct = False
                # Special processing if query key is None
                if isNone:
                    # len is supposed to be 1 if no keyword is declared (e.g. only have '' as keyword param)
                    if len(current_keys) > 1:
                        key_is_correct = False
                    else:
                        key_is_correct = True
                if key_is_correct:
                    temp_string = "API Invocation in line: " + current_line.__str__() + "\n"
                    temp_string += entry["code"]
                    CODE_QUEUE.put(entry["code"])
                    list_api_location.append(temp_string)
                    is_api_found = True

        if is_api_found:
            # previously, if a 
            # temp = result.split(os.sep)
            # temp = temp[temp.index("engineered") + 1]
            # p = str(Path.cwd()) + "/result_snippets/" + FORMATTED_QUERY_NAME + "/" + temp
            # Path(p).mkdir(parents = True, exist_ok = True)
            # copy2(result, p)

            file_count += 1
            listWrite = []
            listWrite.append("----------------\n")
            listWrite.append("File path: " + result + "\n")
            for text in list_api_location:
                api_instance_count += 1
                listWrite.append(text + "\n")

            listWrite.append("\n")
            WRITE_QUEUE.put(listWrite)
    except Exception as e:
        print(e.__str__())
    
    return (file_count, api_instance_count)

def main(library, api_query):
    tfc, tapic = 0, 0
    try:
        global FORMATTED_QUERY_KEYS
        global FORMATTED_QUERY_NAME
    except:
        pass

    temp_query = library + "." + api_query
    temp = temp_query.split("(")
    # if len > 1, there are keyword queries
    if len(temp) > 1: 
        key_string = temp[1][:-1] #"n = 4"
        FORMATTED_QUERY_KEYS = key_string.split(",")
    FORMATTED_QUERY_NAME = temp[0] #"sklearn.cluster.KMeans"

    # Open the output file too
    current_time = datetime.now().strftime("%B-%d-%Y_%H%M%p")
    output_function = api_query.replace(".", "-")
    output_file_name = str(Path.cwd()/"result_summaries") + os.sep + output_function + "_" + current_time + ".txt"
    output_err_name = str(Path.cwd()/"result_errors") + os.sep + output_function + "_" + current_time + "_errors.txt"
    print(f"...Output file: {output_file_name}")
    outfile = open(output_file_name, 'w', encoding="utf-8")
    errorfile = open(output_err_name, "w", encoding="utf-8")

    start_time = time()

    # if an api mention is detected in file f, a copy of f will be saved in ../result_snippets/<api query>/<owner--project>/
    for f in PYTHON_FILEPATHS:
        try:
            total_file_count, total_api_instance_count = processFunction(f)
            tfc += total_file_count
            tapic += total_api_instance_count
        except:
            errorfile.write(f + "\n")

    #with DummyPool(32) as p:
    #    p.map(processFunction, search_result)
    for listQ in WRITE_QUEUE.queue:
        for line in listQ:
            outfile.write(line)

    outfile.write("***Python files evaluated in total: " + str(len(PYTHON_FILEPATHS)) + "\n")
    outfile.write("***Total files containing the API: " + tfc.__str__() + "\n")
    outfile.write("***Total API usage count: " + tapic.__str__() + "\n\n")
    outfile.write("***Time taken: " + (time() - start_time).__str__() + "\n\n")
    outfile.close()
    errorfile.close()

if __name__ == "__main__":
    """
    Usage of script:
    input: list of apis to search for
           directory of projects to search through
    output: 
    """
    (Path.cwd()/"result_summaries").mkdir(exist_ok = True)
    (Path.cwd()/"result_errors").mkdir(exist_ok = True)

    index = build_index()
    print("Indexing Complete!")

    with open('index.json', 'w') as indexfile:
        json.dump(index, indexfile)


    # torch_apis = process_list_of_torch_apis("torch_apis.txt")
    # torch_apis = [("PyTorch", "is_tensor")]
    # for l, q in APIS:
    #     print(f"Querying for {q}...")
    #     #TODO implement cheap search
    #     main(l, q)
    #     with WRITE_QUEUE.mutex:
    #         WRITE_QUEUE.queue.clear()
    #     with CODE_QUEUE.mutex:
    #         CODE_QUEUE.queue.clear()