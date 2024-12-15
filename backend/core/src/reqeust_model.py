from pydantic import BaseModel

# 논문 검색
class paperSearch(BaseModel):
    userKeyword: str | None

# 키워드 최적화
class paperTransformation(BaseModel):
    userPrompt: str | None

# 논문 요약약
class paperSummary(BaseModel):
    paperDoi: str | None
    userKeyword: str | None


class bookMarking(BaseModel):
    paperDoi: str | None
    userKeyword: str | None
    bookMark: bool | None
