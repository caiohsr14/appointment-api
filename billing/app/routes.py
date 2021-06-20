import asyncio
import asyncpg
from .config import settings
from .domain import Billing
from datetime import datetime
from fastapi import FastAPI, HTTPException
from uuid import UUID

app = FastAPI()

@app.on_event("startup")
async def startup():
	app.db_pool = await asyncpg.create_pool(dsn=settings.postgres_url,
											min_size=settings.postgres_min_pool_size,
											max_size=settings.postgres_max_pool_size)

@app.on_event("shutdown")
async def shutdown():
	await app.db_pool.close()

@app.post("/billing/{appointment_id}", response_model=Billing)
async def get_appointment_billing(appointment_id: UUID):
	async with app.db_pool.acquire() as conn:
		record = await conn.fetchrow("SELECT * FROM billing WHERE appointment_id = $1", appointment_id) 
		if not record:
			raise HTTPException(status_code=404, detail="Billing for appointment not found")

		return record
