import base64
import os
import secrets
from pathlib import Path

from authen import auth_request
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
# from fastapi.staticfiles import StaticFiles
from starlette.staticfiles import StaticFiles
from function import create_directory
from PIL import Image
from pydantic import BaseModel

from starlette.requests import Request
router_general = APIRouter()

# static file setup config
router_general.mount("/static", StaticFiles(directory="static"), name="static")
path = "static/"


class Item(BaseModel):
    file_path: str


class base64File(BaseModel):
    file_path: str
    file_name: str


# @app.post("/test")
# async def my_route(request: Request) -> None:
#     print(request.url.path)
#     return request.base_url._url


@router_general.post("/upload/image")
async def create_upload(request: Request, resize: int = 0, file: UploadFile = File(...), authenticated: bool = Depends(auth_request)):
    # FILEPATH = "./static/images/"
    FILEPATH = create_directory("static/photos/")
    filename = file.filename
    # extension = filename.split(".")[1]
    extension = filename.split(".").pop()
    if extension.lower() not in ["png", "jpg", "jpeg"]:
        raise HTTPException(
            status_code=404, detail="File extention not allowed")

    token_name = secrets.token_hex(10)+"."+extension
    generated_name = FILEPATH + token_name

    file_content = await file.read()
    with open(generated_name, "wb") as file:
        file.write(file_content)
    # PILLOW
    img = Image.open(generated_name)
    if resize > 0:
        img = img.resize(size=(200, 200))
    img.save(generated_name)

    file.close()
    # ตัด static ออกเพื่อให้ url ภายนอกปลอดภัยยิ่งขึ้น
    base_system_url = request.base_url._url
    use_path = str(generated_name.strip("static/"))

    file_path = base_system_url + "general/render/?file_path=" + use_path
    return {'file_name': token_name, 'file_path': use_path, "file_url": file_path}


@router_general.post("/upload/file")
async def create_upload(request: Request, file: UploadFile = File(...), authenticated: bool = Depends(auth_request)):
    # FILEPATH = "./static/images/"
    FILEPATH = create_directory("static/files/")
    filename = file.filename
    # extension = filename.split(".")[1]
    extension = filename.split(".").pop()
    if extension.lower() not in ["pdf", "docx", "doc"]:
        raise HTTPException(
            status_code=404, detail="File extention not allowed")

    token_name = secrets.token_hex(10)+"."+extension
    generated_name = FILEPATH + token_name

    file_content = await file.read()
    with open(generated_name, "wb") as file:
        file.write(file_content)
    # PILLOW
    # img = Image.open(generated_name)
    # img.save(generated_name)

    file.close()
    # ตัด static ออกเพื่อให้ url ภายนอกปลอดภัยยิ่งขึ้น
    base_system_url = request.base_url._url
    use_path = str(generated_name.strip("static/"))
    file_path = base_system_url + "general/render/?file_path=" + use_path
    return {'file_name': token_name, 'file_path': use_path, "file_url": file_path}


@router_general.get("/render/")
async def get_file(file_path: str):

    if file_path == "" or file_path == None:
        raise HTTPException(
            status_code=404, detail="message': 'File not found!")
    use = os.path.join(path, file_path)
    if os.path.exists(use):
        return FileResponse(use)
    return {'message': 'File not found!'}


@router_general.delete("/remove/")
async def delete_file(file_path: str, authenticated: bool = Depends(auth_request)):
    use = os.path.join(path, file_path)
    if os.path.exists(use):
        file_to_rem = Path(use)
        file_to_rem.unlink()
        return {'message': 'Delete file success'}
    else:
        # print("The file does not exist")
        return {'message': 'The file does not exist'}


@router_general.post("/base64tofile/")
async def create_file(request: base64File, requestAgent: Request):
    FILEPATH = create_directory("static/")
    file_name = request.file_name
    img_data = request.file_path
    generated_name = FILEPATH + file_name
    decoded_data = base64.b64decode((img_data))
    # write the decoded data back to original format in  file
    img_file = open(str(generated_name), 'wb')
    img_file.write(decoded_data)
    img_file.close()

    # ตัด static ออกเพื่อให้ url ภายนอกปลอดภัยยิ่งขึ้น
    base_system_url = requestAgent.base_url._url
    use_path = str(generated_name.strip("static/"))
    file_path = base_system_url + "general/render/?file_path=" + use_path
    return {'file_name': file_name, 'file_path': use_path, "file_url": file_path}
