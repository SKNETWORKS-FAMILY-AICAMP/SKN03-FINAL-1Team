from pydantic import BaseModel

class userKeyword(BaseModel):
    userKeyword: str | None = None
    