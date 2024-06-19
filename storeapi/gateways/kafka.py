import asyncio

from aiokafka import AIOKafkaProducer
from storeapi.base.Singleton import Singleton
from storeapi.DB.config import config


class Kafka(metaclass=Singleton):

    def __init__(
        self,
        topic,
        port,
        servers
    ) -> None:
        self._topic = topic
        self._port = port
        self._servers = servers
        self.aioproducer = self.create_kafka()


    def __call__(self):
        return self
    
    

    def create_kafka(self):
        loop = asyncio.get_event_loop()
        return AIOKafkaProducer(
            loop=loop,
            bootstrap_servers=f'{self._servers}:{self._port}'
        )
    
def get_kafka_instance():
    return Kafka(
        topic=config.KAFKA_TOPIC_NAME,
        port=config.KAFKA_PORT,
        servers=config.KAFKA_SERVER,
    )
