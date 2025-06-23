import pytest
from httpx import AsyncClient
import logging

logger = logging.getLogger(__name__)


@pytest.mark.parametrize("username, email, password, status_code", [
    ("John", "john@gmail.com", "qwerty", 200),
])
async def test_register_user(username, email, password, status_code, ac_client: AsyncClient):
    response = await ac_client.post("/api/v1/register", json={
        "username": username,
        "email": email,
        "password": password
    })
    assert response.status_code == status_code

@pytest.fixture
async def auth_ac_client(ac_client: AsyncClient):
    """Клиент для аутентификации пользователя для дальнейших тестов"""
    register_response = await ac_client.post("/api/v1/register", json={
        "username": "test_user",
        "email": "test@example.com",
        "password": "test_password"
    })
    token = register_response.json()["access_token"]
    print(token)
    ac_client.headers.update({"Authorization": f"Bearer {token}"})
    return ac_client



async def test_login_user(ac_client: AsyncClient):
    response = await ac_client.post("/api/v1/login", data={
        "username": "test@example.com",
        "password": "test_password"
    })
    assert response.status_code
    data = response.json()
    print(f"Login user: {data}")

async def test_get_users_me_authorized(auth_ac_client: AsyncClient):
    response = await auth_ac_client.get('/api/v1/users/me')
    assert response.status_code == 200
    data = response.json()
    print(f"Users me: {data}")
    assert "username" in data
    assert "email" in data
    assert data["username"] == "test_user"
    assert data["email"] == "test@example.com"





# @pytest.mark.parametrize("book_id, status_code", [(3, 404)])
# async def test_get_book_by_id(book_id, status_code, ac_client: AsyncClient):
#     response = await ac_client.get(f"/api/v1/books/{book_id}")
#     assert response.status_code == status_code
#
#

#
#
# @pytest.mark.parametrize("status_code", [401])
# async def test_get_users_me(status_code, ac_client: AsyncClient):
#     response = await ac_client.get('/api/v1/users/me')
#     assert response.status_code == status_code



