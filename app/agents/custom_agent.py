from typing import Any, Dict, Optional, Sequence, List
from langchain.agents import AgentExecutor, BaseSingleActionAgent, AgentType
from langchain.callbacks.base import BaseCallbackManager
from langchain.schema.language_model import BaseLanguageModel
from langchain.tools import BaseTool
from langchain.agents.mrkl.base import ZeroShotAgent
from langchain.chains.llm import LLMChain

# Import your toolkit here
from toolkits import LostAndFoundToolkit  # Replace with the actual import


def create_custom_agent(
    llm: BaseLanguageModel,
    toolkit: LostAndFoundToolkit,
    agent_type: AgentType = AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    input_variables: Optional[List[str]] = None,
    callback_manager: Optional[BaseCallbackManager] = None,
    verbose: bool = False,
    agent_executor_kwargs: Optional[Dict[str, Any]] = None,
    extra_tools: Sequence[BaseTool] = (),
    **kwargs: Dict[str, Any],
) -> AgentExecutor:
    """Construct a Lost and Found agent from an LLM and tools."""
    tools = toolkit.get_tools() + list(extra_tools)

    # Initialize agent to None
    agent = None

    # Add your custom logic here to create the agent based on the agent_type
    if agent_type == AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION:
        prompt = ZeroShotAgent.create_prompt(
            tools,
            # prefix=prefix,
            # suffix=suffix or SQL_SUFFIX,
            # format_instructions=format_instructions,
            input_variables=input_variables,
        )
        print(prompt)
        llm_chain = LLMChain(
            llm=llm,
            prompt=prompt,
            callback_manager=callback_manager,
        )
        tool_names = [tool.name for tool in tools]
        agent = ZeroShotAgent(llm_chain=llm_chain, allowed_tools=tool_names, **kwargs)
        pass
    else:
        raise ValueError(f"Agent type {agent_type} not supported at the moment.")

    # Check if the agent was properly initialized
    if agent is None:
        raise ValueError("Agent was not properly initialized.")

    return AgentExecutor.from_agent_and_tools(
        agent=agent,
        tools=tools,
        callback_manager=callback_manager,
        verbose=verbose,
        **(agent_executor_kwargs or {}),
    )
