import pytest
from uuid import uuid4

@pytest.mark.asyncio
async def test_valid_appointment_end(mock_appointment, billing_processor, db_pool):
	await billing_processor.process(mock_appointment)

	async with db_pool.acquire() as conn:
		record = await conn.fetchrow("SELECT * FROM billing WHERE appointment_id = $1", mock_appointment["id"]) 
		data = dict(record)

		assert record is not None
		assert data["total_price"] == 600 

@pytest.mark.asyncio
async def test_valid_billing_get(mock_appointment, api_client):
	appointment_id = mock_appointment["id"]
	response = await api_client.post(f"/billing/{appointment_id}")
	payload = response.json()

	assert response.status_code == 200
	assert "total_price" in payload 
	assert payload["total_price"] == 600

@pytest.mark.asyncio
async def test_invalid_billing_get(api_client):
	response = await api_client.post(f"/billing/{uuid4()}")
	payload = response.json()

	assert response.status_code == 404
	assert "detail" in payload 
	assert payload["detail"] == "Billing for appointment not found"
