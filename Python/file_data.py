import os
from datetime import datetime

UNKNOWN = 'unknown'
FILE_TYPE_MAP = {
    'image': ['jpg', 'png', 'tif'],
    'video': ['mp4', 'mkv'],
    'script': ['py', 'ps1', 'cs'],
    'blend': ['blend'],
    'photoshop': ['psd'],
}


class FileData():

    def __init__(self, file_path):
        self.file_name = os.path.basename(file_path)
        self.file_type = UNKNOWN
        if os.path.isfile(file_path):
            if len(os.path.basename(file_path).split('.')) > 1:
                file_ext = os.path.basename(file_path).split('.')[1]
                for k, v in FILE_TYPE_MAP.items():
                    if file_ext in v:
                        self.file_type = k
                        break
        self.date_modified = os.path.getmtime(file_path)

    def __getitem__(self, item):
        if item == 0:
            return self.file_name
        elif item == 1:
            return self.file_type
        elif item == 2:
            return datetime.utcfromtimestamp(self.date_modified).strftime('%Y-%m-%d %H:%M:%S')