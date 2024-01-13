import os
from datetime import date

import discord
from discord.ext import commands

from . import parser
from .article import Article

API_KEY = os.getenv("NASA_APIKEY")


def is_valid_date(in_date: date) -> bool:
    """
    Checks if the date is between today and June 16th 1995    
    """
    min_date = date(1995, 6, 16)
    max_date = date.today()
    return max_date >= in_date >= min_date


class SpaceStop(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(aliases=["cd", "2day"])
    async def today(self, ctx: commands.Context) -> None:
        """
        Get today's APOD
        """
        article = Article.from_response(parser.get_data(api_key=API_KEY))
        await article.send(ctx)

    @commands.command(aliases=["rd", "rnd", "rand"])
    async def random(self, ctx: commands.Context) -> None:
        """
        Get random APOD
        """
        article = Article.from_response(parser.get_data(api_key=API_KEY, count=1)[0])
        await article.send(ctx)
          
    @commands.command(name="date", aliases=["dt"])
    async def get_date(
        self, 
        ctx: commands.Context, 
        day: int = commands.parameter(default=lambda day: int(day), description="in 'DD' format"), 
        month: int = commands.parameter(default=lambda month: int(month), description="in 'MM' format"), 
        year: int = commands.parameter(default=lambda year: int(year), description="in 'YYYY' format")
    ) -> None:
        """
        Get APOD for specific date
        """
        in_date = date(year, month, day)

        if not is_valid_date(in_date):
            return
            
        article = Article.from_response(
            parser.get_data(api_key=API_KEY, date=in_date.strftime("%Y-%m-%d"))
            )
        await article.send(ctx)


