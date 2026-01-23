from fastapi import UploadFile, status, HTTPException
from PIL import Image
import io
import uuid
import os
import shutil
from backend.config import UPLOAD_DIRECTORY, IMAGE_SERVER_ADRESS
from backend.models import ImageValidatorSchema

async def validate_image(file: UploadFile):

    await file.seek(0,2)
    file_size = file.tell()
    await file.seek(0)

    #validation of image (Have to study and might have to rewrite this)
    try:
        ImageValidatorSchema(
            filename=file.filename,
            content_type=file.content_type,
            file_size=file_size
        )
    except ValueError as e:
        # Pydantic raises ValueError, we convert to HTTP exception
        raise HTTPException(status_code=400, detail=str(e))

    try:
        image_data = await file.read()
        img = Image.open(io.BytesIO(image_data))
        img.verify()

        await file.seek(0)

    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or corrupted image!")
    
    return True

async def validate_and_save_image(file: UploadFile):

    if await validate_image(file):

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

        return f"{IMAGE_SERVER_ADRESS}/{UPLOAD_DIRECTORY}/{unique_filename}"



async def delete_images(file_path: str):

    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            
        except:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Could not delete the image!')
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="image is corrupted or deleted")