from schemas.PhotoHandle import PhotoUploadResponse

def create_response( user_message: str, error_status: int, system_message: str,photoUrl: str = None):
    return PhotoUploadResponse(
        photoUrl=photoUrl,
        user_message=user_message,
        error_status=error_status,
        system_message=system_message
    )

