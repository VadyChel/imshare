from pydantic import BaseModel


class File(BaseModel):
    id: int
    filename: str
    name: str
    uploaded_by: str

    class Config:
        orm_mode = True


class FileUpload(BaseModel):
    filename: str
    name: str
    uploaded_by: str


class CreatedFile(BaseModel):
    filename: str