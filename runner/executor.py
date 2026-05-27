import subprocess
import tempfile
import os
import time
import uuid
import stat
from security.validator import validate_code

MAX_CODE_SIZE = 64 * 1024 #64KB to prevent large code insertion and process slowdown

def execute_python(code: str, user_input: str = "", timeout: int = 3):
    if len(code.encode("utf-8")) > MAX_CODE_SIZE:
        return {
            "stdout": "",
            "stderr": "Code Size exceeds maximum allowed limit (64KB)",
            "returncode": -1,
            "execution_time": 0
        }
    
    is_valid, reason = validate_code(code)
    if not is_valid:
        return {
            "stdout": "",
            "stderr":f"Rejected: {reason}",
            "returncode": -1,
            "execution_time": 0
        }
    
    container_name = f"sandbox_{uuid.uuid4().hex}"

    with tempfile.TemporaryDirectory() as tmpdir:
        mount_path = tmpdir.replace("\\", "/")
        
        code_path = os.path.join(tmpdir, "user_code.py")

        with open(code_path, "w") as f:
            f.write(code)
        os.chmod(code_path,stat.S_IRUSER | stat.S_IWUSR)

        if user_input and not user_input.endswith("\n"):
            user_input += "\n"
          
        start = time.time()

        try:
            result = subprocess.run(
                [
                    "docker", "run",
                    "--rm",
                    "-i",
                    "--name", container_name,
                    "--memory=100m",
                    "--cpus=1",
                    "--network=none",
                    "--pids-limit=64",
                    "-v", f"{mount_path}:/workspace",
                    "sandbox_runtime",
                    "python3", "/workspace/user_code.py"
                ],
                input=user_input,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            end = time.time()
            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
                "execution_time": round(end - start, 4)
            }
            

        except subprocess.TimeoutExpired:
            subprocess.run(
                ["docker", "kill", container_name],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            return {
                "stdout": "",
                "stderr": "Execution timed out",
                "returncode": -1,
                "execution_time": timeout
            }
            
        except Exception as e:
            return {
                "stdout": "",
                "stderr": f"Error executing code: {str(e)}",
                "returncode": -1,
                "execution_time": 0
            }