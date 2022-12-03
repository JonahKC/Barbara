import os
import json
import config
import nextcord
import functools
import subprocess
from os import walk
from console import fg
from traceback import extract_tb

# This is an array with all of the commands with @admin command decorators
admin_commands = []

# This is an array with all of the commands with @jcwyt command decorators
jcwyt_commands = []

# All JCWYT Team members always have admin
JCWYT_TEAM = (437404651818582017, 797282028344573992, 738843304057372702)


def admin(*args, **kwargs):
    """
  Does this Member have admin perms?
  """

    # This is a decorator, so we need to get the function that is being decorated
    def predicate(command):

        # Add the command to the admin_commands array
        admin_commands.append(command.name)

        # Return the original command so it can be used
        return command

    # Return the entire predicate (which will be called when the decorator is used)
    return predicate


def jcwyt(*args, **kwargs):
    """
  Is this user on the JCWYT team?
  """
    def predicate(command):

        # Add the command to the admin_commands array
        jcwyt_commands.append(command.name)

        # Return the original command so it can be used
        return command

    # Return the entire predicate (which will be called when the decorator is used)
    return predicate


def has_role(member: nextcord.Member, role: int):
    """
  Does the member have a role with the specified ID?
  """

    # Get the IDs of all the roles that member has
    member_role_ids = map(lambda x: x.id, member.roles)

    # Return a boolean for whether or not the member has the role with the role ID
    return role in member_role_ids


# This is used for checking if a user is an admin in main.py
def _has_permissions(member: nextcord.Member):
    """
  Does this Member have admin perms? This is a private function and should not need to be used outside of this file
  """

    # All admins are, well, admins
    if member.guild_permissions.administrator:
        return True

    #Specifically mentioned as an admin user
    if f"<@!{member.id}>" in config.fetch(member.guild.id, "admin_users"):
        return True
    else:

        # Create a list of member's role ids
        member_roles = set(map(lambda role: role.id, member.roles))

        # Fetch the admin roles
        admin_roles = config.fetch(member.guild.id, "admin roles")

        # Convert to a set to remove duplicate entries
        combined_roles = set([*admin_roles, *member_roles])

        # Return whether any were removed as if any were, that means that there was overlap
        return len(combined_roles) < len(member_roles) + len(admin_roles)

    # If none of that returned True, we can assume they aren't an admin and return False
    return False


def load_directory(bot, directory_name):
    """
  Recursively walk through every Python file in `directory_name`, and load each as a Cog UNLESS the file name starts with lib
  """

    # Walk through every file in directory_name
    # and add each filename to all_files
    all_files = []

    for root, dirs, files in walk(directory_name):
        for file in files:

            # If it's a Python file that isn't a library
            if file.endswith(".py") and not file.startswith("lib"):

                all_files.append(file)

    # Sort it alphabetically!
    all_files = sorted(all_files)

    # Loop through all the cogs now
    for file in all_files:

        # Log the Cog is loading
        print(
            f"{fg.t_5865f2}Loading {fg.yellow}{directory_name}.{file[:-3]}{fg.default}"
        )

        try:

            # Load the Cog!
            bot.load_extension(f"{directory_name}.{file[:-3]}")

        # An error was encountered trying to load the Cog
        except Exception as error:

            # Get the stacktrace from the exception
            # .original gets the actual error in the Cog
            stack = extract_tb(error.original.__traceback__)

            # Debug it to the console with pretty red text
            print(fg.red + f"Error: {str(error.original)}")
            for i in stack.format():
                print(i)
            print("\n\nEnd of Stacktrace\n\n" + "_" * 50 + "\n\n" + fg.default)


def clear_terminal():
    """
  Clear the terminal
  """

    # If we're on Windows the command is "cls," otherwise it's "clear"
    subprocess.Popen('cls' if os.name == 'nt' else 'clear',
                     shell=True).communicate()


class InvalidLanguagePath(Exception):
    """
  Exception for when you try and read a language path from
  lang.json that doesn't exist
  """
    def __init__(self, path, *args, **kwargs):
        self.path = path
        super(*args, **kwargs)

    def __repr__(self):
        return f"I don't know where \'{self.path}\' is."


def get_message(path: str, *args, **kwargs):
    """
  Returns a message from a code (Ex. admin.no_perms = "no permissions!") using lang.json
  Additional parameters replace corresponding values in the message (Ex. get_message("foo.bar", name="joe") will replace {name} with joe)
	"""

    # Read the lang file
    with open('./lang.json') as lang_file:

        # Load it into Python as an object
        language_data = json.load(lang_file)

    if len(args) > 0:
        path = f"{path}{list(args)}"

    # Attempt to get the message at the path
    try:
        message = language_data[path]
        # Attempt to replace {foo} with the value of the custom_value foo
        try:
            return message.format(**kwargs)

        # If {foo} doesn't exist, we don't particularly care
        except KeyError:
            pass

    # Function tried to access invalid language path
    except KeyError:

        # Raise an error
        raise InvalidLanguagePath(path)

        # Return Invalid language path
        return "Invalid language path"


def walk_obj(obj, depth=0):
    """
  Return any object as nested dictionaries
  """

    # If it's a primitive value, return it to minimize on overhead.
    if type(obj) in (int, float, bool, str):
        return obj

    # Otherwise, use dir(obj) to get a list of the objects attributes
    # then uses a map of tuples, each one having the name of the
    # attribute as a string, and the value of the attribute.
    # If you used depth, it finds the value of the attribute by
    # calling itself on the attribute with one less depth.
    return dict(
        map(
            functools.partial(
                lambda a, b, c: (a, getattr(b, a))
                if c == 0 else (a, walk_obj(getattr(b, a))),
                b=obj,
                c=depth,
            ),
            dir(obj),
        ))
