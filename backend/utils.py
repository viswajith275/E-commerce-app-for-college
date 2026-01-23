from fastapi import UploadFile, status, HTTPException
from PIL import Image
import io
import uuid
import os
import shutil
from backend.config import MAX_IMAGE_SIZE, UPLOAD_DIRECTORY, IMAGE_SERVER_ADRESS

async def validate_and_save_image(file: UploadFile):

    await file.seek(0,2)
    file_size = file.tell()
    await file.seek(0)

    ALLOWED_TYPES = ["image/jpeg", "image/png"]

    #validation of image (Have to study and might have to rewrite this)
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="The file is not of an allowed datatype!")
    
    if file_size > MAX_IMAGE_SIZE:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"The maximum file size is {MAX_IMAGE_SIZE / (1024 * 1024)} MB")
    
    try:
        image_data = await file.read()
        img = Image.open(io.BytesIO(image_data))
        img.verify()

        await file.seek(0)

    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or corrupted image!")
    
    file_extension = file.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = os.path.join(UPLOAD_DIRECTORY, unique_filename)

    # Open image using Pillow
    try:
        img = Image.open(file.file)
        
        data = list(img.getdata())
        image_without_exif = Image.new(img.mode, img.size)
        image_without_exif.putdata(data)
        

        image_without_exif.save(file_path)
    except Exception:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    return f"{IMAGE_SERVER_ADRESS}/static/images/{unique_filename}"