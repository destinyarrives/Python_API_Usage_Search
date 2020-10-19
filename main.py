import os
import utils
import sys
from datetime import datetime
from multiprocessing.dummy import Pool as DummyPool
import queue
from api_formatter import *


# File wide constant
MINIMUM_STAR = 0
SEARCHED_REPO = {}
DOWNLOAD_LIST = queue.Queue()
WRITE_QUEUE = queue.Queue()
CODE_QUEUE = queue.Queue()
FORMATTED_QUERY_NAME = ""
FORMATTED_QUERY_KEYS = []

def processFunction(result):
    try:
        global total_api_instance_count
        global total_file_count
        global SEARCHED_REPO
        global DOWNLOAD_LIST
        global WRITE_QUEUE
        global CODE_QUEUE

        current_file = result
        current_repo = result.repository
        repository_name = current_repo.full_name
        file_type = utils.get_file_type(current_file.name)
        print("Searching for API usage in: ")
        print("    Repository name: " + repository_name)
        print("        File path: " + current_file.path)


        # Check if current file is contained within site-packages or venv
        list_not_processed = [".git", "venv", "site-packages", "sklearn"]
        contain_not_processed = False
        for term in list_not_processed:
            if term in current_file.path:
                contain_not_processed = True
                break
        if contain_not_processed:
            return None

        # Check if the repo is already looked into before
        # And check the minimum number of star on the repo
        # Consider deactivating the functionality for ipynb / jupyter notebook first because of their different
        # type of file (not a simple plain text)

        # Also consider a less rigid approach in which a repo does not need to have a requirements.txt but instead have
        # a mention of sklearn in the readme as there are some people who list their requirements in the readme

        already_exist = False
        # check if repository is checked before
        if repository_name in SEARCHED_REPO:
            REPO_PATH = SEARCHED_REPO[repository_name]
            # check if the same path is already checked
            # if not, add to the list of checked path
            if current_file.path in REPO_PATH:
                already_exist = True
            else:
                REPO_PATH.append(current_file.path)
        else:
            # Repository is not checked yet, add them into the dictionary
            SEARCHED_REPO[repository_name] = [current_file.path]

        if not already_exist and current_repo.stargazers_count >= MINIMUM_STAR:
            # Process the file content
            try:
                decoded_file_content = current_file.decoded_content.decode("utf-8")
            except:
                return None
            try:
                tree = ast.parse(decoded_file_content)
            except:
                return

            # SAVE THE FILE TO COUNT THE RECALL LATER:


            api_name = FORMATTED_QUERY_NAME.split(".")[-1]
            list_processed_api = process_api_format(tree, api_name)
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
                git_url = current_file.repository.git_url
                if git_url not in DOWNLOAD_LIST.queue:
                    DOWNLOAD_LIST.put("git clone " + git_url + "\n")
                total_file_count += 1
                listWrite = []
                listWrite.append("----------------\n")
                listWrite.append("Github Link: " + git_url.__str__() + "\n")
                listWrite.append("Repository: " + repository_name + "\n")
                listWrite.append("File path: " + current_file.path + "\n")
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
        print('python search.py "LIBRARY_NAME" "FUNCTION_NAME"')
        print('e.g. : python search.py "scikit-learn" "sklearn.cluster.KMeans"')
        exit()

    # Github API search provide up to 1000 results for each search
    PYTHON_LANGUAGE_QUERY = "language:python"
    API_QUERY = sys.argv[2]
    LIBRARY = sys.argv[1]
    SEARCH_QUERY = "q={}+extension:py".format(API_QUERY)

    # Changed into () from #
    temp = API_QUERY.split("(")
    # if len > 1, there are keyword query
    if len(temp) > 1:
        key_string = temp[1][:-1]
        FORMATTED_QUERY_KEYS = key_string.split(",")
    FORMATTED_QUERY_NAME = temp[0]

    # Create and test connection
    g = utils.open_github_connection()

    conn = utils.test_github_connection()
    functionName = API_QUERY.__str__().split(".")[-1]
    if conn != 1:
        exit()

    search_result = g.search_code(SEARCH_QUERY)
    total_count = search_result.totalCount
    # You can modify the amount of searched repo using python array slicing here
    # search_result = search_result[0:100]

    print("Query: " + SEARCH_QUERY)

    # Open the output file too
    current_time = datetime.now().strftime("%B-%d-%Y_%H%M%p")
    output_function = API_QUERY.replace(".", "-")
    output_file_name = output_function + "_" + current_time + ".txt"
    print("Output file: " + output_file_name)
    outfile = open(output_file_name, 'w', encoding="utf-8")
    outfile.write("Total amount of searched repo: " + total_count.__str__() + "\n")

    total_file_count = 0
    total_api_instance_count = 0

    start_time = time()

    print(search_result)

    with DummyPool(32) as p:
        p.map(processFunction, search_result)

    for listQ in WRITE_QUEUE.queue:
        for line in listQ:
            print(line)
            outfile.write(line)

    outfile.write("Total file containing the API: " + total_file_count.__str__() + "\n")
    outfile.write("Total API usage count: " + total_api_instance_count.__str__() + "\n\n")
    outfile.write("Download link and script below: \n")
    outfile.write("Time taken: " + (time() - start_time).__str__() + "\n\n")
    for line in DOWNLOAD_LIST.queue:
        outfile.write(line)
    outfile.close()

    print("Time taken: " + (time() - start_time).__str__())