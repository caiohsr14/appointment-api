import asyncio
import asyncpg

from .config import settings
from .domain import Appointment, CreateAppointmentModel
from .mq_producer import Producer

from datetime import datetime
from fastapi import FastAPI, HTTPException
from uuid import UUID

app = FastAPI()

@app.on_event("startup")
async def startup():
	app.producer = Producer()
	app.db_pool = await asyncpg.create_pool(dsn=settings.postgres_url,
											min_size=settings.postgres_min_pool_size,
											max_size=settings.postgres_max_pool_size)

@app.on_event("shutdown")
async def shutdown():
	await app.db_pool.close()

@app.post("/appointment", response_model=Appointment)
async def start_appointment(appointment_request: CreateAppointmentModel):
	appointment = Appointment(physician_id=appointment_request.physician_id, patient_id=appointment_request.patient_id)

	async with app.db_pool.acquire() as conn:
		async with conn.transaction():
			await conn.execute("INSERT INTO appointment VALUES ($1, $2, $3, $4, $5, $6)", 
				appointment.id, appointment.start_date, appointment.end_date, 
				appointment.physician_id, appointment.patient_id, appointment.price)
			return appointment

@app.post("/appointment/end/{appointment_id}", response_model=Appointment)
async def end_appointment(appointment_id: UUID):
	async with app.db_pool.acquire() as conn:
		async with conn.transaction():
			record = await conn.fetchrow("SELECT * FROM appointment WHERE id = $1", appointment_id) 
			if not record:
				raise HTTPException(status_code=404, detail="Appointment not found")

			appointment = dict(record)
			if appointment["end_date"]:
				raise HTTPException(status_code=400, detail="Appointment already ended")

			appointment["end_date"] = datetime.now()
			await conn.execute("UPDATE appointment SET end_date = $1 WHERE id = $2", appointment["end_date"], appointment["id"])
			await app.producer.publish(appointment)

			return appointment
