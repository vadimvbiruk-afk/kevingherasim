"""Upload image to Cloudinary; returns public URL or None if not configured or error."""

import os

def upload_image(file_storage):
    """
    Upload file to Cloudinary. Returns the secure URL string or None.
    Requires env: CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET.
    """
    if not file_storage or not file_storage.filename:
        return None
    cloud_name = os.environ.get("CLOUDINARY_CLOUD_NAME")
    api_key = os.environ.get("CLOUDINARY_API_KEY")
    api_secret = os.environ.get("CLOUDINARY_API_SECRET")
    if not all([cloud_name, api_key, api_secret]):
        return None
    try:
        import cloudinary
        import cloudinary.uploader
        cloudinary.config(
            cloud_name=cloud_name,
            api_key=api_key,
            api_secret=api_secret,
        )
        try:
            file_storage.stream.seek(0)
        except Exception:
            pass
        result = cloudinary.uploader.upload(
            file_storage.stream,
            resource_type="image",
        )
        return result.get("secure_url")
    except Exception:
        return None
