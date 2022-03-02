"""
A wrapper for the Huggingface Accelerated Inference API. For generating text from an AI prompt.
"""

import os
import enum
import aiohttp

api_token = os.getenv("HUGGINGFACE_API_TOKEN")

# HTTP headers to pass to Huggingface (w/ authentication)
_headers = {"Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_TOKEN')}"}

# So we don't create a new ClientSession each time
# the AI is prompted
session = None

# The base URL for accessing Huggingface models
_BASE_URL = "https://api-inference.huggingface.co/models/"

class Model(enum.Enum):
  """
  Enum representing various models and their IDs for Huggingface. This only really becomes useful when there's a lot more options to choose from. For now it looks hella cool though.
  """
  GPT_J_6B = "EleutherAI/gpt-j-6B"
  GPT_NEO_2B = "EleutherAI/gpt-neo-2.7B"

async def query(payload, model: Model, parameters={}, options={}):
  """
  Pass input text into an AI in the Huggingface Accelerated Inference API
  
  `payload`: Input text for AI
  `model`: URL for the specified AI (in the Model enum)
  `parameters`: JSON object with data about how the AI should process the text. Example: `{"repetition_penalty": float (>=0.0, <=100.0), "temperature": float (>0.0, <=100.0), "return_full_text": bool, "top_p": float (>0.0, <=1.0)}`
  `options`: Non-AI-related options for how Huggingface processes the request. Example: `{'wait_for_model': bool}`
  """
  body = {"inputs": payload, 'parameters': parameters, 'options': options}
  async with session.post(_BASE_URL + model.value, headers=_headers, json=body) as response:
    try:
      return (await response.json())
    except aiohttp.client_exceptions.ContentTypeError:
      return (await response.text())