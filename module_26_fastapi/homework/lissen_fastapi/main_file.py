from typing import Annotated

from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}


"""
File - это класс, который наследуется непосредственно от Form.

Но помните, что когда вы импортируете Query, Path, File и другие из fastapi, на самом деле это функции, 
которые возвращают специальные классы.
"""


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}


"""
Для объявления тела файла необходимо использовать File, поскольку в противном случае параметры будут интерпретироваться 
как параметры запроса или параметры тела (JSON).
"""