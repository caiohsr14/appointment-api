import asyncio
import asyncpg
import pytest
from app.config import settings
from app.routes import app
from mq_consumer import Processor
from httpx import AsyncClient
from datetime import datetime, timedelta
from uuid import uuid4

@pytest.fixture(scope="module")
def mock_appointment():
	appointment = {
	  "id": str(uuid4()),
	  "start_date": str(datetime.now()),
	  "end_date": str(datetime.now() + timedelta(hours=2, minutes=30)),
	  "physician_id": str(uuid4()),
	  "patient_id": str(uuid4()),
	  "price": 200
	}
	yield appointment

@pytest.fixture(scope="module")
def event_loop():
	loop = asyncio.get_event_loop()
	yield loop

@pytest.fixture(scope="module")
def billing_processor():
	yield Processor(settings.postgres_test_url)

@pytest.fixture(scope="module")
async def db_pool():
	pool = await asyncpg.create_pool(dsn=settings.postgres_test_url)
	yield pool

@pytest.fixture(scope="module")
async def api_client(db_pool):
	app.db_pool = db_pool

	client = AsyncClient(app=app, base_url=f"http://localhost:{settings.app_port}")
	yield client
	await client.aclose()
