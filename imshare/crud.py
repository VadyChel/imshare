from fastapi import HTTPException
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from . import models, schemas


async def add_file(db: AsyncSession, image: schemas.FileUpload) -> schemas.File:
    db_file = models.File(**image.dict())
    db.add(db_file)
    await db.commit()
    await db.refresh(db_file)
    return db_file


async def delete_file(db: AsyncSession, name: str, api_key: str):
    deleted_file = await get_file(db=db, name=name)
    if deleted_file is None:
        raise HTTPException(status_code=404, detail='File not found')

    if deleted_file.uploaded_by != api_key:
        raise HTTPException(status_code=403, detail="You don't an owner of file")

    await db.execute(delete(models.File).where(models.File.name == name))
    await db.commit()
    return deleted_file


async def get_file(db: AsyncSession, name: str) -> schemas.File | None:
    resp = await db.execute(select(models.File).where(models.File.name == name))
    if (resp_first := resp.first()) is None:
        return None

    return resp_first[0]


async def get_api_keys(db: AsyncSession) -> list[str]:
    resp = await db.execute(select(models.ApiKey.api_key))
    return [item[0] for item in resp.all()]


async def get_files_names(db: AsyncSession) -> list[str]:
    resp = await db.execute(select(models.File.name))
    return [item[0] for item in resp.all()]
