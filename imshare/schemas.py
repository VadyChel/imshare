from pydantic import BaseModel


class ImageInResponse(BaseModel):
    id: int
    filename: str
    name: str
    uploaded_by: str

    class Config:
        orm_mode = True


class ImageInRequest(BaseModel):
    filename: str
    name: str
    uploaded_by: str