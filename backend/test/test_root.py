import pytest


@pytest.mark.asyncio
async def test_root(client):

    response = await client.get("/")

    assert response.json()["message"] == "Hello MyGPT"
    assert response.status_code == 200
