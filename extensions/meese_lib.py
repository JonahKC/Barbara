import re
import util
import config
import nextcord
import unicodedata
from unidecode import unidecode
from nextcord.ext import commands

class MeeseLib(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.reloadMeeseBlacklist()

  # Various Regexes that I use a lot in the future
  # Best for efficiency to compile them now
  MEESE_REGEX = re.compile(r"me{2,}s+e")
  MULTIPLE_LETTERS_REGEX = re.compile(r"(.)\1{2,}")
  SPOILER_REGEX = re.compile(r"\|\|.*?\|\|", re.MULTILINE | re.DOTALL)

  def reloadMeeseBlacklist(self):
    """
    Reload all of the characters (like nn) that look similar to M, E, or S
    as well as TRIM_CHARS (extra stuff like period)
    """

    # Open the meese blacklist text file
    with open('./resources/meese_blacklist.txt', 'r') as blacklist_raw:

      # Make all of the variables global
      global M_BLACKLIST, E_BLACKLIST, S_BLACKLIST, TRIM_CHARS
      M_BLACKLIST = []
      E_BLACKLIST = []
      S_BLACKLIST = []
      TRIM_CHARS = []

      # Read the blacklist and add an extra newline to the end
      blacklist_raw = blacklist_raw.read() + '\n'

      # This is the current category it's parsing
      temp_category = "M_BLACKLIST"

      # Read blacklist, and sort into M_BLACKLIST, E_BLACKLIST, S_BLACKLIST, and TRIM_CHARS
      # Split by newlines and loop through each line
      for line in blacklist_raw.split('\n'):

        # If it starts with $$ (a new category)
        if line.startswith('$$'):

          # Get the category name
          temp_category = line[2:].strip()

          # Go to the next line and continue parsing
          continue
        else:

          # Otherwise, append the current character to the corresponding category
          if temp_category == "M_BLACKLIST":
            M_BLACKLIST.append(line.strip('\n'))
          elif temp_category == "E_BLACKLIST":
            E_BLACKLIST.append(line.strip('\n'))
          elif temp_category == "S_BLACKLIST":
            S_BLACKLIST.append(line.strip('\n'))
          elif temp_category == "TRIM_CHARS":
            TRIM_CHARS.append(line.strip('\n'))

  def replace_words(self, words, string, replaceWith, replace=1):
    """
    Replace a whole array of different words with a string, and convert it all to lowercase
    """

    # If there's nothing to replace, just return the original string
    if len(words) == 0: return string

    # Go through each word to replace
    for word in words:

      # Replace it
      newString = string.replace(word, replaceWith, replace)

      # Update the original string
      string = newString

    # Make it all lowercase and return it
    return string.lower()


  def has_meese(self, potentially_dirty_string, whitelist = []):
    """
    Use the Meese Detection Algorithm™ to detect meese (the incorrect plural of moose) in a string
    """

    # Use Regex to remove anything inside a discord spoiler (||text||)
    cleaned_string = re.sub(self.SPOILER_REGEX, '', potentially_dirty_string)

    # Clean up fake letters "/\/\" instead of "m" etc.
    cleaned_string = self.replace_words(M_BLACKLIST, cleaned_string, "m", 32)
    cleaned_string = self.replace_words(E_BLACKLIST, cleaned_string, "e", 64)
    cleaned_string = self.replace_words(S_BLACKLIST, cleaned_string, "s", 32)

    # Remove digits
    cleaned_string = re.sub(r'\d', '', cleaned_string)

    # Convert other fancy unicode characters to normal characters
    cleaned_string = unicodedata.normalize('NFKC', cleaned_string)

    # Remove all accents etc.
    cleaned_string = unidecode(cleaned_string)

    # Finally run it through regex to detect the string meese
    contains_meese = re.findall(self.MEESE_REGEX, cleaned_string)

    # If there's a match, return the array of all the matches
    if contains_meese:
      return (True, contains_meese, cleaned_string)

    # Otherwise just return false
    return (False, contains_meese, cleaned_string)

  async def detect_in_message(self, message):
    try:

      # Prevent bot conflicts
      if not message.author.bot:

        # Check if the config is set to detect/delete  meese
        if config.read(message.guild.id, "nomees"):

          # Trim the message (removing filler chars etc.)
          trimmed_message = self.replace_words(
            TRIM_CHARS,
            message.content.lower(),
            "",
            -1
          )
          
          # Remove whitelisted characters
          trimmed_message = self.replace_words(
            config.fetch(message.guild.id, "whitelist"),
            trimmed_message,
            "",
            -1
          )

          # Check for meese using the Meese Detection Algorithm™
          has_meese = self.has_meese(trimmed_message, config.fetch(message.guild.id, "whitelist"))
          
          # If there's matches
          if has_meese[0]:

            # Send a message explaining what just happened
            await message.reply(util.get_message("meese.meese_detection", nomees=nextcord.PartialEmoji.from_str("nomees:936864150716575744")))
            
            # Delete the heresay
            await message.delete()
            await self.bot.logger.log(message.guild.id, "meese detection", message=message)
            


            # Report the message in our channel to help us debug false detections
            await self.bot.get_channel(864644173835665458).send(
              f"{message.author.name}: ```\n{message.content}```\n" \
              f"Message after processing: ```\n{has_meese[2]}```\n" \
              f"Matches: ```\n{has_meese[1]}```"
            )

    # The message has already been deleted or something
    except (nextcord.errors.NotFound, nextcord.errors.HTTPException):
      
      # I'm sure it's fine
      pass

  # Detect for meese when you send a new message
  @commands.Cog.listener()
  async def on_message(self, message):
    await self.detect_in_message(message)
  
  # Detect for meese when you edit an old message
  @commands.Cog.listener()
  async def on_message_edit(self, before, after):
    await self.detect_in_message(after)
  
  # JCWYT-only context menu item for reporting a false detection
  @util.jcwyt()
  @nextcord.message_command(
    name="Report Detection",

    # This context menu item is only available in the JCWYT server
    guild_ids=[863919587825418241],
  )
  async def report_meese_detection(self, interaction: nextcord.Interaction, message: nextcord.Message):
    """
    Report a message that wasn't detected automatically as containing meese
    """

    # Trim the message (removing filler chars etc.)
    trimmed_message = self.replace_words(
      TRIM_CHARS,
      message.content.lower(),
      "",
      -1
    )
    
    # Remove whitelisted characters
    trimmed_message = self.replace_words(
      config.fetch(interaction.guild_id, "whitelist"),
      trimmed_message,
      "",
      -1
    )

    # Run the message through detection and get some data on it
    has_meese = self.has_meese(trimmed_message, config.fetch(interaction.guild_id, "whitelist"))

    # Send a message explaining what just happened
    await message.reply(util.get_message("meese.meese_detection", nomees=nextcord.PartialEmoji.from_str("nomees:936864150716575744")))
    
    # Delete the heresay
    await message.delete()
    await self.bot.logger.log(interaction.guild_id, "meese detection", message=message)

    # Report the message in our channel to help us debug false detections
    await self.bot.get_channel(864644173835665458).send(
      f"{message.author.name}: ```\n{message.content}```\n" \
      f"Message after processing: ```\n{has_meese[2]}```\n" \
      f"Matches: ```\n{has_meese[1]}```"
    )

    # Send an ephemeral success message
    await interaction.send("Successfully reported the message.", ephemeral=True)

def setup(bot):
  bot.add_cog(MeeseLib(bot))