from pathlib import Path

def extract():
    stats_of_apis = {}
    python_files_total, files_containing_api_total, api_usage_total = 0, 0, 0
    p = Path.cwd()/"result_summaries"
    for subdir, dirs, files in os.walk(p):
        for filename in files:
            with open(str(p) + os.sep + filename, "r") as f:
                result = f.read()
                result = result.split("***Python files evaluated in total: ")[1]
                python, result = result.split("\n***Total files containing the API: ")
                files, result = result.split("\n***Total API usage count: ")
                api, result = result.split("\n\n***Time taken: ")

                python_files_total += python
                files_containing_api_total += files
                api_usage_total += api
                stats_of_apis[]