import json, os
from constants import DATA_FOLDER

def load_file(file_name):
    file_path = os.path.join(DATA_FOLDER, file_name)
    return json.load(open(file_path))


def test_load_file():
    from pprint import pprint 

    file_name = "__utah-businesses-for-sale__3__.json"
    results = load_file(file_name)
    pprint(results)


if __name__ == "__main__":

    test_load_file()
