from langchain_core.tools import tool
from langchain.agents import create_agent


@tool
def multiply(a: int, b: int) -> int:
    """Multiply a and b.

    Args:
        a: first int
        b: second int
    """
    print(f"Multiplying {a} and {b}")
    return a * b


agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[multiply],
    system_prompt="You are a helpful assistant",
)
