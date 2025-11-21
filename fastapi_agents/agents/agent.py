# from strands import Agent, tool
# from strands.models.gemini import GeminiModel
# import requests
# import os
# from dotenv import load_dotenv
# load_dotenv()
# model = GeminiModel(
#     client_args={
#         "api_key": os.getenv("GEMINI_API_KEY")
#     },
#     model_id="gemini-2.5-flash",
#     params={
#         "temperature": 0.5,
#         "max_output_tokens": 2048,
#         "top_p": 0.9,
#         "top_k": 40
#     }
# )


# @tool
# def fetch_india_act(act_code: str):
#     """ Fetch full act text from India Code API"""
#     url = f"https://www.indiacode.nic.in/api/acts/{act_code}"
#     r = requests.get(url)
#     return r.json() if r.headers.get("content-type") == "application/json" else r.text

# @tool
# def fetch_india_section(act_code: str, section_number: str):
#     """Fetch specific section from an act."""
#     url = f"https://www.indiacode.nic.in/api/section/{act_code}/{section_number}"
#     r = requests.get(url)
#     return r.json() if r.headers.get("content-type") == "application/json" else r.text

# @tool
# def fetch_constitution_article(article_number: str):
#     """Fetch Constitution article."""
#     url = f"https://www.indiacode.nic.in/api/articles/A1950/{article_number}"
#     r = requests.get(url)
#     return r.json() if r.headers.get("content-type") == "application/json" else r.text

# agent = Agent(model=model, tools=[fetch_india_act, fetch_india_section, fetch_constitution_article])

from strands import Agent, tool
from strands.models.gemini import GeminiModel
import requests
import os
from dotenv import load_dotenv
load_dotenv()

# ----------------------------
# Safe Model Config
# ----------------------------
model = GeminiModel(
    client_args={
        "api_key": os.getenv("GEMINI_API_KEY")
    },
    model_id="gemini-2.5-flash",
    params={
        "temperature": 0.3,
        "max_output_tokens": 1500,         # keeps responses small
        "top_p": 0.9,
        "top_k": 40
    }
)

# ----------------------------
# TOOL SAFETY WRAPPERS
# Tools return LARGE data -> limit results
# ----------------------------
def safe_truncate(text: str, limit: int = 2000):
    """Avoid giant JSON overwhelming token budget."""
    return text[:limit] + "..." if len(text) > limit else text


@tool
def fetch_india_act(act_code: str):
    """Fetch act text safely (truncated)."""
    url = f"https://www.indiacode.nic.in/api/acts/{act_code}"
    r = requests.get(url)
    data = r.text
    return safe_truncate(data)


@tool
def fetch_india_section(act_code: str, section_number: str):
    """Fetch specific section (truncated)."""
    url = f"https://www.indiacode.nic.in/api/section/{act_code}/{section_number}"
    r = requests.get(url)
    return safe_truncate(r.text)


@tool
def fetch_constitution_article(article_number: str):
    """Fetch Constitution article (truncated)."""
    url = f"https://www.indiacode.nic.in/api/articles/A1950/{article_number}"
    r = requests.get(url)
    return safe_truncate(r.text)


# ----------------------------
# STATELESS AGENT (IMPORTANT)
# ----------------------------
def get_agent():
    """Returns a fresh stateless Agent instance every time."""
    return Agent(
        model=model,
        tools=[
            fetch_india_act,
            fetch_india_section,
            fetch_constitution_article
        ],
        memory=None,                 # <-- DISABLE MEMORY
        max_tokens=4096,             # <-- Prevent runaway event loop
        reset_context=True           # <-- FORCE STATELESS BEHAVIOR
    )
