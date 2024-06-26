import json


def count_links(file_name) -> int:
    with open(file_name, 'r') as file:
        data = file.read()
        json_data = json.loads(data)
        return len(json_data)
