from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import Request, HTTPException
from runner.executor import execute_python
from collections import defaultdict
import time
import asyncio

RATE_LIMIT = 10  # Max requests per minute
WINDOW_SECONDS = 60
requests_log = defaultdict(list)

def is_rate_limited(client_ip):
    now = time.time()
    requests_log[client_ip] = [t for t in requests_log[client_ip] if now - t < WINDOW_SECONDS]
    
    if len(requests_log[client_ip]) >= RATE_LIMIT:
        return True
    requests_log[client_ip].append(now)
    return False

app = FastAPI()
MAX_CONCURRENT_EXECUTIONS = 2
semaphore = asyncio.Semaphore(MAX_CONCURRENT_EXECUTIONS)

class CodeRequest(BaseModel):
    code: str

@app.post("/execute")
async def run_code(request: CodeRequest, req: Request):
    client_ip = req.client.host

    if is_rate_limited(client_ip):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    async with semaphore:
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            execute_python,
            request.code
        )
        return result

@app.get("/")
def root():
    return {"message": "Secure Sandbox API is running"}