import cloudinary
import cloudinary.uploader
from PIL import Image
import uuid
from fastapi import UploadFile, File, status
from config import CLOUDINARY_API_KEY,CLOUDINARY_API_SECRET,CLOUDINARY_NAME
from utils.PhotoHandle import create_response


class PhotoUploadService:
    cloudinary.config(
    cloud_name=CLOUDINARY_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET,
    secure=True)
    
    @staticmethod
    def photo_upload_service(file: UploadFile = File(...)):
            # Validate file type
        if file.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
            return create_response(
                user_message="Invalid file type. Please upload a valid image file",
                error_status=status.HTTP_400_BAD_REQUEST,
                system_message="Invalid file type"
            )
        
        try:
            # Open the image 
            image = Image.open(file.file)
            image.verify()  # Ensure it's a valid image
            
            # Generate unique public ID
            public_id = f"image_{uuid.uuid4()}"
            
            file.file.seek(0)
            
            # Upload to Cloudinary
            upload_result = cloudinary.uploader.upload(
                file.file,
                public_id=public_id,
                folder="uploads" # Buraya pp ya da advertisement yazılabilir

            )
            
            return create_response(
                photoUrl=upload_result["secure_url"],
                user_message="Image uploaded successfully",
                error_status=status.HTTP_201_CREATED,
                system_message="OK"
            )
        
        except Exception as e:
            return create_response(
                user_message="Failed to upload image",
                error_status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                system_message=str(e)
            )