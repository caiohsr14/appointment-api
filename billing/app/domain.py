from decimal import Decimal
from pydantic import BaseModel, Field
from uuid import UUID, uuid4

class Billing(BaseModel):
	id: UUID = Field(default_factory=uuid4)
	appointment_id: UUID
	total_price: Decimal
