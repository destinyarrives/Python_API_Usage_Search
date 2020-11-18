from pathlib import Path
import os
import pandas as pd

PYTHON_FILES_TOTAL, FILES_CONTAINING_API_TOTAL, API_USAGE_TOTAL = 0, 0, 0
APISTATS = {}

def extract():
    try:
        global PYTHON_FILES_TOTAL
        global FILES_CONTAINING_API_TOTAL
        global API_USAGE_TOTAL
        global APISTATS
    except:
        pass

    p = Path.cwd()/"result_summaries"
    for subdir, dirs, files in os.walk(p):
        for filename in files:
            if filename.split(".")[-1] != "txt":
                continue
            with open(str(p) + os.sep + filename, "r") as f:
                result = f.read()
                if not result:
                    continue
                result = result.split("***Python files evaluated in total: ")[1]
                python, result = result.split("\n***Total files containing the API: ")
                files, result = result.split("\n***Total API usage count: ")
                api, result = result.split("\n\n***Time taken: ")

                PYTHON_FILES_TOTAL += int(python)
                FILES_CONTAINING_API_TOTAL += int(files)
                API_USAGE_TOTAL += int(api)

                api_name = filename.split("_November")[0]
                APISTATS[api_name] = (python, files, api)

if __name__ == "__main__":
    extract()
    df = pd.DataFrame.from_dict(APISTATS, orient = "index", columns = ["py files evaluated", "file count", "api count"])
    df.to_csv("summary_results.csv")
