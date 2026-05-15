import os
import uuid
import re
from helpers.config import get_settings , Settings


class BaseController:
    def __init__(self):
        self.app_settings = get_settings()
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.file_dir = os.path.join(self.base_dir , "assets" , "uploads")
        os.makedirs(self.file_dir , exist_ok=True)

    def clean_filename(self , org_filename: str) -> str:
        # 1. normalize
        filename = os.path.basename(org_filename)  # avoid path traversal

        # 2. strip + lowercase
        filename = filename.strip().lower()

        # 3. clean invalid chars
        filename = re.sub(r'[^a-z0-9_.-]', '_', filename)

        # 4. split name + ext
        name, ext = os.path.splitext(filename)

        # 5. avoid empty names
        if not name:
            name = "file"

        # 6. add uniqueness (important in production)
        unique_id = uuid.uuid4().hex[:12]

        return f"{name}_{unique_id}{ext}"
