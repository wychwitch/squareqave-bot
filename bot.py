import tomllib, discord, yt_dlp
from pathlib import Path
from discord.ext import commands

config_path = Path("config.toml")
config_content = config_path.read_text()
config = tomllib.loads(config_content)

bot_token = config["discord"]["token"]
download_path = config["yt-dlp"]["download_path"]

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command()
async def download(ctx, url):
    if url.startswith("https://youtu") or url.startswith("https://www.youtu"):
        msg = await ctx.reply("Starting download...")
        ydl_opts = {
            'format': 'mp3/bestaudio/best',
            'outtmpl': {"default":f"{download_path}%(playlist_title|)s/%(playlist_index|)s%(playlist_index& - |)s%(title)s.%(ext)s"},
            'postprocessors': [{  # Extract audio using ffmpeg
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }]
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            error_code = ydl.download(url)

        if error_code:
            await msg.edit(content=f"Something went wrong. {error_code}")
        else:
            await msg.edit(content="Downloaded!")
    else:
        await ctx.reply("Url isn't right...")


bot.run(bot_token)