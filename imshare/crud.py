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
    deleted_file = await get_file_by_name(db=db, name=name, api_key=api_key)
    if deleted_file is None:
        raise HTTPException(status_code=404, detail='File not found')

    if deleted_file.uploaded_by != api_key:
        raise HTTPException(status_code=403, detail="You don't an owner of file")

    await db.execute(delete(models.File).where(models.File.filename == deleted_file.filename))
    await db.commit()
    return deleted_file


async def get_file(db: AsyncSession, filename: str) -> schemas.File | None:
    resp = await db.execute(select(models.File).where(models.File.filename == filename))
    if (resp_first := resp.first()) is None:
        return None

    return resp_first[0]


async def get_file_by_name(db: AsyncSession, name: str, api_key: str) -> schemas.File | None:
    resp = await db.execute(select(models.File).where(
        models.File.name == name,
        models.File.uploaded_by == api_key
    ))
    if (resp_first := resp.first()) is None:
        return None

    return resp_first[0]


async def get_api_keys(db: AsyncSession) -> list[str]:
    resp = await db.execute(select(models.ApiKey.api_key))
    return [item[0] for item in resp.all()]


async def get_files_names(db: AsyncSession, api_key: str) -> list[str]:
    resp = await db.execute(select(models.File.name).where(models.File.uploaded_by == api_key))
    return [item[0] for item in resp.all()]


async def get_files(db: AsyncSession, api_key: str) -> list[schemas.File]:
    resp = await db.execute(select(models.File).where(models.File.uploaded_by == api_key))
    return [item[0] for item in resp.all()]


async def get_api_key_limit(db: AsyncSession, api_key: str) -> int | None:
    resp = await db.execute(select(models.ApiKey.max_file_length).where(models.ApiKey.api_key == api_key))
    if (resp_first := resp.first()) is None:
        return None

    return resp_first[0]
