import os

DEVELOPMENT_FEATURES = True if os.getenv('DEVELOPMENT_FEATURES') == 'True' else False

# Whether or not slash commands are only available in TESTING_GUILD_ID, or in all guilds.
SLASH_COMMANDS_GLOBAL = True if os.getenv('SLASH_COMMANDS_GLOBAL') == 'True' else False

# JCWYT Guild ID, for testing slash commands
TESTING_GUILD_ID = [863919587825418241] if DEVELOPMENT_FEATURES else []

# JCWYT Beta Tester role ID, for whitelisting commands
BETA_TESTER_ID = 863920057486671913