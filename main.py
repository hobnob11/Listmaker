import discord
import os
import asyncio
import datetime

token = os.getenv('TOKEN')
#intents=discord.Intents(messages=True, guild_reactions=True)
intents = discord.Intents.default()
client = discord.Client(intents=intents)
job_category = 810086759974961152
cancel_emote = '\U0001f1fd'
checkmark_emote = '\u2705'

def chronus_to_datetime(chrurl):
  return datetime.datetime.utcfromtimestamp(int(chrurl[chrurl.rfind("/")+1:],16)*60)

def datetime_to_chronus(dt):
  return "https://a.chronus.eu/"+(hex(int(dt.timestamp())//60)[2:].upper())

@client.event
async def on_ready():
  print("logged in as {0.user}".format(client))

async def createJob(message, args):
    if len(args) != 4: #todo: arg validation
        await message.channel.send("Invalid Arguments for New Job")
        return
    else:
        cat = discord.utils.get(message.guild.categories, id=job_category)
        newjob = await message.guild.create_text_channel(args[0], category=cat)
        job_cancel_msg = await newjob.send(
             "<@{0.author.id}> can react {1} to close the job.\n".format(message, cancel_emote)
            +"Time: {0}\n".format(args[1])
            +"Job Name: {0}\n".format(args[2])
            +"Party Size: {0}\n".format(args[3]))
            
        await job_cancel_msg.add_reaction(cancel_emote)
        await createList(newjob, int(args[3]))

async def createList(channel, size):
  msg = "<@{0.id}>'s {1}-Man Unclaimed List! (react with {2} to start a new list)\n".format(client.user, size, checkmark_emote)
  for i in range(size):
    msg += str(i+1) + ". \n"
  msg = await channel.send(msg)
  await msg.add_reaction(checkmark_emote)

async def joinList(lst, user):
  s = lst.content
  ownerid = s[2:s.find('>')]
  size = int(s[s.find("-Man")-1])
  if int(ownerid) == client.user.id:
    s = "<@{0}>'s {1}-Man List! (react with {2} to ask to join!)\n1. <@{0}>\n".format(user.id, size, checkmark_emote) + s[s.find("2."):]
    s += "(remove your {0} reaction to leave the list!)".format(checkmark_emote)
    await createList(lst.channel, size)
  await lst.edit(content=s, suppress=True)


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
          if emoji.name == cancel_emote:
            s = message.content
            authorid = s[2:s.find('>')]
            if int(authorid) == payload.user_id:
              await channel.delete()
            else:
              await message.remove_reaction(emoji, payload.member)
          elif emoji.name == checkmark_emote:
            print("new list!")
            await joinList(message, payload.member)
            #await message.remove_reaction(emoji, payload.member)
      


client.run(token)
