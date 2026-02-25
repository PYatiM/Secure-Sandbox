import subprocess
import tempfile
import os
import sys
import time
import json
import uuid


def execute_python(code: str, timeout: int = 3):
    container_name = f"sandbox_{uuid.uuid4().hex}"

    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = os.path.join(tmpdir, "user_code.py")

        with open(file_path, "w") as f:
            f.write(code)

        start = time.time()

        try:
            result = subprocess.run(
                [
                    "docker", "run",
                    "--rm",
                    "--name", container_name,
                    "--memory=100m",
                    "--cpus=1",
                    "--network=none",
                    "--pids-limit=64",
                    "--read-only",
                    "--tmpfs", "/tmp",
                    "-v", f"{tmpdir}:/sandbox:ro",
                    "sandbox_runtime"
                ],
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
            subprocess.run(["docker", "kill", container_name])
            return {
                "stdout": "",
                "stderr": "Execution timed out",
                "returncode": -1
            }