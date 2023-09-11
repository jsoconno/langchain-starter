import re

import requests
from bs4 import BeautifulSoup, NavigableString
from langchain.agents import tool
from requests.exceptions import RequestException


def replace_with_headers(element):
    """
    Replace header tags with corresponding markdown.
    """
    if element.name in ["h1", "h2", "h3", "h4", "h5", "h6"]:
        header_level = int(element.name[1])
        header_text = f'{"#" * header_level} {element.text}'
        element.replace_with(NavigableString(header_text))


def replace_with_backticks(element):
    """
    Replace <code> and certain <div> elements with backticks (`) text.
    """
    if element.name == "code":
        backtick_text = f"`{element.text}`"
    elif element.name == "pre":
        backtick_text = f"```\n{element.text}\n```"
    else:
        return

    element.replace_with(NavigableString(backtick_text))


def scrape_website(
    url: str, tag: str = None, selector: str = None, list_output: bool = False
) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    try:
        response = requests.get(url, headers=headers, allow_redirects=True, timeout=10)
        response.raise_for_status()  # If the response contains an HTTP error status code, raise an exception
    except RequestException as e:
        print(f"Failed to get the webpage. Error: {e}")
        return None

    if response.status_code == 404:
        print("Received a 404 Not Found error.")
        return None

    soup = BeautifulSoup(response.content, "html.parser")

    # Remove all <table> tags
    for table in soup.find_all("table"):
        table.decompose()

    # Find all <code> elements and replace them with single backticks
    for code in soup.find_all("code"):
        replace_with_backticks(code)

    # Find all <pre> elements and replace them with triple backticks
    for pre in soup.find_all("pre"):
        replace_with_backticks(pre)

    # Find all header elements and replace them with markdown
    for header in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]):
        replace_with_headers(header)

    if tag:
        elements = soup.find_all(tag)
    elif selector:
        elements = soup.select(selector)
    else:
        return "\n".join(line.strip() for line in soup.text.split("\n") if line.strip())

    texts = [
        "\n".join(
            line.replace("\\n", "\n").strip()
            for line in elem.get_text().split("\n")
            if line.strip()
        )
        for elem in elements
    ]

    text_output = "\n".join(texts)

    # Post-processing to remove extra whitespace
    text_output = re.sub(r"\n{3,}", "\n\n", text_output)

    if list_output:
        return text_output.split("\n\n")
    else:
        return text_output


@tool
def get_terraform_documentation_url(
    type: str,
    provider: str,
    namespace: str = "hashicorp",
    resource: str = None,
    version: str = "main",
) -> str:
    """
    Get the documentation URL for a provider resource or data source.

    Args:
        namespace: The namespace of the provider.
        provider: The provider name.
        resource: The resource or data source name.
        scope: The scope of the documentation (resource or data source).
        version: The version of the provider (default: 'main').

    Returns:
        The documentation URL as a string.
    """

    # if docs_path:
    if type == "provider":
        url = f"https://github.com/{namespace}/terraform-provider-{provider}/blob/{'' if version == 'main' else 'v'}{version}/website/docs/index.html.markdown"
    elif type == "resource":
        url = f"https://github.com/{namespace}/terraform-provider-{provider}/blob/{'' if version == 'main' else 'v'}{version}/website/docs/r/{resource}.html.markdown"
    elif type == "data":
        url = f"https://github.com/{namespace}/terraform-provider-{provider}/blob/{'' if version == 'main' else 'v'}{version}/website/docs/d/{resource}.html.markdown"
    else:
        print("Type must be one of provider, resource, or data")

    return url


@tool
def get_terraform_documentation(documentation_url) -> str:
    """
    Get the documentation for a provider resource or data source based on its url.

    Args:
        documentation_url: The url for the Terraform documentation.

    Returns:
        The documentation content as a string.
    """
    documentation_url = documentation_url
    documentation = scrape_website(documentation_url, tag="article")
    if documentation is None:
        print("Failed to retrieve documentation.")
        return "The url is invalid. Make sure the provider name is not included in the resource."

    # Make sure newlines are translated from //n to /n for writing to file:
    documentation = documentation.replace("\\n", "\n")

    return documentation
