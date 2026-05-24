from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import Request, HTTPException
from runner.executor import execute_python
from collections import defaultdict
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
import time
import asyncio

RATE_LIMIT = 10  # Max requests per minute
WINDOW_SECONDS = 60
requests_log = defaultdict(list)
limiter = Limiter(key_func=get_remote_address)
MAX_OUTPUT_SIZE = 100 * 1024 # 100KB

def sanitize_output(text:str) -> str:
    if not text:
        return ""
    
    if len(text) > MAX_OUTPUT_SIZE:
        text = text[:MAX_OUTPUT_SIZE] + "\n... [output truncated]" # if output too large

    #strip ansi escape sequences
    import re
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('',text)

def is_rate_limited(client_ip):
    now = time.time()
    requests_log[client_ip] = [t for t in requests_log[client_ip] if now - t < WINDOW_SECONDS]
    
    if len(requests_log[client_ip]) >= RATE_LIMIT:
        return True
    requests_log[client_ip].append(now)
    return False

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
MAX_CONCURRENT_EXECUTIONS = 2
semaphore = asyncio.Semaphore(MAX_CONCURRENT_EXECUTIONS)

class CodeRequest(BaseModel):
    code: str
    input: str | None = ""
    
@app.post("/execute")
@limiter.limit("10/minute")
async def run_code(request: CodeRequest, req: Request):
    client_ip = req.client.host

    if is_rate_limited(client_ip):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    async with semaphore:
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            execute_python,
            request.code,
            request.input
        )
        return result
    return {
        "stdout": sanitize_output(result["stdout"]),
        "stderr": sanitize_output(result["stderr"]),
        "returncode": sanitize_output(result["returncode"]),
        "execution_time": sanitize_output(result["execution_time"])
    }

@app.get("/")
def serve_ui():
    return FileResponse("static/index.html")