FORBIDDEN_KEYWORDS = [
    "import os",
    "import sys",
    "subprocess",
    "socket",
    "__import__",
    "open(",
]


def validate_code(code: str):
    for keyword in FORBIDDEN_KEYWORDS:
        if keyword in code:
            return False, f"Forbidden usage detected: {keyword}"

    return True, "Code is valid"