# Secure Sandboxed Code Execution Engine

An environment that accepts user code -> executes safely -> returns output.
Allows the execution of potential unsafe code in a controlled environment.
Whats different is that it enforces CPU limit, Memory limit, No file system access.

    User Input → API → Isolated Runner → Resource Limiter → Output Sanitizer → Response

-> Designed a containerized secure execution engine with enforced CPU/memory constraints, syscall restriction awareness, and network isolation to mitigate RCE and fork bomb attacks.

## How to Run

Follow these instructions to set up and run the Secure Sandbox environment on your local machine.

### Prerequisites

Before you begin, ensure you have the necessary system requirements installed.

**1. Install Docker and Docker Compose**
For Linux/Ubuntu users, run the following command:
```bash
sudo apt update
sudo apt install docker docker-compose -y

- If you are using Windows, download and install Docker Desktop. Ensure the Docker Engine application is open and running before proceeding
```
### Setup and Execution

1. Clone the repository
Pull the project files to your local machine:
```Bash

git clone [https://github.com/PYatiM/Secure-Sandbox.git](https://github.com/PYatiM/Secure-Sandbox.git)
```
2. Navigate to the project directory
```Bash

cd Secure-Sandbox

(Note: If your local environment created the folder with an underscore, use cd Secure_Sandbox instead).
```
3. Install Python dependencies
Download and install the required Python libraries:
```Bash

pip install -r requirements.txt
```
4. Build the Docker runtime image
With the Docker engine running, build the isolated sandbox environment:
```Bash

docker build -t sandbox_runtime -f Dockerfile.runtime .
```
5. Start the API server
Launch the backend application using Uvicorn:
```Bash

uvicorn api.app:app --reload
```
### Access the Application

Once the server successfully starts, open your web browser and navigate to:
http://localhost:8000


## Images

### Bare Post method in the backend
[img](img/3.png)

### Bare Get method in the backend
[img](img/4.png)

### Starting run UI
[img](img/1.png)

### Sample execution UI
[img](img/2.png)

