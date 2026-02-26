import time
from fastapi import Request
from ..core.logger import logger

async def logging_middleware(request: Request, call_next):
    start_time = time.time()
    
    method = request.method
    path = request.url.path
    
    logger.info(f"Incoming request: {method} {path}")
    
    response = await call_next(request)
    
    process_time = (time.time() - start_time) * 1000
    logger.info(f"Completed request: {method} {path} - Status: {response.status_code} - Time: {process_time:.2f}ms")
    
    return response
