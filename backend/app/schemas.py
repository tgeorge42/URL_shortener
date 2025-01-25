from pydantic import BaseModel

class ShortenedURLBase(BaseModel):
    original_url: str

class ShortenedURLCreate(ShortenedURLBase):
    pass

class ShortenedURLResponse(ShortenedURLBase):
    id: int
    short_code: str
    title: str

    class Config:
        orm_mode = True
