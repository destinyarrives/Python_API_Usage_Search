# DeepHarvest Python Project
The high-level goal of this project is to create a set of functions which, when given two inputs 1. a set of projects and 2. a set of APIs we're interested in, creates output: search results of where APIs we're interested in (2) appear in the set of projects (1). 

## Setup/Requirements

- Python 3.6 and up
- Use the desired package manager (pip or conda) to install from requirements.txt. 


## Workflow
The general workflow for the project is as follows: (A) find engineered python projects -> (B) clone these projects -> (C) obtain a list of apis we're interested in and process them in the appropriate manner -> (D) first build an index of candidate matches to perform search on, this might require two passes through every flie in step B -> (E) using the index from step D run the type matching function to obtain final search results -> (F) manually check the returned results to see if the matching was accurate and compute avg accuracy. 

#### A. Finding Engineered Projects
./scraping/gh_scaper.py

Script outputs a csv file that will be populated with all the data from the RepoReapers page (https://reporeapers.github.io/results/1.html). Columns consist of ["Repo", "Web", "Language", "Architecture", "Community", "CL", "Documentation", "History", "Issues", "License", "Size", "Unit Test", "State", "Stars", "Org Score Based", "Org Random Forest", "Util Score Based", "Util Random Forest", "Timestamp"]... The csv will also be filtered based on programming language and predicted score assigned by the 4 different classifiers of the RepoRepears project. For our purposes we will only use those that have a combined score of 4/4 (meaning each of the 4 classifiers predicted the project is engineered). 

#### B. Cloning Projects
./git_clone.py

Script takes as input the csv from (A) and clones them into the folder which you can name. The folders containing each project will be named "./<project owner name>--<project name>/"

#### C. API Json Processing
./data/scripts/py_functions_processing.py

Some useful functions for processing the json file provided by Divya. It also contains functions for the indexing step. 

#### D. Search Indexing
./build_index.py

Does simple string matching to find apis that contain mentions of the top level library name, and the final method/function name (Eg: "tensorflow" and "Conv2d("). Depending on your needs, it is possible to run on just the library level or just the function level, this would incur different costs because the more indexing you do the less time you'd have to spend on step E. 

#### E. Main Search Function
./main.py

Main search function built on top of Stefanus' work. It uses the index from step (D) to perform the type-matched search. The FQN of the api is first recovered from the input dictionary, and script searches for it in the list of files retrieved as the value from the input dictionary using the FQN as key. The final output for each FQN is written into a textfile at "./results_summaries/<FQN><current time>.txt". Each ouput text contains the file name that was found to contain the API as well as the lines where it was found.  
```
NOTE: this is basically the only component in the pipeline that needs to be changed out to treat projects of other languages. 
```

#### F. Evaluation
./card_sort.py

Script helps with evaluation by randomly choosing 50 apis, processing the corresponding search output from step (E), randomly choosing 10 samples and copying the relevant sample files to a different folder (so you don't have to go searching for them yourself). 
