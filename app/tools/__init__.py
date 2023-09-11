import random

from langchain.agents import tool


@tool
def generate_random_number() -> int:
    """Generates a random number between 1 and 100."""
    random_integer = random.randint(1, 100)

    return random_integer


@tool
def add_two_numbers(a: int, b: int) -> int:
    """Adds two numbers together."""
    return a + b
