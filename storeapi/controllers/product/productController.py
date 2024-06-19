from storeapi.dtos.products import ProductDTO


from storeapi.services.product.productService import ProductService
from fastapi import Depends

from storeapi.base.Singleton import Singleton
from sqlalchemy.ext.asyncio import AsyncSession

from storeapi.gateways.kafka import Kafka

import logging
logger = logging.getLogger(__name__)

class ProductController(metaclass=Singleton):  

    productService: ProductService

    def __call__(self):
        return self
    
    def __init__(self, productService: ProductService = Depends(ProductService())) -> None:

        self.productService = productService.dependency

    async def create_product(
                        self, 
                        post: ProductDTO, 
                        session: AsyncSession,
                        server: Kafka
                        ):
        try:
            data = post.model_dump()

            response = await self.productService.create_product(data, session, server)

            return {**response}
        except Exception as e:
            logger.error(f"Exception {e}")
            raise e
