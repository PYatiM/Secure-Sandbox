from fastapi import FastAPI
from pydantic import BaseModel
from runner.executor import execute_python

app = FastAPI()


class CodeRequest(BaseModel):
    code: str


@app.post("/execute")
def run_code(request: CodeRequest):
    return execute_python(request.code)