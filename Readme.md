# Secure Sandboxed Code Execution Engine

An environment that accepts user code -> executes safely -> returns output.
Allows the execution of potential unsafe code in a controlled environment.
Whats different is that it enforces CPU limit, Memory limit, No file system access.

    User Input → API → Isolated Runner → Resource Limiter → Output Sanitizer → Response

-> Designed a containerized secure execution engine with enforced CPU/memory constraints, syscall restriction awareness, and network isolation to mitigate RCE and fork bomb attacks.

## Whats UNSAFE code and how does it "Sanitize it"

    A code is deemed unsafe when it tends to break the flow of operations of the program and intends to corrupt or gain access to the source.

    how does it Sanitize it:
        Blocks every unsafe keywords and operations from the source code by checking for them from a list of pre coded checklist
        Even if there is a bypass the sandbox nature ensures the code doesnt affect the entire projects is onlya limited impact
        It ensure usage of safe coding methods and practices

## Fork Bomb attacks and its mitigation

    Fork bombing is the act of spawning child processes recursively until the system runs out of process ids (pid)

    The sandbox counter it with the Dockers 
    --pid-linit
    flag, which caps the total number of process the container can have. 
    When the limit is hit fork() fails with EAGAIN - the bomb exhausts itself without touching the host pids namespace.
    Hence the container gets killed or stalls, returning an error to the user

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
![img](img/3.png)

### Bare Get method in the backend
![img](img/4.png)

### Starting run UI
![img](img/1.png)

### Sample execution UI
![img](img/2.png)

