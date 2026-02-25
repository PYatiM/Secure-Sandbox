from fastapi import FastAPI
from pydantic import BaseModel
from runner.executor import execute_python
import asyncio

app = FastAPI()
MAX_CONCURRENT_EXECUTIONS = 2
semaphore = asyncio.Semaphore(MAX_CONCURRENT_EXECUTIONS)

class CodeRequest(BaseModel):
    code: str


@app.post("/execute")
async def run_code(request: CodeRequest):
    async with semaphore:
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            execute_python,
            request.code
        )
        return result