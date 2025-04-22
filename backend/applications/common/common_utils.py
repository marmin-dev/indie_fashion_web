import json

# Json 파일 읽기
def load_json_data(filename):
    with open(filename) as json_file:
        return json.load(json_file)