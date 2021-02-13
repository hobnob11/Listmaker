import discord
import os
import asyncio

token = os.getenv('TOKEN')
#intents=discord.Intents(messages=True, guild_reactions=True)
intents = discord.Intents.default()
client = discord.Client(intents=intents)
job_category = 810086759974961152
job_cancel_emote = '\U0001f1fd'
new_list_emote = '\u2705'

@client.event
async def on_ready():
  print("logged in as {0.user}".format(client))


async def createJob(message, args):
    if len(args) != 1:
        await message.channel.send("Invalid Arguments for New Job")
        return
    else:
        cat = discord.utils.get(message.guild.categories, id=job_category)
        newjob = await message.guild.create_text_channel(
            args[0], category=cat)
        job_cancel_msg = await newjob.send(
            "<@{0.author.id}> can react \U0001f1fd to close the job.\n Anyone can react \u2705 to start a new list!".format(message))
        await job_cancel_msg.add_reaction(job_cancel_emote)
        await job_cancel_msg.add_reaction(new_list_emote)



@client.event
async def on_message(message):
    if message.author == client.user: return
    if message.content.startswith('$'):
        args = message.content[1:].split()
        if (len(args) < 1):
            await message.channel.send("Error, Invalid Command")
        else:
            if args[0] == "newjob":
                await createJob(message, args[1:])
                await message.delete()

            #await message.channel.send("Command Test")


@client.event
async def on_raw_reaction_add(payload):
    channel = client.get_channel(payload.channel_id)
    message = await channel.get_partial_message(payload.message_id).fetch()
    emoji = payload.emoji
    if payload.user_id == client.user.id: return
    if channel.category.id == job_category:
      if message.author == client.user:
          #if the channel is in the job category and the message
          #reacted too was posted by the bot:
          if emoji.name == job_cancel_emote:
            s = message.content
            authorid = s[2:s.find('>')]
            if int(authorid) == payload.user_id:
              await channel.delete()
            else:
              await message.remove_reaction(emoji, payload.member)
          elif emoji.name == new_list_emote:
            print("new list!")
            await message.remove_reaction(emoji, payload.member)
      


client.run(token)
