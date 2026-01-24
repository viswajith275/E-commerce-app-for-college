from fastapi import UploadFile, status, HTTPException
from PIL import Image
import io
import uuid
import os
import shutil
from backend.config import UPLOAD_DIRECTORY, IMAGE_SERVER_ADRESS
from backend.models import ImageValidatorSchema

async def validate_image(file: UploadFile):

    file_size = await file.read()
    await file.seek(0)

    #validation of image (Have to study and might have to rewrite this)
    try:
        ImageValidatorSchema(
            filename=file.filename,
            content_type=file.content_type,
            file_size=len(file_size)
        )
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Image specifications does not match!")

    try:
        image_data = await file.read()
        img = Image.open(io.BytesIO(image_data))
        img.verify()

        await file.seek(0)

    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or corrupted image!")


async def save_image(file: UploadFile):


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
    abs_path = os.path.dirname(os.path.abspath(__file__))
    new_path = os.path.join(abs_path, file_path)

    if os.path.exists(new_path):

        try:
            await os.remove(new_path)
            
        except:

            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Could not delete the image!')
    