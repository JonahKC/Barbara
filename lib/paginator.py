import util
import nextcord
class Paginator(nextcord.ui.View):
  def __init__(self, interaction, bot, pages):
    """
    Custom written Paginator built for Nextcord
  
    Allows for multi-page help commands, or any long string of test.
  
    Parameters:\n
    message `(nextcord.Mesage)`: The message to get the paginator attached\n
    bot `(nextcord.ext.commands.Bot)`: The bot that will send the buttons etc\n
    pages `(Union[list[str], tuple[str], set[str]])`: All the pages, each page being it's own array element
    ephemeral `bool`: Whether or not the pages should be ephemeral
    """

    # Run the __init__ function for nextcord.ui.View disabling the timeout
    super().__init__(timeout=None)

    # Set data about this paginator instance
    self.interaction = interaction
    self.author = interaction.user
    self.pages = pages
    self.page = 0
    self.ephemeral = True
    self.bot = bot

  async def start(self, *, ephemeral=True):
    self.ephemeral = ephemeral
    
    # Send the first page, and attach all the navigation buttons as a View
    await self.interaction.send(content=self.pages[0] + f"\nPage {self.page+1}/{len(self.pages)}", view=Paginator(self.interaction, self.bot, self.pages), ephemeral=self.ephemeral)

  @nextcord.ui.button(style=nextcord.ButtonStyle.gray, disabled=True, label='←')
  async def previous_page(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
    """
    Previous page button
    """

    # If the person that clicked the button is the original command sender
    if self.author.id == interaction.user.id:

      # Go to the previous page
      self.page -= 1

      # Get the contents of the previous page
      page = self.pages[self.page]

      # If we're on the first page
      if self.page == 0:

        # Disable the previous page button (this button)
        button.disabled = True
        button.style = nextcord.ButtonStyle.gray

      # If we're no longer on the last page
      if self.page < len(self.pages):

        # Re-enable the next page button
        self.next_page.disabled = False
        self.next_page.style = nextcord.ButtonStyle.green

      # Update the interaction response to have the new page
      await interaction.response.edit_message(content=page + f"\nPage {self.page+1}/{len(self.pages)}", view=self)

    # If the person that clicked the button isn't the original command sender
    else:

      # Tell them not to touch other people's buttons
      await interaction.response.send_message(util.get_message("ui.someone_elses_button"), ephemeral=True)

  @nextcord.ui.button(style=nextcord.ButtonStyle.red, label='End Interaction')
  async def end_interaction(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
    """
    End interaction button
    """

    # If the person that clicked the button is the original command sender
    if self.author.id == interaction.user.id:

      # Delete all UI components (next page, previous page, and end interaction)
      await interaction.response.edit_message(view=None)
    
    # If the person that clicked the button isn't the original command sender
    else:

      # Tell them not to touch other people's buttons
      await interaction.response.send_message(util.get_message("ui.someone_elses_button"), ephemeral=True)

  @nextcord.ui.button(style=nextcord.ButtonStyle.green, disabled=False, label='→')
  async def next_page(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
    """
    Next page button
    """

    # If the person that clicked the button is the original command sender
    if self.author.id == interaction.user.id:

      # Go to the next page
      self.page += 1

      # Get the text of the next page
      page = self.pages[self.page]

      # If there's a previous page page to go to
      if self.page > 0:

        # Make sure the previous button is enabled
        self.previous_page.disabled = False
        self.previous_page.style = nextcord.ButtonStyle.green

      # If we've gotten to the last page
      if self.page == len(self.pages) - 1:
        
        # Disable the next page button (this button)
        button.disabled = True
        button.style = nextcord.ButtonStyle.gray
      await interaction.response.edit_message(content=page + f"\nPage {self.page+1}/{len(self.pages)}", view=self)
    
    # If the person that clicked the button isn't the original command sender
    else:

      # Tell them not to touch other people's buttons
      await interaction.response.send_message(util.get_message("ui.someone_elses_button"), ephemeral=True)