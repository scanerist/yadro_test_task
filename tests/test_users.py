import pytest
from unittest.mock import patch, AsyncMock
from app.users.services import fetch_random_users, get_user, get_random_user, create_user
from app.users.schemas import UserCreate
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

@pytest.mark.asyncio
@patch("app.users.services.httpx.AsyncClient")
async def test_fetch_random_users(mock_async_client):
    mock_client_instance = mock_async_client.return_value.__aenter__.return_value
    mock_response = AsyncMock()
    mock_response.json = AsyncMock(return_value={
        "results": [
            {
                "gender": "male",
                "name": {"first": "John", "last": "Doe"},
                "phone": "1234567890",
                "email": "john@example.com",
                "location": {"country": "USA", "city": "New York"},
                "picture": {"thumbnail": "http://example.com/photo.jpg"}
            }
        ]
    })
    mock_response.raise_for_status.return_value = None
    mock_client_instance.get.return_value = mock_response

    users = await fetch_random_users(1)
    assert users[0]["email"] == "john@example.com"

@pytest.mark.asyncio
@patch("app.users.services.httpx.AsyncClient")
async def test_fetch_random_users_external_api(mock_async_client):
    mock_client_instance = mock_async_client.return_value.__aenter__.return_value
    mock_response = AsyncMock()
    mock_response.json = AsyncMock(return_value={
        "results": [
            {
                "gender": "female",
                "name": {"first": "Alice", "last": "Smith"},
                "phone": "555-1234",
                "email": "alice@example.com",
                "location": {"country": "USA", "city": "LA"},
                "picture": {"thumbnail": "http://example.com/alice.jpg"}
            }
        ]
    })
    mock_response.raise_for_status.return_value = None
    mock_client_instance.get.return_value = mock_response

    users = await fetch_random_users(1)
    mock_client_instance.get.assert_called_with(
        "https://randomuser.me/api/", params={"results": 1}
    )
    assert users[0]["email"] == "alice@example.com"
    assert users[0]["name"]["first"] == "Alice"
    assert users[0]["picture"]["thumbnail"] == "http://example.com/alice.jpg"

@pytest.mark.asyncio
async def test_get_user_found(monkeypatch):
    class DummyUser:
        id = 1
        gender = "male"
        first_name = "John"
        last_name = "Doe"
        phone = "1234567890"
        email = "john@example.com"
        location = "USA, New York"
        picture = "http://example.com/photo.jpg"
    class DummyResult:
        def scalar_one_or_none(self):
            return DummyUser()
    class DummyDB:
        async def execute(self, *a, **kw):
            return DummyResult()
    dummy_db = DummyDB()
    user = await get_user(dummy_db, 1)
    assert user.email == "john@example.com"

@pytest.mark.asyncio
async def test_get_user_not_found(monkeypatch):
    async def dummy_get_user(db, user_id):
        return None
    monkeypatch.setattr("app.users.dao.get_user", dummy_get_user)
    class DummyResult:
        def scalar_one_or_none(self):
            return None
    class DummyDB:
        async def execute(self, *a, **kw):
            return DummyResult()
    dummy_db = DummyDB()
    user = await get_user(dummy_db, 999)
    assert user is None

@pytest.mark.asyncio
async def test_get_random_user(monkeypatch):
    class DummyUser:
        id = 2
        gender = "female"
        first_name = "Jane"
        last_name = "Smith"
        phone = "9876543210"
        email = "jane@example.com"
        location = "USA, Boston"
        picture = "http://example.com/photo2.jpg"
    class DummyResult:
        def scalar_one_or_none(self):
            return DummyUser()
    async def dummy_get_random_user(db):
        return DummyUser()
    monkeypatch.setattr("app.users.dao.get_random_user", dummy_get_random_user)
    class DummyDB:
        async def execute(self, *a, **kw):
            return DummyResult()
    dummy_db = DummyDB()
    user = await get_random_user(dummy_db)
    assert user.email == "jane@example.com"

@pytest.mark.asyncio
async def test_create_user_unique(monkeypatch):
    class DummyUser:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)
    async def dummy_create_user(db, user):
        if user.email == "exists@example.com":
            raise Exception("IntegrityError")
        return DummyUser(**user.dict())
    monkeypatch.setattr("app.users.dao.create_user", dummy_create_user)
    user_data = UserCreate(
        gender="male",
        first_name="Test",
        last_name="User",
        phone="0000000000",
        email="unique@example.com",
        location="Testland",
        picture="http://example.com/test.jpg"
    )
    class DummyDB:
        def add(self, obj): pass
        async def commit(self): pass
        async def refresh(self, obj): pass
        async def rollback(self): pass
    dummy_db = DummyDB()
    user = await create_user(dummy_db, user_data)
    assert user.email == "unique@example.com" 