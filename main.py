import asyncio
import os
import discord
from discord.ext import commands
from movie_link import get_title
from dotenv import load_dotenv
load_dotenv()
DISCORD_KEY = os.getenv("CLIENT_KEY")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

client = discord.Client(intents=intents)


@bot.command()
async def movie(ctx, *, name):
    film = get_title(name)
    name = name.upper()
    if not film:
        await ctx.send(f"No movies found for {name}")
        return

    em = discord.Embed(title=f"Movies Found: ", colour=discord.Color.brand_green())
    em.add_field(
            name=f"{film['title']}",
            value=f"[IMDB Link]({film['imdb']})\n[Streaming Link]({film['stream']})",
            inline=False
        )

    await ctx.send(embed=em)


@bot.command()
async def prompt(ctx, message: str, timeout: float) -> str:
    await ctx.send(message)

    message = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel,
                                 timeout=timeout)

    return message.content


@bot.command()
async def series(ctx, *, name):
    try:
        season = await prompt(ctx, message="What season?", timeout=10)
        episode = await prompt(ctx, message="What episode?", timeout=10)
        response = get_title(name, season=season, episode=episode)
        em = discord.Embed(title=f"Series Found:", colour=discord.Color.blue())
        em.add_field(
            name=f"{response['title']} - Season {season} Episode {episode}",
            value=f"[IMDB Link]({response['imdb']})\n[Streaming Link]({response['stream']})",
            inline=False
        )

        await ctx.send(embed=em)
    except asyncio.TimeoutError as e:
        print(e)


bot.run(DISCORD_KEY)
