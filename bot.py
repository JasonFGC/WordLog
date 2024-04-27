# WordLog bot 
# Jason Lam
# Project started 2024 - 04 - 23
# Last Update: 2024 - 04 - 24
# Trying to keep comments plentiful to document progress + have explanations for the stuff I'm doing
# for discord implementation 
from word import * # Imports my word class, would rather keep a different object in a different file for clarity
import discord
from discord.ext import commands
from config import * # Keeps sensitive information private
# for implementation of firebase / firestore
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
cred = credentials.Certificate(firebase_config)
firebase_admin.initialize_app(cred)
db = firestore.client()
#for weekly resets etc
import datetime

testword = Word(0,0, False, "test")
wordbank = [testword]

# Apr 23: Firestore has been created, functionality low, figuring out how to store things first
# Apr 24: Firestore database changed, added basic functionality (words get passed through the bot, if bot sees a word, it catches it. Doesn't catch itself.)
# Words cannot be duplicate in the wordbank. I want to start making this functional with firebase, but I'll need make a per server-esque method of using the 
# database, currently it's set up with one collection named servers, with multiple documents that should include the servers that the bot is in.
# It should create a new document depending on the server ID, and things such as wordbank will be taking words from the document for that corresponding server.
#
bot=commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("Bot is online.")


@bot.command()
async def hi(ctx):
    await ctx.send("hai :3")

@bot.command()
async def add(ctx , argword):
    inWords = 0
    for i in range(len(wordbank)):
        if argword == wordbank[i].getWord():
            inWords+=1
    if inWords>=1:
        await ctx.send("This word is already in the wordbank.")
    else:
        await ctx.send("You have added "+argword+" to the list of tracked words.")
        wordbank.append(Word(0,0,False,argword))

@bot.command()
async def trackedwords(ctx):
    wordoutput =""
    for i in range(len(wordbank)):
        wordoutput += ' "'+wordbank[i].getWord()+'"'
    if len(wordbank) <=0:
        await ctx.send("There are no words currently being tracked.")
    else:
        await ctx.send("The list of words that are being tracked is:" + wordoutput + ".")

@bot.command()
async def checkDatabaseExists(databaseName):
    doc_ref = db.collection(databaseName)
    doc = doc_ref.get()
    if doc.exists:
        print(f"Document data: {doc.to_dict()}")
    else:
        print("No such document!")

# I'll uncomment this when I start getting the database functionality working. I want to make it so the database 
# is structured where the collection is actually the server, the documents are each word and each word has fields, for if it's limited, what word it even is, 
# and the actual limit itself (how many times per week.)
#@bot.command()
#async def addWeeklyLimit(word):

    

# Checks every message for commands. If it does not have commands, checks for words.
@bot.event
async def on_message(message):
    # This needs to be here, without it, it will not process other commands.
    await bot.process_commands(message)

    # This prevents the bot from catching itself.
    if message.author == bot.user:
        return
    # This prevents the bot from catching messages that are intended to be commands.
    if message.content[0] != "!":
        #This is for catching words in messages.
        personsaid = str(message.author)
        trigger = 0
        wordOutput= ""
        messageSplit = message.content.casefold().split()
        for i in range(len(messageSplit)):
            for j in range(len(wordbank)):
                if messageSplit[i] == wordbank[j].getWord():
                    print(messageSplit[i])
                    trigger +=1
                    wordOutput += ' "' + messageSplit[i] + '"'
                    print(personsaid)
        if trigger != 0:            
            await message.add_reaction('\U0001FAF5')
            await message.channel.send(personsaid + ' has used:' + wordOutput+'.')     


# quick thing for when it joins a server
@bot.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send("Hello! I'm WordLog! I track words that you want me to track! For more info, type !commands!")
        break

@bot.command()
async def commands(ctx):
    await ctx.send("Here is the list of commands:\n!add WORD - This command adds a work to be tracked \n!trackedwords - This command shows you which words are being tracked. \n!remove WORD - This removes the word from being tracked. \n!setlimit WORD - This allows you to set a weekly limit for a word.\n!removelim WORD - This removes the limit from this word.")
    


bot.run(Bot_Token) 