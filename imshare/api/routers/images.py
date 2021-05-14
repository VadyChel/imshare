import os
import uuid

from fastapi import APIRouter, Depends, File, Header, HTTPException, Request
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from aiofile import async_open

from imshare import crud, schemas
from imshare.api import dependencies

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
    db: Session = Depends(dependencies.get_db)
):
    if len(name) > 32:
        raise HTTPException(status_code=400, detail='Too long filename')

    if len(file) > 500000:
        raise HTTPException(status_code=400, detail='File too long. Over 500kb')

    if filetype.lower() not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail='Unknown file type')

    if authorization not in crud.get_api_keys(db=db):
        raise HTTPException(status_code=403, detail='Invalid api key was provided')

    if name in crud.get_images_names(db=db):
        raise HTTPException(status_code=400, detail='This name is already in use')

    filename = str(uuid.uuid4())+CONTENT_TYPE_TO_FILETYPE[filetype]
    crud.add_image(db=db, image=schemas.ImageInRequest(
        filename=filename, name=name, uploaded_by=authorization
    ))

    async with async_open(f'imshare/files/{filename}', 'wb') as to_write:
        await to_write.write(file)
    return 'OK'


@router.delete('/api/v1/delete')
async def delete_image(
    name: str,
    authorization: str = Header(None),
    db: Session = Depends(dependencies.get_db)
):
    if len(name) > 32:
        raise HTTPException(status_code=400, detail='Too long filename')

    db_image = crud.delete_image(db=db, name=name, api_key=authorization)
    os.remove(f'imshare/files/{db_image.filename}')
    return 'OK'


@router.get('/{name}')
async def get_image(request: Request, name: str, db: Session = Depends(dependencies.get_db)):
    db_image = crud.get_image(db=db, name=name)
    if db_image is None:
        raise HTTPException(status_code=404, detail='File not found')

    path = f'imshare/files/{db_image.filename}'
    if db_image.filename.endswith('.txt'):
        async with async_open(path, 'r') as f:
            lines = (await f.read()).splitlines()

        return templates.TemplateResponse('file_preview.html', {
            'request': request, 'lines': lines, 'enumerate': enumerate, 'filename': db_image.name
        })

    return FileResponse(path)