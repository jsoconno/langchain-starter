from typing import List
from langchain.agents.agent_toolkits.base import BaseToolkit
from langchain.pydantic_v1 import Field
from langchain.schema.language_model import BaseLanguageModel
from langchain.tools import BaseTool

# Import your tools here
from tools import (
    generate_random_number,
    add_two_numbers,
)


class MathToolkit(BaseToolkit):
    """Toolkit for Lost and Found utilities."""

    llm: BaseLanguageModel = Field(exclude=True)

    class Config:
        """Configuration for this pydantic object."""

        arbitrary_types_allowed = True

    def get_tools(self) -> List[BaseTool]:
        """Get the tools in the toolkit."""

        # Define your tools here
        generate_random_number_tool = generate_random_number
        add_two_numbers_tool = add_two_numbers

        return [generate_random_number_tool, add_two_numbers_tool]
