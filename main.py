from runner.executor import execute_python

if __name__ == "__main__":
    user_code = "print('Hello Sandbox')"
    result = execute_python(user_code)
    print(result)