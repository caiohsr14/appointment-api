import pytest
from uuid import uuid4

@pytest.mark.asyncio
async def test_valid_appointment_start(api_client):
	response = await api_client.post(
		"/appointment", 
		json={
		  "physician_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
		  "patient_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
		}
	)

	payload = response.json()
	assert response.status_code == 200
	assert "id" in payload
	assert payload["id"] is not None
	assert "start_date" in payload 
	assert payload["start_date"] is not None

@pytest.mark.asyncio
async def test_invalid_appointment_start(api_client):
	response = await api_client.post(
		"/appointment", 
		json={
		  "physician_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
		}
	)

	payload = response.json()
	assert response.status_code == 422
	assert "detail" in payload
	assert "type" in payload["detail"][0]
	assert payload["detail"][0]["type"] == "value_error.missing"

@pytest.mark.asyncio
async def test_valid_appointment_end(api_client):
	start_response = await api_client.post(
		"/appointment", 
		json={
		  "physician_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
		  "patient_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
		}
	)
	start_payload = start_response.json()
	appointment_id = start_payload["id"]

	response = await api_client.post(f"/appointment/end/{appointment_id}")
	payload = response.json()

	assert response.status_code == 200
	assert "end_date" in payload 
	assert payload["end_date"] is not None

@pytest.mark.asyncio
async def test_invalid_appointment_end(api_client):
	response = await api_client.post(f"/appointment/end/{uuid4()}")
	payload = response.json()

	assert response.status_code == 404
	assert "detail" in payload 
	assert payload["detail"] == "Appointment not found"
