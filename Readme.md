# Secure Sandboxed Code Execution Engine

## Basically an environment that accepts user code -> executes safely -> returns output 
## whats different is that it enforces CPU limit, Memory limit, No file system acess

    User Input → API → Isolated Runner → Resource Limiter → Output Sanitizer → Response

## Designed a containerized secure execution engine with enforced CPU/memory constraints, syscall restriction awareness, and network isolation to mitigate RCE and fork bomb attacks.
