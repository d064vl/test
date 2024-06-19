from fastapi import APIRouter, HTTPException, Request, status, Request, Depends
from typing import Annotated

from storeapi.controllers.product.productController import ProductController
from storeapi.dtos.products import ProductDTO

from storeapi.gateways.kafka import Kafka, get_kafka_instance

from storeapi.DB.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


import logging
logger = logging.getLogger(__name__)


@router.post(
            "/product", 
            status_code=201
            )
async def create_product(
                    product: ProductDTO, 
                    request: Request, 
                    ProductController: ProductController = Depends(ProductController()), 
                    session: AsyncSession = Depends(get_db),
                    server: Kafka = Depends(get_kafka_instance)
                    ):
    try:

        logger.debug(f'{product}')

        response = await ProductController.create_product(product, session, server)

        return response

    except Exception as e:
        logger.error(f"Exception {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"There was an error",
        )
