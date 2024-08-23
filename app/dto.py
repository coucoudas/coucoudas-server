from pydantic import BaseModel

class CreateBoardRequest(BaseModel):
    title: str
    content: str

class UpdateBoardRequest(BaseModel):
    title: str
    content: str