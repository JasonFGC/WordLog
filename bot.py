# WordLog bot 
# Jason Lam
# Project started 2024 - 04 - 23
# Last Update: 2024 - 04 - 24
# Trying to keep comments plentiful to document progress + have explanations for the stuff I'm doing
# for discord implementation 
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

wordbank = ["test"]

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
    if argword in wordbank:
        await ctx.send("This word is already in the wordbank.")
    else:
        await ctx.send("You have added "+argword+" to the list of tracked words.")
        wordbank.append(argword)

@bot.command()
async def trackedwords(ctx):
    wordoutput =""
    for i in wordbank:
        wordoutput += ' "'+i+'"'
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
            if messageSplit[i] in wordbank:
                print(messageSplit[i])
                trigger +=1
                wordOutput += ' "' + messageSplit[i] + '"'
                print(personsaid)
        if trigger != 0:            
            #await message.add_reaction('U+1FAF5')
            await message.channel.send(personsaid + ' has used:' + wordOutput+'.')     
    

    
    


bot.run(Bot_Token) 