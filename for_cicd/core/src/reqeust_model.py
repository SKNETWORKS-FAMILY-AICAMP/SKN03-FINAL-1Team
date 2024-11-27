from pydantic import BaseModel


class userKeyword(BaseModel):
    userKeyword: str | None = None

class userPrompt(BaseModel):
    userPrompt: str | None = None


class paperDoi(BaseModel):
    paperDoi: str | None = None

class bookMark(BaseModel):
    paperDoi: str 
    userKeyword : str
    bookMark : bool
