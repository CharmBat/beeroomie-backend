from fastapi import APIRouter, File, UploadFile
from services.PhotoHandle import PhotoHandleService


router = APIRouter(tags=["PhotoHandle"])

@router.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    return PhotoHandleService.photo_upload_service(file)