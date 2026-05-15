import uuid
import os 
from fastapi import UploadFile

from .base_controller import BaseController
from models.enums import ResponseSignal
from .project_controller import ProjectController

class DataController(BaseController):
    def __init__(self):
        super().__init__()
    
    def validate_file(self, file: UploadFile)   -> tuple[bool, str]:
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False,ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value
        
        if file.size is not None and file.size > self.app_settings.FILE_MAX_SIZE:
            return False , ResponseSignal.FILE_SIZE_EXCEEDED.value
        
        return True, ResponseSignal.FILE_VALIDATION_SUCCESS.value
    

    def generate_unique_filename(self , org_filename : str , project_id : str) -> str:

        project_file_dir = ProjectController().get_project_path(project_id = project_id)
        cleaned_filename = self.clean_filename(org_filename = org_filename)
        new_filepath = os.path.join(project_file_dir , cleaned_filename)

        while  os.path.exists(new_filepath):
            unique_suffix = uuid.uuid4().hex[:8]
            name, ext = os.path.splitext(cleaned_filename)
            new_filename = f"{name}_{unique_suffix}{ext}"
            new_filepath = os.path.join(project_file_dir , new_filename)
        
        return new_filepath

