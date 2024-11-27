import pytest
import httpx

BASE_URL = "http://127.0.0.1:8000"

@pytest.mark.asyncio
async def test_get_paper_by_doi():
    """Test: GET /papers"""
    paper_doi = "10.1234/example"
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/papers", params={"paperDoi": paper_doi})
    assert response.status_code == 200
    print("GET /papers response:", response.json())


@pytest.mark.asyncio
async def test_get_prior_papers():
    """Test: GET /papers/priorpapers"""
    paper_doi = "10.1234/example"
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/papers/priorpapers", params={"paperDoi": paper_doi})
    assert response.status_code == 200
    print("GET /papers/priorpapers response:", response.json())


@pytest.mark.asyncio
async def test_create_paper_summary():
    """Test: POST /papers/summary"""
    payload = {"paperDoi": "10.18653/v1/2020.acl-demos.1"}
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/papers/summary", json=payload)
    assert response.status_code == 200
    print("POST /papers/summary response:", response.json())


@pytest.mark.asyncio
async def test_create_paper_transformation():
    """Test: POST /papers/transformation"""
    payload = {"userPrompt": "한국어 사용자 프롬프트"}
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/papers/transformation", json=payload)
    assert response.status_code == 200
    print("POST /papers/transformation response:", response.json())


@pytest.mark.asyncio
async def test_search_papers():
    """Test: POST /papers/search"""
    payload = {"userKeyword": "한국어 사용자 키워드"}
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/papers/search", json=payload)
    assert response.status_code == 200
    print("POST /papers/search response:", response.json())

@pytest.mark.asyncio
async def test_get_user_bookmarks():
    """Test: GET /users/bookmarks"""
    user_id = 1
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/users/bookmarks", params={"userId": user_id})
    assert response.status_code == 200
    print("GET /users/bookmarks response:", response.json())


@pytest.mark.asyncio
async def test_add_to_bookmarks():
    """Test: POST /users/bookmarks"""
    payload = {"userId": 1, "paperDoi": "10.1234/example"}
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/users/bookmarks", json=payload)
    assert response.status_code == 200
    print("POST /users/bookmarks response:", response.json())


@pytest.mark.asyncio
async def test_remove_from_bookmarks():
    """Test: DELETE /users/bookmarks"""
    params = {"userId": 1, "paperDoi": "10.1234/example"}
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{BASE_URL}/users/bookmarks", params=params)
    assert response.status_code == 200
    print("DELETE /users/bookmarks response:", response.json())
