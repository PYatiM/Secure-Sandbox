import os

RATE_LIMIT         = int(os.getenv("RATE_LIMIT", 10))
WINDOW_SECONDS     = int(os.getenv("WINDOW_SECONDS", 60))
EXECUTION_TIMEOUT  = int(os.getenv("EXECUTION_TIMEOUT", 3))
MEMORY_LIMIT       = os.getenv("MEMORY_LIMIT", "100m")
CPU_LIMIT          = os.getenv("CPU_LIMIT", "1")
PIDS_LIMIT         = int(os.getenv("PIDS_LIMIT", 64))
MAX_CONCURRENT     = int(os.getenv("MAX_CONCURRENT", 2))
MAX_CODE_SIZE      = int(os.getenv("MAX_CODE_SIZE", 65536))