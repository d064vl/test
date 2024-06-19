from fastapi import HTTPException, status, Depends

from storeapi.base.Singleton import Singleton
from sqlalchemy.ext.asyncio import AsyncSession

from storeapi.schemas.Products import ProductTable
from storeapi.DB.config import config

from storeapi.gateways.kafka import Kafka

import json


from sqlalchemy import select

import logging
logger = logging.getLogger(__name__)

class ProductService(metaclass=Singleton):
    async def create_product(
                            self, 
                            data: dict, 
                            session: AsyncSession, 
                            server: Kafka
                            ):
        try:
        ######################
            logger.debug(data)
            
            productData = {
                "id":   data.get('id'),
                "name": data.get('name'),
                "description": data.get('description'),
                "amount":   data.get('pricing', {}).get('amount'),
                "currency": data.get('pricing', {}).get('currency'),
                "quantity": data.get('availability', {}).get('quantity'),
                "category": data.get('category'),
                "availability_timestamp": data.get('availability', {}).get('timestamp'),
            }
            
            await server.aioproducer.send_and_wait(
                            config.KAFKA_TOPIC_NAME, 
                            json.dumps(productData).encode("ascii")
                            )
            print(productData)
            product = ProductTable(**productData)
            session.add(product)
            await session.commit()

            return {'message' : 'Successul Operation'}
        ######################
        except Exception as e:
            logger.error(f"Exception {e}")
            raise e
