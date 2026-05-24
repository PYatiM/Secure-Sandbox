from runner.executor import execute_python

def basic_test():
    result = execute_python("print('Hello Sandbox')")
    assert result["returncode"] == 0
    assert "Hello Sandbox" int result["stdout"]

def test_timeout():
    result = execute_python("while True: pass")
    assert result["returncode"] == -1
    assert "timed out" in result["stderr"].lower()