# DeepHarvest Python Project
The high-level goal of this project is to create a set of functions which, when given two inputs 1. a set of projects and 2. a set of APIs we're interested in, creates output: search results of where APIs we're interested in (2) appear in the set of projects (1). 

## Setup/Requirements

- Python 3.6 and up
- Use the desired package manager (pip or conda) to install from requirements.txt. 


## Workflow
The general workflow for the project is as follows: (A) find engineered python projects -> (B) clone these projects -> (C) obtain a list of apis we're interested in and process them in the appropriate manner -> (D) first build an index of candidate matches to perform search on, this might require two passes through every flie in step B -> (E) using the index from step D run the type matching function to obtain final search results -> (F) manually check the returned results to see if the matching was accurate and compute avg accuracy. 

#### A. Finding Engineered Projects
./scraping/gh_scaper.py



#### B. Cloning Projects
```
android.app.Notification.Builder#addAction(android.app.Notification.Action)
```
#### C. API Json Processing
```
android.app.Notification.Builder#addAction(int, java.lang.CharSequence, android.app.PendingIntent)
```
#### D. Search Indexing
```
android.os.Vibrator#vibrate(long)&android.location.LocationManager#removeGpsStatusListener(android.location.GpsStatus.Listener)
```
#### E. Main Search Function
#### F. Evaluation



## Developer Mark 
**Note** that this apps is already tested on Ubuntu and Mac OS. Unfortunately, this doesn't work well on Microsoft shell because of the multi-threading part. Don't worry, we still find the solution for this. If you find a problem while using this apps, please notify me via [this](mhilmia@smu.edu.sg) email. I will help you soon to ensure that you can try this amazing apps immediately :). 
