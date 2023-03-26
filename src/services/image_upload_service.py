from genericpath import isdir
import os
from werkzeug.utils import secure_filename
from datetime import datetime


class ImageUploadService:
    def __init__(self):
        pass

    def __format_int(self, number: int):
        if len(f'{number}') < 2:
            return f'0{number}'
        return str(number)

    def __verify_dir(self, dir: str):
        if not os.path.isdir(dir):
            os.mkdir(dir)

    def mount_filename(self):
        now = datetime.now()
        year = self.__format_int(now.year)
        month = self.__format_int(now.month)
        day = self.__format_int(now.day)
        hour = self.__format_int(now.hour)
        minute = self.__format_int(now.minute)
        second = self.__format_int(now.second)
        return f'{year}{month}{day}{hour}{minute}{second}'

    def save(self, image, entity_id, bucket_name: str):
        filename = self.mount_filename()
        ext = secure_filename(image.filename).split('.')[-1]
        filename = f'{filename}-{entity_id}.{ext}'
        relative_path = f'./upload/{bucket_name}'
        self.__verify_dir(relative_path)
        image.save(os.path.join(relative_path, filename))
        full_path = os.path.abspath(relative_path)
        return f'http://localhost:5001/image/{bucket_name}/{filename}'
        # return f'{full_path}/{filename}'
