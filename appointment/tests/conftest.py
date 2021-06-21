import asyncio
import asyncpg
import pytest
from httpx import AsyncClient
from app.config import settings
from app.routes import app
from app.mq_producer import Producer

@pytest.fixture(scope="module")
def event_loop():
	loop = asyncio.get_event_loop()
	yield loop
	loop.close()

@pytest.fixture(scope="module")
async def api_client():
	app.producer = Producer()
	app.db_pool = await asyncpg.create_pool(dsn=settings.postgres_test_url)

	client = AsyncClient(app=app, base_url=f"http://localhost:{settings.app_port}")
	yield client
	await client.aclose()
