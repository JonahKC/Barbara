import re
from unidecode import unidecode
import unicodedata

def reloadMeeseBlacklist():
  with open('./resources/meese_blacklist.txt', 'r') as blacklist_raw:
    global M_BLACKLIST, E_BLACKLIST, S_BLACKLIST, TRIM_CHARS
    M_BLACKLIST = []
    E_BLACKLIST = []
    S_BLACKLIST = []
    TRIM_CHARS = []
    blacklist_raw = blacklist_raw.read() + '\n'
    temp_category = "M_BLACKLIST"
    # Read blacklist, and sort into M_BLACKLIST, E_BLACKLIST, S_BLACKLIST, and TRIM_CHARS
    for line in blacklist_raw.split('\n'):
      if line.startswith('$$'):
        temp_category = line[2:].strip()
        continue
      else:
        if temp_category == "M_BLACKLIST":
          M_BLACKLIST.append(line.strip('\n'))
        elif temp_category == "E_BLACKLIST":
          E_BLACKLIST.append(line.strip('\n'))
        elif temp_category == "S_BLACKLIST":
          S_BLACKLIST.append(line.strip('\n'))
        elif temp_category == "TRIM_CHARS":
          TRIM_CHARS.append(line.strip('\n'))

MEESE_REGEX = re.compile(r"me{2,}s+e")
MULTIPLE_LETTERS_REGEX = re.compile(r"(.)\1{2,}")
SPOILER_REGEX = re.compile(r"\|\|.*?\|\|", re.MULTILINE | re.DOTALL)

def reverseString(x):
  return x[::-1]

def replaceWords(words, string, replaceWith, replace=1):
  if len(words) == 0: return string
  for word in words:
    newString = string.replace(word, replaceWith, replace)
    #if newString != string:
      #print(word + ': ' + newString)
    string = newString
  return string.lower()

def trim(inputStr):
  return replaceWords(TRIM_CHARS, inputStr, "", -1)

# The Jaro-Winkler distance is a way to measure
# the similarity between two strings
# 0.0 is entirely different and 1.0 is the same string
# Yoinked from https://python.algorithms-library.com/strings/jaro_winkler
def jaro_winkler(str1: str, str2: str) -> float:

  # Get the number of characters that are matching
  def get_matched_characters(_str1: str, _str2: str) -> str:
    matched = []
    limit = min(len(_str1), len(_str2)) // 2
    for i, l in enumerate(_str1):
      left = int(max(0, i - limit))
      right = int(min(i + limit + 1, len(_str2)))
      if l in _str2[left:right]:
        matched.append(l)
        _str2 = f"{_str2[0:_str2.index(l)]} {_str2[_str2.index(l) + 1:]}"

    return "".join(matched)

  matching_1 = get_matched_characters(str1, str2)
  matching_2 = get_matched_characters(str2, str1)

  # Get the number of matches
  match_count = len(matching_1)

  # Transposition
  transpositions = (
    len([(c1, c2) for c1, c2 in zip(matching_1, matching_2) if c1 != c2]) // 2
  )

  if not match_count:
    jaro = 0.0
  else:
    jaro = (
      1
      / 3
      * (
        match_count / len(str1)
        + match_count / len(str2)
        + (match_count - transpositions) / match_count
      )
    )

  # Common prefix up to 4 characters
  prefix_len = 0
  for c1, c2 in zip(str1[:4], str2[:4]):
    if c1 == c2:
      prefix_len += 1
    else:
      break

  return jaro + 0.1 * prefix_len * (1 - jaro)

def containsMeese(inputStr, whitelist=[]):
  # Remove whitelisted chars
  inputStr = replaceWords(whitelist, inputStr, "").lower()

  # Use Regex to remove anything inside a discord spoiler (||text||)
  inputStr = re.sub(SPOILER_REGEX, '', inputStr)

  ##print('ORIGINAL STRING: ' + inputStr)
  inputStr = replaceWords(M_BLACKLIST, inputStr, "m", 32)
  inputStr = replaceWords(E_BLACKLIST, inputStr, "e", 64)
  inputStr = replaceWords(S_BLACKLIST, inputStr, "s", 32)
  inputStr = re.sub(r'\d', '', inputStr)
  
  # Convert other fancy unicode characters to normal characters
  inputStr = unicodedata.normalize('NFKC', inputStr)

  # Remove all accents etc.
  inputStr = unidecode(inputStr)
  
  #print('FINAL STRING: ' + inputStr)

  # Detect meese the old fashioned way
  containsMeese = re.match(MEESE_REGEX, inputStr)

  # Use jaro-winkler to determine meese as well
  jaro_distances = [0]

  for meese_instance in inputStr.split(" "):
    jaro_distances.append(jaro_winkler(re.sub(MULTIPLE_LETTERS_REGEX, "\1", meese_instance), "meese"))

  # Support for meese spelled backwards
  # Disabled due to too many false detections
  #if contains_meese == None:
  #  contains_meese = re.search(MEESE_REGEX, reverseString(inputStr))

  # If the match is close enough to meese, return inputStr
  # Or if an actual match has been found
  if max(jaro_distances) > 0.94 or containsMeese:
    return (inputStr, max(jaro_distances))

  # Otherwise, return False
  return False