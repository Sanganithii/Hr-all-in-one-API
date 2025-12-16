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
    return  {"uuid": result["public_id"],   "secure_url": result["secure_url"]}

async def delete_profile_image(public_id: str):
    cloudinary.uploader.destroy(
        public_id,
        resource_type="image"
    )
