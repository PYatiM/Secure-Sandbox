import ast

FORBIDDEN_NODES = {
    ast.Import: lambda n: any(a.name in BLOCKED_MODULES for a in n.names),
    ast.ImportFrom: lambda n: n.module in BLOCKED_MODULES,
    ast.Call: lambda n: (
        isinstance(n.func, ast.Name) and n.func.id in ("eval", "exec", "compile")
    ),
}

BLOCKED_MODULES = {"os", "sys", "subprocess", "socket", "shutil", "ctypes", "importlib"}

def validate_code(code: str):
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return False, f"Syntax error: {e}"

    for node in ast.walk(tree):
        for node_type, checker in FORBIDDEN_NODES.items():
            if isinstance(node, node_type) and checker(node):
                return False, f"Forbidden construct detected: {ast.dump(node)}"

    return True, "Code passed static checks"