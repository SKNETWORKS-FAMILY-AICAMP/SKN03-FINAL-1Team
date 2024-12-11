from pydantic import BaseModel


class userKeyword(BaseModel):
    userKeyword: str | None


class userPrompt(BaseModel):
    userPrompt: str | None


class paperDoi(BaseModel):
    paperDoi: str | None


class bookMarking(BaseModel):
    paperDoi: str | None
    userKeyword: str | None
    bookMark: bool | None
