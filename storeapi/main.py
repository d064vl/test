import uvicorn

from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.exception_handlers import http_exception_handler
from fastapi.responses import JSONResponse, PlainTextResponse
from storeapi.gateways.kafka import get_kafka_instance

from contextlib import asynccontextmanager


from fastapi.middleware.cors import CORSMiddleware


from asgi_correlation_id import CorrelationIdMiddleware


from fastapi.middleware.gzip import GZipMiddleware


import time


import httpx

from storeapi.routers.products import router as products_router

import logging
logger = logging.getLogger(__name__)
from storeapi.log.logging_conf import configure_logging
from storeapi.DB.config import config

from storeapi.DB.database import init_models, close

kafka_server = get_kafka_instance()


@asynccontextmanager
async def lifespan(app: FastAPI):

    configure_logging() 
    await init_models()
    await kafka_server.aioproducer.start()
    app.requests_client = httpx.AsyncClient() 

    yield

    await close()
    await app.requests_client.aclose() 
    await kafka_server.aioproducer.stop()

app = FastAPI(lifespan=lifespan)


app.add_middleware(CorrelationIdMiddleware)


app.add_middleware(GZipMiddleware, minimum_size=1000)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


app.include_router(products_router)



@app.exception_handler(HTTPException)
async def http_exception_handle_logging(request, exc: HTTPException):
    logger.error(f"HTTPException: {exc.status_code} {str(exc.detail)} {str(exc.headers)}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": f"Oops! {exc.status_code} {str(exc.detail)} {exc.headers}"},
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)