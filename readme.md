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

#### D. Search Indexing
```
android.os.Vibrator#vibrate(long)&android.location.LocationManager#removeGpsStatusListener(android.location.GpsStatus.Listener)
```
#### E. Main Search Function
#### F. Evaluation



## Developer Mark 
**Note** that this apps is already tested on Ubuntu and Mac OS. Unfortunately, this doesn't work well on Microsoft shell because of the multi-threading part. Don't worry, we still find the solution for this. If you find a problem while using this apps, please notify me via [this](mhilmia@smu.edu.sg) email. I will help you soon to ensure that you can try this amazing apps immediately :). 
