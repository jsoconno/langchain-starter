import os

from langchain.agents import AgentType, initialize_agent
from langchain.agents.agent import AgentExecutor
from langchain.llms.loading import load_llm
from langchain.llms import AzureOpenAI

from toolkits.terraform import TerraformToolkit
from config import set_environment_variables


def main():
    VARS = set_environment_variables(api_type="azure")

    # Use a chat model deployment
    llm = load_llm(f"{os.path.dirname(__file__)}/models/azure/completion.json")
    # llm = AzureOpenAI(
    #     deployment_name="gpt-35-turbo-16k", model="gpt-35-turbo-16k", temperature=0.7
    # )

    # Load the tools to use
    toolkit = TerraformToolkit(llm=llm)
    tools = toolkit.get_tools()

    # Initialize the agent
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )

    agent_executor = AgentExecutor(
        agent=agent.agent,
        tools=tools,
        verbose=True,
    )

    # Test
    result = agent_executor.run(
        "What blocks are available as part of the azurerm resource_group resource?"
    )
    print(result)


if __name__ == "__main__":
    main()
