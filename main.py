# Main bot color hex code: 0xd9880f
from re import A
import discord
import json
from discord.ext import commands, tasks
from discord import ui
from discord.ui import Button, View
import asyncio
import os
import re
import random
import dotenv
import sys
import datetime
from discord import app_commands
import time
import pyttsx3
import requests
import flask
import typing
import sqlite3
from typing import Union


COLORS = {
  (0, 0, 0): "⬛",
  (0, 0, 255): "🟦",
  (255, 0 , 0): "🟥",
  (255, 255, 0): "🟨",
  (255, 165, 0): "🟧",
  (255, 255, 255): "⬜",
  (0, 255, 0): "🟩",
  (160, 140, 210): "🟪",
  # (190, 100, 80):  "🟫",
}

bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())

class PersistentViewBot(commands.Bot):
  def __init__(self):
    intents = discord.Intents.all()
    super().__init__(command_prefix=("."), intents=intents)

bot = PersistentViewBot()

statuses = ["Returned to Discord!", "Check Bot", ".help", "With friends", "Working on Employing workers", "I am public!", "I am free to use!", "Check me out at github.com/imdakiki/checkbot"]
status_index = 0

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    change_status.start()

@tasks.loop(seconds=15)
async def change_status():
    global status_index
    await bot.change_presence(activity=discord.Game(name=statuses[status_index]))
    status_index = (status_index + 1) % len(statuses)
    
def restart_bot():
  os.execv(sys.executable, ['python'] + sys.argv)

@bot.command()
async def restart(ctx):
    allowed_ids = [898255050592366642]

    if ctx.author.id not in allowed_ids:
        error_msg = discord.Embed(description=":x: Only <@898255050592366642> can use this command")
        await ctx.send(ctx.message.author.mention, embed=error_msg)
        return

    await ctx.reply(f":white_check_mark: {bot.user.name} Has restarted!")
    restart_bot()

@bot.command()
async def invite(ctx):
    view = discord.ui.View()
    view.add_item(discord.ui.Button(label="Invite me", url="https://discord.com/api/oauth2/authorize?client_id=1190678343230685265&permissions=8&scope=bot%20applications.commands"))

    # Create the embed with the button
    embed = discord.Embed(
        title="Check Bot Invite",
        description="Want to Invite me to your server? Press the button saying `Invite me` Below"
    )

    await ctx.reply(embed=embed, view=view)

    interaction, _ = await bot.wait_for("button_click", check=lambda i: i.component.label == "Invite me")

    await interaction.response.send_message(content="You clicked the support server button!")

@bot.command()
async def say(ctx, *, text):
    allowed_ids = [898255050592366642]

    if ctx.author.id not in allowed_ids:
        error_msg = discord.Embed(description=":x: Only <@898255050592366642> can use this command")
        await ctx.send(ctx.message.author.mention, embed=error_msg)
        return

    await ctx.send(f"{text}")
    await ctx.message.delete()

@bot.command()
async def support(ctx):
    # Create a view with a link button
    view = discord.ui.View()
    view.add_item(discord.ui.Button(label="Support Server", url="https://discord.gg/sapZzf59Nv"))

    # Create the embed with the button
    embed = discord.Embed(
        title="Support server",
        description="Need support?? Join the support server with the button saying `Support Server` Below!"
    )

    # Send the embed with the button
    await ctx.reply(embed=embed, view=view)

    # Wait for the user to interact with the button
    interaction, _ = await bot.wait_for("button_click", check=lambda i: i.component.label == "Support Server")

    # Respond to the button click if needed
    await interaction.response.send_message(content="You clicked the support server button!")

    # You can also perform other actions based on the button click, if desired
    # For example, you can use the interaction to get the user who clicked the button: interaction.user



bot.run(PROCESS.ENV.TOKEN)
