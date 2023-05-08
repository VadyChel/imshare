import os
import uuid

import aiofiles
from fastapi import APIRouter, Depends, File, Header, HTTPException, Request, Response
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from imshare import crud, schemas
from imshare.api import dependencies
from imshare.config import config

router = APIRouter()
templates = Jinja2Templates(directory="imshare/templates")
ALLOWED_TYPES = (
    'image/png',
    'image/jpeg',
    'image/gif',
    'text/plain'
)
CONTENT_TYPE_TO_FILETYPE = {
    'image/png': '.png',
    'image/jpeg': '.jpeg',
    'image/gif': '.gif',
    'text/plain': '.txt'
}


@router.post('/api/v1/upload')
async def upload_image(
    filetype: str,
    name: str,
    file: bytes = File(...),
    authorization: str = Header(None),
    db: AsyncSession = Depends(dependencies.get_db)
):
    if len(name) > config.max_name_length:
        raise HTTPException(status_code=400, detail='Too long filename')

    if len(file) > config.max_file_length:
        raise HTTPException(status_code=400, detail='File too long. Over 500kb')

    if filetype.lower() not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail='Unknown file type')

    if authorization not in await crud.get_api_keys(db=db):
        raise HTTPException(status_code=403, detail='Invalid api key was provided')

    if name in await crud.get_files_names(db=db):
        raise HTTPException(status_code=400, detail='This name is already in use')

    filename = str(uuid.uuid4())+CONTENT_TYPE_TO_FILETYPE[filetype]
    await crud.add_file(db=db, image=schemas.FileUpload(
        filename=filename, name=name, uploaded_by=authorization
    ))

    async with aiofiles.open(f'imshare/files/{filename}', mode="wb") as f:
        await f.write(file)

    return Response(status_code=201)


@router.delete('/api/v1/delete')
async def delete_file(
    name: str,
    authorization: str = Header(None),
    db: AsyncSession = Depends(dependencies.get_db)
):
    if len(name) > config.max_file_length:
        raise HTTPException(status_code=400, detail='Too long filename')

    db_file = await crud.delete_file(db=db, name=name, api_key=authorization)
    os.remove(f'imshare/files/{db_file.filename}')
    return Response(status_code=201)


@router.get('/{name}')
async def get_image(request: Request, name: str, db: AsyncSession = Depends(dependencies.get_db)):
    db_file = await crud.get_file(db=db, name=name)
    if db_file is None:
        raise HTTPException(status_code=404, detail='File not found')

    path = f'imshare/files/{db_file.filename}'
    if db_file.filename.endswith('.txt'):
        async with aiofiles.open(path, mode="r") as f:
            lines = await f.read()
            lines = lines.splitlines()

        return templates.TemplateResponse('file_preview.html', {
            'request': request, 'lines': lines, 'enumerate': enumerate, 'filename': db_file.name
        })

    return FileResponse(path)