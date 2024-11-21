from fastapi import HTTPException

# 아이템 유효성 검사 함수
def validate_item_exists(item_id: int, fake_db: dict):
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return fake_db[item_id]

# 새로운 아이템 ID 생성
def generate_new_id(fake_db: dict):
    return len(fake_db) + 1
