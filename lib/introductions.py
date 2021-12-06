from discord.ext import commands

KEYWORDS = ("lincoln", "hale", "roosevelt", "holy name", "lakeside", "ingraham", "ida b", 'he', 'them', '8th', '9th', '10th', '11th', '12th')
TRIM = ('hello', ':', 'name', 'my', 'is', 'go', 'by', 'howdy', '\'', 'im')

async def index(bot):
  global INTRODUCTIONS
  INTRODUCTIONS = (await (await bot.fetch_channel(854961975292854283)).history(limit=250).flatten())[::-1]

def is_wwhs():
  def predicate(ctx):
    return ctx.guild.id == 838269717566718002
  return commands.check(predicate)

def has_keywords(msg):
  for k in KEYWORDS:
    if k in msg.lower():
      return True
  return False

def extract_name_from_intro(intro: str):
  trimmed = intro.lower()
  for t in TRIM:
    trimmed = trimmed.replace(t, '') # Remove keywords such as name and my name is, etc.
  return " ".join(" ".join([name.capitalize() for name in trimmed.split('\n')[0].split(' ')]).strip().split(' ')[0:2]) # Format the name from a multiline intro

def find_name(person):
  try:
    # Get messages contents from the #introductions channel that match either the person's discord id or discord tag and has a school name in it
    potentialMessages = [x for x in filter(lambda x: (person.name in x.content or x.author.id == person.id) and has_keywords(x.content), INTRODUCTIONS)]
    potentialMessages = [x.content for x in potentialMessages]
    # Return the extracted name w/a newspace
    return extract_name_from_intro('\n'.join(potentialMessages))
  except AttributeError as e:
    print(e)
    return "`no introduction found for user`"