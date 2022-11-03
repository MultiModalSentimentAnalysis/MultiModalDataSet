import sys
import csv
import json
from pathlib import Path
sys.path.append(str(Path(".").resolve()))
from settings import LABEL_STUDIO_URL, API_KEY, LABELSTUDIO_DIR

# Import the SDK and the client module
from label_studio_sdk import Client

# Connect to the Label Studio API and check the connection
ls = Client(url=LABEL_STUDIO_URL, api_key=API_KEY)
ls.check_connection()

template = ''.join(open(LABELSTUDIO_DIR / "template.xml").readlines())

project = ls.start_project(
    title='MMDS',
    label_config=template
)

json_array = []
with open("label-studio/label_studio_input.csv", newline='\n') as csvf:
    csvReader = csv.DictReader(csvf) 
    for row in csvReader: 
        json_array.append(row)

json_string = json.dumps(json_array, indent=4)
# print(json_string)

project.import_tasks(json_array)