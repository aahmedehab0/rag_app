from fastapi import APIRouter , Depends , UploadFile , File , status
import logging
import aiofiles

from fastapi.responses import JSONResponse
from helpers.config import get_settings , Settings
from controllers import DataController , ProjectController
from models.enums import ResponseSignal

logger = logging.getLogger('uvicorn.error')
data_router = APIRouter(
    prefix= "/rag",
    tags= ["api_v1"]
    )

@data_router.post("/upload/{project_id}")

async def upload(project_id: str  , file: UploadFile,
                 app_settings : Settings = Depends(get_settings)
                 ): 
    data_controller = DataController()
    project_controller = ProjectController()

    is_valid , response = data_controller.validate_file(file = file)
    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": response})
    
    project_path = project_controller.get_project_path(project_id = project_id)   

    if project_path is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": ResponseSignal.PROJECT_PATH_NOT_FOUND.value})

    file_path = data_controller.generate_unique_filename(
        org_filename = file.filename,               # type: ignore
        project_id = project_id)  
                     
    try:
        async with aiofiles.open(file_path, 'wb') as f:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": ResponseSignal.FILE_UPLOAD_SUCCESS.value})
    
    except Exception as e:
        logger.error(f"Error uploading file: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": ResponseSignal.FILE_UPLOAD_FAILED.value})
