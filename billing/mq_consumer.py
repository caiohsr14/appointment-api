import asyncio
import asyncpg
import json
import logging
import math
import sys
from aio_pika import connect_robust, IncomingMessage, ExchangeType
from app.config import settings
from datetime import datetime
from decimal import Decimal
from functools import partial
from uuid import uuid4

appointment_props = ["id", "start_date", "end_date", "physician_id", "patient_id", "price"]

class Processor():
	def __init__(self, db_url):
		self.db_url = db_url

	async def process(self, appointment):
		if not all(prop in appointment.keys() for prop in appointment_props):
			return

		start = datetime.fromisoformat(appointment["start_date"])
		end = datetime.fromisoformat(appointment["end_date"])
		total_seconds = (end - start).total_seconds()
		total_hours = math.ceil(total_seconds/3600)
		total_price = Decimal(appointment["price"]) * Decimal(total_hours)

		conn = await asyncpg.connect(self.db_url)
		await conn.execute("INSERT INTO billing VALUES ($1, $2, $3)", 
				uuid4(), appointment["id"], total_price)
		await conn.close()

def _init_logger():
	logger = logging.getLogger("consumer")
	logger.setLevel(logging.INFO)

	handler = logging.StreamHandler(sys.stderr)
	handler.setLevel(logging.INFO)

	formatter = logging.Formatter("%(created)f:%(levelname)s:%(name)s:%(module)s:%(message)s")
	handler.setFormatter(formatter)
	logger.addHandler(handler)

async def on_message(logger, processor, message: IncomingMessage):
	async with message.process():
		logger.info(f"Processing message: {message.body}")
		await processor.process(json.loads(message.body.decode("utf-8")))

async def main(loop, logger):
	try:
		logger.info("Initializing appointment message consumer")
		connection = await connect_robust(
			settings.rabbitmq_url,
			loop=loop
		)

		logger.info("Connection established")

		processor = Processor(settings.postgres_url)
		channel = await connection.channel()
		await channel.set_qos(prefetch_count=1)

		exchange = await channel.declare_exchange(
			settings.rabbitmq_exchange_topic, ExchangeType.TOPIC
		)

		queue = await channel.declare_queue(
			settings.rabbitmq_queue_name, durable=True
		)

		await queue.bind(exchange, routing_key=settings.rabbitmq_binding_key)
		await queue.consume(partial(on_message, logger, processor))
	except Exception as e:
		logger.exception(e)
		await asyncio.sleep(5)
		await main(loop, logger)

if __name__ == "__main__":
	_init_logger()
	logger = logging.getLogger("consumer")

	loop = asyncio.get_event_loop()
	loop.create_task(main(loop, logger))
	loop.run_forever()
