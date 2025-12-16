import cloudinary
import cloudinary.uploader
import os
import uuid



cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
)



async def upload_profile_image(file):
    result = cloudinary.uploader.upload(
        file.file,
        folder="profiles",
        public_id=str(uuid.uuid4()),
        resource_type="image",
        overwrite=True
    )
    return result["secure_url"]


# # Helper to upload to Cloudinary
# async def upload_to_cloudinary(file: UploadFile,user_id:int) -> str:
#     file_content = await file.read()  # Read file bytes
#     result = cloudinary.uploader.upload(
#         file_content,
#         folder="profileImages_hr",
#         public_id=f"user_{user_id}",   # 🔑 fixed ID
#         overwrite=True,     # optional folder
#         resource_type="image"
#     )
#     return result.get("secure_url")  # URL to store in DB