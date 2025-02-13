import pytest
from faker import Faker
from fastapi import FastAPI
from httpx import Response
from starlette.responses import Response
from starlette.testclient import TestClient


@pytest.mark.asyncio
async def test_create_chat_success(client: TestClient,
                                   app: FastAPI,
                                   faker: Faker, ):
    url = app.url_path_for("create_chat_handler")
    title = faker.text(max_nb_chars=20)
    response: Response = client.post(url, json={'title': title})

    assert response.status_code == 201
    json_data = response.json()

    assert json_data['title'] == title


@pytest.mark.asyncio
async def test_create_chat_fail_title_too_long(client: TestClient,
                                               app: FastAPI,
                                               faker: Faker, ):
    url = app.url_path_for("create_chat_handler")
    title = faker.text(max_nb_chars=300)
    response: Response = client.post(url, json={'title': title})

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_create_chat_fail_empty_title(client: TestClient,
                                            app: FastAPI,
                                            faker: Faker, ):
    url = app.url_path_for("create_chat_handler")
    response: Response = client.post(url, json={'title': ''})

    assert response.status_code == 400
