import shutil
import settings
import os
from .exceptions import *
from fastapi import UploadFile
from typing import List, Tuple


class FileManager:
    
    def upload_file(self, _file: UploadFile, 
                    filename: str, directory: str, extensions = List[str]) -> Tuple[str, str]:
        try:
            ext = _file.filename.split('.')[1]
        except Exception:
            raise InvalidFileExtension('Uploaded file has no extension')
    
        if ext not in extensions:
            raise InvalidFileExtension(
                'Invalid file extension. Allowed extensions: ' + ', '.join(extensions))
            
        abs_directory = '/'.join([settings.MEDIA_DIR, directory])
        if not os.path.exists(abs_directory):
            os.mkdir(abs_directory)
            
        path = '/'.join([abs_directory, f'{filename}.{ext}'])
        url = '/'.join([settings.MEDIA_ROOT, directory, f'{filename}.{ext}'])
        
        with open(path, 'wb') as buffer:
                shutil.copyfileobj(_file.file, buffer)
                
        return path, url
                
    def delete_file(self, path: str):
        if os.path.exists(path):
            os.remove(path)