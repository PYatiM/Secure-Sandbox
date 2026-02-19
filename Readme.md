# Secure Sandboxed Code Execution Engine

## Basically an environment that accepts user code -> executes safely -> returns output 
## whats different is that it enforces CPU limit, Memory limit, No file system acess

    User Input → API → Isolated Runner → Resource Limiter → Output Sanitizer → Response
