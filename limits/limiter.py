import resource


def set_limits(memory_limit_mb: int = 50, cpu_time_sec: int = 2):
    # Limit CPU time
    resource.setrlimit(resource.RLIMIT_CPU, (cpu_time_sec, cpu_time_sec))

    # Limit memory usage
    memory_bytes = memory_limit_mb * 1024 * 1024
    resource.setrlimit(resource.RLIMIT_AS, (memory_bytes, memory_bytes))