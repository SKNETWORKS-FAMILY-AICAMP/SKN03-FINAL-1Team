from pydantic import BaseModel


class userKeyword(BaseModel):
    userKeyword: str 

class userPrompt(BaseModel):
    userPrompt: str 


class paperDoi(BaseModel):
    paperDoi: str 
    
class bookMarking(BaseModel):
    paperDoi: str
    userKeyword : str
    bookmark : bool
