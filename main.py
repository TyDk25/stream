import asyncio
import os
import discord
from discord.ext import commands
from movie_link import search_movie, search_series
from dotenv import load_dotenv
load_dotenv()
DISCORD_KEY = os.getenv("CLIENT_KEY")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

client = discord.Client(intents=intents)


@bot.command()
async def movie(ctx, *, name):
    film = search_movie(name)
    name = name.upper()
    if not film:
        await ctx.send(f"No movies found for {name}")
        return

    em = discord.Embed(title=f"Movies Found: ", colour=discord.Color.brand_green())
    for movie in film:
        em.add_field(
            name=f"{movie['title']}",
            value=f"[IMDB Link]({movie['url']})\n[Streaming Link]({movie['streaming_link']})",
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
        response = search_series(name, season, episode)

        em = discord.Embed(title=f"Series Found: ", colour=discord.Color.blue())
        for show in response:
            em.add_field(
                name=f"{show['title']}",
                value=f"[IMDB Link]({show['url']}) [Streaming Link]({show['streaming_link']})",
                inline=False
            )

        await ctx.send(embed=em)
    except asyncio.TimeoutError as e:
        print(e)


bot.run(DISCORD_KEY)
