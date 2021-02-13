import discord
import os
token = os.getenv('TOKEN')
#intents=discord.Intents(messages=True, guild_reactions=True)
intents=discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
  print("logged in as {0.user}".format(client))

@client.event
async def on_message(message):
  if message.author == client.user: return
  if message.content.startswith('$'):
    await message.channel.send("Command Test")

client.run(token)