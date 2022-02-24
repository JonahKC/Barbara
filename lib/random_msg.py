"""
Tools for providing evenly-distributed (every value gets displayed equally as much, but still randomly) using a file, and other fancy stuff. Built for Barbara's /secret, /pickup, and /breakup.
"""

import os
from typing import Union
from random import shuffle

class MessageBank:
  """
  Stores a list of messages and provbank_ides a random selection
  """

  def __init__(self, message_bank: Union[list, tuple, set], bank_id: int, prefix="p-"):
    """
    Initializes the MessageBank object
    `message_bank` is A list of messages in the form of a list/tuple/set
    `bank_id` is a unique bank_identifier for the MessageBank, used to store the cache
    """
    self.messages = message_bank
    self.bank_id = bank_id
    self.prefix = prefix

    # If the cache file doesn't exist or it's empty
    if not os.path.exists(f"./temp/cache/{self.prefix}{str(bank_id)}.txt") or os.stat(f"./temp/cache/{self.prefix}{str(bank_id)}.txt").st_size == 0:

      # There's a cache so that we don't repeat the same message for a while
      with open(f"./temp/cache/{self.prefix}{str(bank_id)}.txt", "w") as cache_file:

        # Shuffle the messages
        shuffle(self.messages)

        # Write the shuffled messages to the file
        cache_file.writelines(self.messages)

  def reshuffle(self, new_messages: Union[list, tuple, set]=None):
    """
    Force-reshuffle the message bank
    """
    self.messages = new_messages
    with open(f"./temp/cache/{self.prefix}{str(self.bank_id)}.txt", "w") as cache_file:
      
      # Shuffle the messages
      shuffle(self.messages)

      # Write the shuffled messages to the file
      cache_file.writelines(self.messages)

  def get_random_message(self):
    """
    Returns a random message from the message bank, using the cache to avoid repeating the same message
    """
    with open(f"./temp/cache/{self.prefix}{str(self.bank_id)}.txt", "r") as cache_file:
      
      # Read the cache into an array
      cache = cache_file.readlines()

    with open(f"./temp/cache/{self.prefix}{str(self.bank_id)}.txt", "w") as cache_file:    
      # If the cache is empty
      if len(cache) == 0:
      
        # Shuffle the messages again
        shuffle(self.messages)
        new_cache = self.messages
  
        try:
          return new_cache.pop()
  
        # *chuckles* I bet you thought this wasn't possible.
        # Through the black magic of try..finally, AFTER the function returns
        finally:
        
          # Write the shuffled messages to the file
          cache_file.writelines(new_cache)
      else:
      
        # WARNING: Black magic again
        try:
          
          # Return the last element in the cache array, and remove it
          return cache.pop()
        finally:
        
          # Write the new array to the file
          cache_file.writelines(cache)

def create_message_bank_for_every_server(guilds, path="./resources/pickup_lines.txt", prefix="p-"):
  """
  Creates a MessageBank object for every server in the guilds list, using the guild bank_id as the cache bank_id. Returns a dictionary of all of the guild bank_ids, and their corresponding MessageBank objects.
  """
  pickupMessageBanks = {}

  # Open the list of messages
  with open(path, 'r') as raw_messges:

    # Read the list of messages into a list
    messages = raw_messges.readlines()

  # For each guild in the guilds list
  for guild in guilds:

    # Create a MessageBank object for the guild
    pickupMessageBanks[guild.id] = MessageBank(messages, guild.id, prefix)

  # Return the list of MessageBank objects
  return pickupMessageBanks