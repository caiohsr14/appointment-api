import json
import logging
import sys
from aio_pika import connect_robust, Exchange, Message, DeliveryMode, ExchangeType
from aio_pika.pool import Pool
from .config import settings

def _init_logger():
	logger = logging.getLogger("producer")
	logger.setLevel(logging.INFO)

	handler = logging.StreamHandler(sys.stderr)
	handler.setLevel(logging.INFO)

	formatter = logging.Formatter("%(created)f:%(levelname)s:%(name)s:%(module)s:%(message)s")
	handler.setFormatter(formatter)
	logger.addHandler(handler)

class Producer():
	def __init__(self):
		self.url = settings.rabbitmq_url
		self.connection_pool = Pool(self.get_connection, max_size=10)
		self.exchange_pool = Pool(self.get_exchange, max_size=20)

		_init_logger()
		self.logger = logging.getLogger("producer")

	async def get_connection(self):
		return await connect_robust(self.url)

	async def get_exchange(self) -> Exchange:
		async with self.connection_pool.acquire() as conn:
			channel = await conn.channel()
			return await channel.declare_exchange(
				settings.rabbitmq_exchange_topic, ExchangeType.TOPIC
			)

	async def publish(self, content):
		async with self.exchange_pool.acquire() as exchange:
			serializedContent = json.dumps(content, sort_keys=True, default=str)
			self.logger.info(
				f"Publishing message [{serializedContent}] on exchange topic: [{settings.rabbitmq_exchange_topic}]"
			)

			message = Message(
				serializedContent.encode("utf-8"),
				delivery_mode=DeliveryMode.PERSISTENT
			)

			await exchange.publish(message, routing_key=settings.rabbitmq_binding_key)
