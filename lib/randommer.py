"""
A wrapper for https://randommer.io, or more specifically, the pages that aren't natively in the API.
"""

import json
from enum import Enum
from bs4 import BeautifulSoup
from aiohttp import ClientSession

# The aiohttp session to make requests from
session: ClientSession = None

# There's an official API for Randommer, however it does not yet have
# support for some things (like random songs). So this is a very
# crude makeshift wrapper for just automating use of the website
_API_HEADERS = {
  "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
  "accept-language": "en-US,en;q=0.9",
  "cache-control": "max-age=0",
  "content-type": "application/x-www-form-urlencoded",
  "sec-fetch-dest": "document",
  "sec-fetch-mode": "navigate",
  "sec-fetch-site": "same-origin",
  "sec-fetch-user": "?1",
  "sec-gpc": "1",
  "upgrade-insecure-requests": "1"
}

# The root URL of Randommer
_API_URL = 'https://randommer.io'

class PageType(Enum):
  """
  Randommer has a few types of pages. The first type simply makes an XHR POST request to an endpoint, to get the random data. The other type submits a form reloading the entire page. Obviously, these different types of pages need to be handled differently in code. 
  """
  FORM_PAGE = 0
  XHR_PAGE = 1

class RandommerEndpoint:
  """
  Represents an endpoint for Randommer, including the URL and the type of page it is (check out RandommerPageType)
  """
  def __init__(self, path: str, page_type: PageType):
    self.url = _API_URL + path
    self.page_type = page_type

class Endpoint(Enum):
  """
  You likely won't need to use this! This is an enum containing all of the API endpoints used in this wrapper.
  """
  RANDOM_SONG = RandommerEndpoint('/random-songs', PageType.FORM_PAGE)
  RANDOM_THINGS_TO_DRAW = RandommerEndpoint('/random-things-to-draw', PageType.XHR_PAGE)

async def scrape_randommer_endpoint(endpoint: Endpoint):
  """
  For Randommer pages that do not have API support yet, this function manually scrapes the page and returns the random value.
  """

  # Fetch the randommer page, passing the same data the frontend website uses.
  async with session.post(
    endpoint.value.url,
    data='quantity=1&__RequestVerificationToken=CfDJ8B_ybJQnCGBOjvVX6NM4i3oWntf8vI3v5azYSEoLz6L9pyjiOJ_NdhQtiaTS1bolCBj1591WFIl1ViEV3QvbPN3r2OW-lix_PHx8_rEZWBVrfoU0GfmAXApzjufVtMk6fU268PHP3w7Xn6d-Z4jUJ1Xw8Yu_WwkybxKldIWOWWm4MPkGzmebfAUV65xOrP4QCA',
    headers={
      "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
      "accept-language": "en-US,en;q=0.9",
      "cache-control": "max-age=0",
      "content-type": "application/x-www-form-urlencoded",
      "sec-fetch-dest": "document",
      "sec-fetch-mode": "navigate",
      "sec-fetch-site": "same-origin",
      "sec-fetch-user": "?1",
      "sec-gpc": "1",
      "upgrade-insecure-requests": "1"
    }
  ) as res:
    
    # Get the raw HTML
    raw_html = await res.text()
    
    # If we need to parse the value out of the page
    if endpoint.value.page_type == PageType.FORM_PAGE:

      # Parse it with BeautifulSoup
      parsed_html = BeautifulSoup(raw_html, 'html.parser')

      try:

        # Get the (first) random value out of the HTML
        value = parsed_html.select_one('body > div > main > div:nth-child(4) > div > div > a > div > p').text

      # The result we want doesn't exist, or it's not in the right place 
      except IndexError:
        return "RESULT_NOT_FOUND"
    
    # Otherwise, just grab the value
    else:
      value = json.loads(raw_html)[0]

    # Return it
    return value