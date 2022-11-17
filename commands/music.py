import aiohttp
import nextcord
import base64
from io import BytesIO
from nextcord.ext import commands
from constants import TESTING_GUILD_ID, SLASH_COMMANDS_GLOBAL


class ExtendSong(nextcord.ui.View):
    def __init__(self, bot, encodings, song_data, instruments,
                 message_to_reply):
        super().__init__(timeout=60)
        self.bot = bot
        self.encodings = encodings
        self.data = song_data
        self.data['instruments'] = instruments
        self.message_to_reply = message_to_reply

    async def extend_song(self, song: int, interaction: nextcord.Interaction):
        await MusicCommand.music_command(self.bot, interaction,
                                         self.data['generationLength'],
                                         self.data['genre'],
                                         self.data['instruments'],
                                         self.encodings[song],
                                         self.message_to_reply, True)

    @nextcord.ui.button(style=nextcord.ButtonStyle.blurple,
                        disabled=False,
                        label='Extend Song 1')
    async def extend_song_1(self, button: nextcord.ui.Button,
                            interaction: nextcord.Interaction):
        await self.extend_song(1, interaction)

    @nextcord.ui.button(style=nextcord.ButtonStyle.blurple,
                        disabled=False,
                        label='Extend Song 2')
    async def extend_song_2(self, button: nextcord.ui.Button,
                            interaction: nextcord.Interaction):
        await self.extend_song(2, interaction)

    @nextcord.ui.button(style=nextcord.ButtonStyle.blurple,
                        disabled=False,
                        label='Extend Song 3')
    async def extend_song_3(self, button: nextcord.ui.Button,
                            interaction: nextcord.Interaction):
        await self.extend_song(3, interaction)

    @nextcord.ui.button(style=nextcord.ButtonStyle.blurple,
                        disabled=False,
                        label='Extend Song 4')
    async def extend_song_4(self, button: nextcord.ui.Button,
                            interaction: nextcord.Interaction):
        await self.extend_song(4, interaction)


class MusicCommand(commands.Cog):
    MUSENET_URL = 'https://musenet.openai.com'
    HEADERS = {  # Just what Brave used--probably not all necessary
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "sec-gpc": "1"
    }
    STYLES = {
        "Chopin": 'chopin',
        "Mozart": 'mozart',
        "Rachmaninoff": 'rachmaninoff',
        "Lady Gaga": 'ladygaga',
        "Country": 'country',
        "Disney": 'disney',
        "Jazz": 'jazz',
        "Bach": 'bach',
        "Beethoven": 'beethoven',
        "Journey": 'journey',
        "The Beatles": 'thebeatles',
        "Video Games": 'videogames',
        "Broadway": 'broadway',
        "Frank Sinatra": 'franksinatra',
        "Bluegrass": 'bluegrass',
        "Tchaikovsky": 'Tchaikovsky'
    }

    def __init__(self, bot):
        self.bot = bot
        # for continuing a song
        self.bot.music_encodings = {}

    @staticmethod
    async def music_command(bot,
                            interaction: nextcord.Interaction,
                            length,
                            style,
                            instruments,
                            encoding='',
                            message_to_reply=None,
                            reply=False):
        await interaction.response.defer()
        instruments = instruments.lower()
        data = {
            "genre": style,
            "instrument": {
                "piano": 'piano' in instruments,
                "strings": 'string' in instruments,
                "winds": 'wind' in instruments,
                "drums": 'drum' in instruments,
                "harp": 'harp' in instruments,
                "guitar": 'guitar' in instruments,
                "bass": 'bass' in instruments
            },
            "encoding": encoding,
            "temperature": 1,
            "truncation": 27,
            "generationLength": length,
            "audioFormat": "mp3"
        }
        async with bot.session.post(MusicCommand.MUSENET_URL + '/sample',
                                    headers=MusicCommand.HEADERS,
                                    json=data) as response:
            try:
                sample_data = (await response.json())['completions']
                audio_files = [
                    nextcord.File(
                        BytesIO(
                            bytes(
                                base64.b64decode(
                                    completion['audioFile'][2:-1]))
                        ),  # the base64 is wrapped in b'' so we trim that out here
                        f'{interaction.user.display_name}-{i+1}.mp3')
                    for i, completion in enumerate(sample_data)
                ]

                if message_to_reply and reply:
                    send = message_to_reply.reply
                else:
                    send = interaction.send
                await send(
                    f'Songs in the style of **{list(MusicCommand.STYLES.keys())[list(MusicCommand.STYLES.values()).index(style)]}** by **{interaction.user.display_name}**',
                    files=audio_files,
                    view=ExtendSong(
                        bot,
                        [completion['encoding'] for completion in sample_data],
                        data, instruments, message_to_reply))
            except aiohttp.client_exceptions.ContentTypeError:
                await interaction.send(await response.text())

    @nextcord.slash_command(
        name='music',
        description=
        'Generate music! (Payne, Christine. "MuseNet." OpenAI, 25 Apr. 2019, openai.com/blog/musenet)',
        guild_ids=TESTING_GUILD_ID,
        force_global=SLASH_COMMANDS_GLOBAL)
    async def music_command_wrapper(
        self,
        interaction: nextcord.Interaction,
        length: int = nextcord.SlashOption(
            name='length',
            description='Length of piece in tokens (50-400)',
            required=False,
            default=50,
            min_value=50,
            max_value=400),
        style: str = nextcord.SlashOption(
            name='style',
            description='Genre of music to generate',
            required=False,
            choices=STYLES,
            default='thebeatles'),
        instruments: str = nextcord.SlashOption(
            name='instrumentation',
            description=
            'List of instruments: piano, strings, winds, drums, harp, guitar, or bass',
            required=False,
            default='piano, strings, winds, drums, harp, guitar, bass')):
        await MusicCommand.music_command(self.bot, interaction, length, style,
                                         instruments)


def setup(bot):
    bot.add_cog(MusicCommand(bot))
