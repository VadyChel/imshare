import typing

from fastapi import HTTPException
from sqlalchemy.orm import Session
from . import models, schemas


def add_image(db: Session, image: schemas.ImageInRequest) -> schemas.ImageInResponse:
    db_image = models.Image(**image.dict())
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image


def delete_image(db: Session, name: str, api_key: str):
    deleted_image = get_image(db=db, name=name)
    if deleted_image is None:
        raise HTTPException(status_code=404, detail='File not found')

    if deleted_image.uploaded_by != api_key:
        raise HTTPException(status_code=403, detail="You don't an owner of file")

    db.query(models.Image).filter(models.Image.name == name).delete()
    db.commit()
    return deleted_image


def get_image(db: Session, name: str) -> schemas.ImageInResponse:
    return db.query(models.Image).filter(models.Image.name == name).first()


def get_api_keys(db: Session) -> typing.List[str]:
    return [item.api_key for item in db.query(models.ApiKey).all()]


def get_images_names(db: Session) -> typing.List[str]:
    return [item.name for item in db.query(models.Image).all()]
