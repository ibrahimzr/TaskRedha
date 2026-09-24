from datetime import datetime
from pydantic import BaseModel,ConfigDict
from app.enums import OrderStatus,Role

class ResponseModel(BaseModel):
    model_config=ConfigDict(from_attributes=True)

class UserResponse(ResponseModel):
    id:int
    username:str
    email:str
    role:Role
    is_active:bool

class TokenResponse(ResponseModel):
    access_token:str
    token_type:str="bearer"

class ChallengeResponse(ResponseModel):
    challenge_token:str
    numbers:list[int]
    expires_in_seconds:int=300

class AuthorSummaryResponse(ResponseModel):
    id:int
    name:str

class BookSummaryResponse(ResponseModel):
    id:int
    title:str

class AuthorProfileResponse(ResponseModel):
    bio:str
    website:str|None

class AuthorResponse(ResponseModel):
    id:int
    name:str
    email:str|None
    profile:AuthorProfileResponse|None
    books:list[BookSummaryResponse]

class AuthorListItemResponse(ResponseModel):
    id:int
    name:str
    book_count:int

class GenreResponse(ResponseModel):
    id:int
    name:str

class BookResponse(ResponseModel):
    id:int
    title:str
    price:float
    stock:int
    author:AuthorSummaryResponse
    genres:list[GenreResponse]

class OrderResponse(ResponseModel):
    id:int
    user_id:int
    book_id:int
    quantity:int
    total_price:float
    status:OrderStatus
    created_at:datetime
    due_at:datetime
    remaining_seconds:int
