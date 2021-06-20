from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field
from uuid import UUID, uuid4

class CreateAppointmentModel(BaseModel):
	physician_id: UUID
	patient_id: UUID

class Appointment(BaseModel):
	id: UUID = Field(default_factory=uuid4)
	start_date: datetime = Field(default_factory=datetime.now)
	end_date: datetime = None
	physician_id: UUID
	patient_id: UUID
	price: Decimal = Decimal(200.00)
