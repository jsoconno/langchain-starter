import os
import sys

import openai


def check_env_variable(var_name):
    value = os.getenv(var_name)
    if not value:
        print(f"Error: Environment variable {var_name} is not set.")
        sys.exit(1)
    return value


def set_environment_variables(api_type="openai"):
    env_vars = {}
    # Configure openai api
    env_vars["api_type"] = openai.api_type = check_env_variable("OPENAI_API_TYPE")

    if api_type == "azure":
        env_vars["api_version"] = openai.api_version = check_env_variable(
            "OPENAI_API_VERSION"
        )
        env_vars["api_base"] = openai.api_base = check_env_variable("OPENAI_API_BASE")
        env_vars["api_key"] = openai.api_key = check_env_variable("OPENAI_API_KEY")

    return env_vars
