import sys
from time import time
import ast
import astunparse
from github import Github
import requests
from requests.auth import HTTPBasicAuth
import os

# my github api key will be stored in an untracked token.txt file
token_file = os.path.join(os.getcwd(), "token.txt")

with open(token_file, 'rt') as f:
    GITHUB_TOKEN = f.read().replace('\n', '')
#GITHUB_TOKEN = "aa829f9756cfd2ff68d08cb11fd91722b4cf1957"


def open_github_connection():
    if not GITHUB_TOKEN:
        sys.exit("Error: Github token is not set or incorrect.\nPlease set your Github token in utils.py file")
    return Github(GITHUB_TOKEN, timeout=30, per_page=100)

# Return:
# 1 === Connection successful
# 0 === Credential error
# -1 === No internet connection
def test_github_connection():
    try:
        r = requests.get('https://api.github.com/user', auth=HTTPBasicAuth("username", GITHUB_TOKEN))
        try:
            user = r.json()['login']
            print("Connection successful!!!")
            return 1
        except:
            print(r.content.__str__())
            print("Error: token/credential invalid!!!")
            return 0
    except:
        print("Error: no connection!!!")
        return -1


# Recursive search on the repository
def find_requirements_file(repository):
    start_time = time()
    # Consider adding setup.py later
    requirement_filename = ["requirements.txt"]
    repoContents = repository.get_contents("")
    returnFile = None
    while repoContents:
        file = repoContents.pop(0)
        # Recursive if found directory
        if file.type == "dir":
            repoContents.extend(repository.get_contents(file.path))
        else:
            if file.name in requirement_filename:
                returnFile = file
                break
    print("Time finding requirements file: " + (time() - start_time).__str__())
    return returnFile

def get_library_versions(list_requirements, library_name):
    start_time = time()
    for req in list_requirements:
        if library_name in req:
            split = req.split("==")
            lib_name = split[0]
            if library_name == lib_name:
                if len(split) > 1:
                    lib_version = split[1]
                    return lib_version
                else:
                    return "newest"
    print("Time finding specific library versions: " + (time() - start_time).__str__())
    return None

def get_file_type(filename):
    splitted_name = filename.split(".")
    file_type = splitted_name[-1]
    return file_type


def getName(node):
    try:
        return node.attr
    except:
        try:
            return node.id
        except:
            try:
                return node.func.id
            except:
                try:
                    return node.func.attr
                except:
                    try:
                        return node.value.id
                    except:
                        try:
                            return node.value.attr
                        except:
                            # End of support
                            return None

# helper function to get the API invocation or function keyword arguments list
# return list of keyword argument name. e.g.
# getKeywordArguments(sklearn.cluster.KMeans(n_clusters=10).fit(X=[1,2,3])
# -> [X]
def getKeywordArguments(node):
    list_keyword = []
    if (isinstance(node, ast.Call)):
        for keyword in node.keywords:
            keyword_split = astunparse.unparse(keyword).split("=")
            keyword_string = keyword_split[0]
            list_keyword.append(keyword_string)
    return list_keyword

def getScopeNode(node):
    try:
        return node.func.value
    except:
        try:
            return node.value
        except:
            return None

def recurseScope(node):
    returnList = []
    scope = getScopeNode(node)
    returnList.append(scope)
    if scope is not None:
        # Has scope that might be function call too
        recurseList = recurseScope(scope)
        returnList += recurseList
    return returnList