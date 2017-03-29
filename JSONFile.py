import json
import os
from pprint import pprint

class JSONFile(object):
    def __init__(self, file_path):
        self.file_name = os.path.basename(file_path)
        self.file_path = file_path
        self._file_ref = open(file_path, "r+")
        self.open = True

    def read_file(self):
        return json.load(self._file_ref)

    def write_to_file(self, data):
        if not self.open:
            raise ValueError("File is already closed")
        self._file_ref.seek(0)
        json.dump(data, self._file_ref)

    def close_file(self):
        self._file_ref.close()
        self.open = False
