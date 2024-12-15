from fastapi import APIRouter, File, UploadFile
from services.PhotoUpload import PhotoUploadService


router = APIRouter(tags=["PhotoUpload"])

@router.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    return PhotoUploadService.photo_upload_service(file)