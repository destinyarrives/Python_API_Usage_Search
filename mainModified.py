import os
import utils
import sys
from datetime import datetime
from multiprocessing.dummy import Pool as DummyPool
import queue
from api_formatter import *
import pandas as pd
from pathlib import Path
from shutil import copy2 

#from git import Repo

# File wide constant
PYTHON_FILEPATHS = []
WRITE_QUEUE = queue.Queue()
CODE_QUEUE = queue.Queue()
FORMATTED_QUERY_NAME = ""
FORMATTED_QUERY_KEYS = []

def processFunctionModified(result, folder_to_move_into):
    try:
        global total_api_instance_count
        global total_file_count
        global SEARCHED_REPO
        global WRITE_QUEUE
        global CODE_QUEUE

        file_type = utils.get_file_type(result)
        if file_type != "py":
            return

        #print("Searching for API usage in: ")
        #print("    Repository name: " + repository_name)
        #print("        File path: " + current_file.path)

        """
        # Check if current file is contained within site-packages or venv
        list_not_processed = [".git", "venv", "site-packages", "sklearn"]
        contain_not_processed = False
        for term in list_not_processed: 
            if term in current_file.path: #see if term is in path of current file we're checking
                contain_not_processed = True
                break
        if contain_not_processed:
            return None
        """

        try:
            decoded_file_content = get_file_contents(result)
        except:
            return None
        try:
            tree = ast.parse(decoded_file_content)
        except:
            return

        # SAVE THE FILE TO COUNT THE RECALL LATER:


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
            print(result)
            copy2(result, folder_to_move_into + "/")
            total_file_count += 1
            listWrite = []

            #do we want the info on owner of repo?
            #listWrite.append("Repository: " + p + "\n") 
            listWrite.append("----------------\n")
            listWrite.append("File path: " + result + "\n")
            for text in list_api_location:
                total_api_instance_count += 1
                listWrite.append(text + "\n")

            listWrite.append("\n")
            WRITE_QUEUE.put(listWrite)
    except Exception as e:
        print(e.__str__())

if __name__ == "__main__":

    if len(sys.argv) < 3:
        print("USAGE: ")
        print('python search.py "LIBRARY_NAME" "FUNCTION_NAME" "FILE_TO_SEARCH_IN"')
        print('e.g. : python search.py "scikit-learn" "sklearn.cluster.KMeans" "/asdfasdf/test.py"')
        exit()

    #SEARCH_FILE = sys.argv[3]
    API_QUERY = sys.argv[2] #"sklearn.cluster.KMeans(n = 4)"
    LIBRARY = sys.argv[1] #"scikit-learn"

    # Changed into () from #
    temp = API_QUERY.split("(")
    # if len > 1, there are keyword query
    if len(temp) > 1: 
        key_string = temp[1][:-1] #"n = 4"
        FORMATTED_QUERY_KEYS = key_string.split(",")
    FORMATTED_QUERY_NAME = temp[0] #"sklearn.cluster.KMeans"

    # Open the output file too
    current_time = datetime.now().strftime("%B-%d-%Y_%H%M%p")
    output_function = API_QUERY.replace(".", "-")
    output_file_name = output_function + "_" + current_time + ".txt"
    print("Output file: " + output_file_name)
    outfile = open(output_file_name, 'w', encoding="utf-8")
    #outfile.write("Total amount of searched repo: " + total_count.__str__() + "\n")

    # Prepare folder to move resultant files into
    p = str(Path.cwd()) + "/result_snippets/" + FORMATTED_QUERY_NAME + "_" + current_time
    print(p)
    try:
        Path(p).mkdir(parents = True, exist_ok = True)
    except:
        pass

    total_file_count = 0
    total_api_instance_count = 0

    start_time = time()

    PYTHON_FILEPATHS = utils.get_all_py_files(Path.cwd()/"engineered"/"adaptnlp")

    for file in PYTHON_FILEPATHS:
        processFunctionModified(file, p)

    #with DummyPool(32) as p:
    #    p.map(processFunction, search_result)

    for listQ in WRITE_QUEUE.queue:
        for line in listQ:
            print(line)
            outfile.write(line)

    outfile.write("APIs evaluated in total: " + str(len(PYTHON_FILEPATHS)) + "\n")
    outfile.write("Total file containing the API: " + total_file_count.__str__() + "\n")
    outfile.write("Total API usage count: " + total_api_instance_count.__str__() + "\n\n")
    outfile.write("Time taken: " + (time() - start_time).__str__() + "\n\n")
    outfile.close()

    print("Time taken: " + (time() - start_time).__str__())