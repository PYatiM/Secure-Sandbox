from security.validator import validate_code
from limits.limiter import set_limits
import subprocess
import tempfile
import os
import sys
import time

preexec = set_limits if os.name != "nt" else None
def execute_python(code: str, timeout: int = 2):
    start = time.time()
    
    is_valid, message = validate_code(code)

    if not is_valid:
        return {
            "stdout": "",
            "stderr": message,
            "returncode": -1
        }
        
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = os.path.join(tmpdir, "user_code.py")

        with open(file_path, "w") as f:
            f.write(code)
        
        try:
            result = subprocess.run(
                [sys.executable, file_path],
                capture_output=True,
                text=True,
                timeout=timeout,
                preexec_fn=set_limits
            )
            end = time.time()
            
            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
                "execution_time": round(end - start, 4)
            }

        except subprocess.TimeoutExpired:
            return {
                "stdout": "",
                "stderr": "Execution timed out",
                "returncode": -1
            }