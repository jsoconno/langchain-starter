from typing import List
from langchain.agents.agent_toolkits.base import BaseToolkit
from langchain.pydantic_v1 import Field
from langchain.schema.language_model import BaseLanguageModel
from langchain.tools import BaseTool

# Import your tools here
from tools.terraform import get_terraform_documentation_url, get_terraform_documentation


class TerraformToolkit(BaseToolkit):
    """Toolkit for Lost and Found utilities."""

    llm: BaseLanguageModel = Field(exclude=True)

    class Config:
        """Configuration for this pydantic object."""

        arbitrary_types_allowed = True

    def get_tools(self) -> List[BaseTool]:
        """Get the tools in the toolkit."""

        # Define your tools here
        get_terraform_documentation_url_tool = get_terraform_documentation_url
        get_terraform_documentation_toolkit = get_terraform_documentation

        return [
            get_terraform_documentation_url_tool,
            get_terraform_documentation_toolkit,
        ]
