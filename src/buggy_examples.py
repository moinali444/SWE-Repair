BUG_EXAMPLES = [
    {
        "id": "BUG001",
        "description": "Assignment operator used instead of comparison",
        "code": "def is_zero(n):\n    if n = 0:\n        return True\n    return False",
        "expected": "def is_zero(n):\n    if n == 0:\n        return True\n    return False",
    },
    {
        "id": "BUG002",
        "description": "List index out of range",
        "code": "def get_last(numbers):\n    return numbers[len(numbers)]",
        "expected": "def get_last(numbers):\n    return numbers[len(numbers) - 1]",
    },
    {
        "id": "BUG003",
        "description": "Incorrect arithmetic operator",
        "code": "def add(a, b):\n    return a - b",
        "expected": "def add(a, b):\n    return a + b",
    },
]