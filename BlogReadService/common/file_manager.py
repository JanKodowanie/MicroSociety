import shutil
import settings
import os
from .exceptions import *
from fastapi import UploadFile
from typing import List, Tuple, Optional


class FileManager:
    
    def upload_file(self, _file: UploadFile, 
                    filename: Optional[str], directory: str, extensions = List[str]) -> Tuple[str, str]:
        try:
            ext = self.validate_file(_file, extensions)
        except InvalidFileExtension as e:
            raise e
            
        if not filename:
            filename = _file.filename.split('.')[0]
            
        abs_directory = '/'.join([settings.MEDIA_DIR, directory])
        if not os.path.exists(abs_directory):
            os.mkdir(abs_directory)
            
        path = '/'.join([abs_directory, f'{filename}.{ext}'])
        url = '/'.join([settings.MEDIA_ROOT, directory, f'{filename}.{ext}'])
        
        with open(path, 'wb') as buffer:
                shutil.copyfileobj(_file.file, buffer)
                
        return path, url
                
    def delete_file(self, path: str):
        if path:
            if os.path.exists(path):
                os.remove(path)
                
    def validate_file(self, _file: UploadFile, extensions = List[str]) -> str:
        try:
            ext = _file.filename.split('.')[1]
        except Exception:
            raise InvalidFileExtension('Plik nie posiada rozszerzenia.')
    
        if ext not in extensions:
            raise InvalidFileExtension(
                'Nieprawidłowe rozszerzenie pliku. Dozwolone rozszerzenia: ' + ', '.join(extensions))
            
        return ext