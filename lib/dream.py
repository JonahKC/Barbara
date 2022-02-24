"""
A wrapper for the WOMBO Dream API written in Python
"""

import json
import nextcord
from io import BytesIO
from asyncio import sleep
from aiohttp import ClientSession

session: ClientSession = None

async def _authenticate():
  """
  Get a token to access the WOMBO Dream API. You should not need this unless you're doing your own stuff with the API.
  """
  r = await session.post('https://identitytoolkit.googleapis.com/v1/accounts:signUp?key=AIzaSyDCvp5MTJLUdtBYEKYWXJrlLzu1zuKM6Xw', json={'returnSecureToken': True})
  data = await r.json()
  token = data['idToken']
  return {'Authorization': 'bearer ' + token}

async def url_to_file(url: str, secret: bool=False):
  """
  Supply a URL to an image, returns a nextcord.File object. secret will append _SECRET to the end of the filename, so Discord spoilers it.
  """

  # Note that it is often preferable to create a single session to use multiple times later - see below for this.
  async with session.get(url) as resp:
    buffer = BytesIO(await resp.read())
  
  return nextcord.File(fp=buffer, filename=f"image{'_SECRET' if secret else ''}.png")

async def imagine(prompt: str, style: int=3, *, check_progress: int=2):
  """
  Use WOMBO Dream to generate an image from a text description. Style is an integer representing the style of the AI output, I haven't gone through and figured out what each number corresponds with, but you can figure out by opening the networking tab of the developer console when you submit a prompt with a specific style. Style number 3 is no-style, which I find to be the best since you can recreate any style and more with it (by adding text like "A stone etching..." to the beginning of the prompt). check_progress is how often (in seconds) we should poll WOMBO to check on the progress of our image.
  """

  # Get the token we need to pass to the API for usage of it.
  auth_headers = await _authenticate()

  # Get a task id for a new job.
  r = await session.post('https://app.wombo.art/api/tasks', headers=auth_headers, json=json.dumps({'premium': False}))
  task_id = (await r.json())['id']

  # Assemble the complete data we'll be sending to them
  query = {'input_spec': {
    'display_freq': 10, # My guess is this is how often Wombo sends us a new image but idk
    'prompt': prompt,
    'style': style
  }}

  # Start the task!
  r = await session.put('https://app.wombo.art/api/tasks/' + task_id, json=json.dumps(query), headers=auth_headers)
  data = await r.json()

  # Wait until task is done
  while True:

    # Let's see what WOMBO Dream is doing
    r = await session.get('https://app.wombo.art/api/tasks/' + task_id, headers=auth_headers)
    data = await r.json()

    # If it's done processing
    if data['state'] == 'completed':

      # We're ready to return all of the results
      break

    # If it failed processing
    if data['state'] == 'failed':

      # Raise an error so we know what's going on
      raise RuntimeError(data)

    # Wait check_progress seconds before checking WOMBO Dream again
    await sleep(check_progress)

  # Return an array with all of the image URLs (as the AI progressively develops the image)
  return data['photo_url_list']