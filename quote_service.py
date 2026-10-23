import os
from dotenv import load_dotenv
from openai import OpenAI
import constants
import logging

AION_MODEL = "aion-labs/aion-3.5-mini"
INSTRUCTION = "You write concise, original, memorable quotes. Return exactly a single (one) quote, with no explanation. DO NOT ADD ANYTHING APART FROM THE QUOTE ITSELF."

logger = logging.getLogger(__name__)
load_dotenv()

api_key = os.getenv(constants.AION_API_KEY)

if not api_key:
    raise RuntimeError(f'{constants.AION_API_KEY} is missing from env variables. Set it first.')


client = OpenAI(
            api_key=api_key,
            base_url=constants.AION_BASE_URL,
            timeout=30.0,
            max_retries=0,
        )

def ask_llm(query):
    quote = None
    try:
        response = client.responses.create(
            model=AION_MODEL,
            instructions=INSTRUCTION,
            input=f"Generate a single quote on {query}",
        )

        quote = response.output_text.strip()
    except Exception:
        logger.exception("Failed to generate a quote for subject: ", query)
        quote = None

    return quote


