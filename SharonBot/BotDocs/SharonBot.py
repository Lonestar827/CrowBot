from random import randint
import discord
import sys

client = discord.Client()

#current invokers for the bot
invoker = 'dandyism'

#stanzas based off of Slayers Instant Kill
stanza1= [line.rstrip('\n') for line in open('FirstDandyStanzas.txt')]
stanza2= [line.rstrip('\n') for line in open('SecondDandyStanzas.txt')]
stanza3= [line.rstrip('\n') for line in open('ThirdDandyStanzas.txt')]
#submissions of stanzas by user input
submit1= [line.rstrip('\n') for line in open('FirstDandySubmissions.txt')]
submit2= [line.rstrip('\n') for line in open('SecondDandySubmissions.txt')]
submit3= [line.rstrip('\n') for line in open('ThirdDandySubmissions.txt')]
#databases for future use
stanzaDatabase = [stanza1, stanza2, stanza3]
submissionDatabase = [submit1, submit2, submit3]
totalDatabase = [stanzaDatabase, submissionDatabase]
#database references for !view
FIRST_STANZA = 0
SECOND_STANZA = 1
THIRD_STANZA = 2
STANZA_DATABASE = 0
SUBMISSION_DATABASE = 1

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    #H E L L O
    if message.content.startswith(invoker + '!hello'):
        #<:HelloPenguini:410292057622708235> is the penguin emote
        msg = '<:HelloPenguini:410292057622708235> \n ``「H E L L O」``'.format(message)
        await client.send_message(message.channel, msg)

    #!bitchass : If ya want to insult the bot
    if message.content.startswith(invoker + '!bitchass'):
        msg = 'WHAT DID YA SAY, SUCKA!? \n' + '<a:Gahn:395276099141238794><a:Frame:395276114064572426>'.format(message)
        await client.send_message(message.channel, msg)

    #!toTheStars : be treated to a dandy haiku
    if message.content.startswith(invoker + '!toTheStars'):
        #generate the stanzas
            part1 = stanzaDatabase[0][randint(0,len(stanza1))]
            part2 = stanzaDatabase[1][randint(0,len(stanza2))]
            part3 = stanzaDatabase[2][randint(0,len(stanza3))]

        #put together the messege
            msg = "```" + part1 + "\n" + part2 + "\n" + part3 + "```".format(message)
            await client.send_message(message.channel, msg)

    #!submit : submit a stanza for the bot
    if message.content.startswith(invoker + '!submit'):

        #see which stanza they want
        await client.send_message(message.channel,
        "Please tell me which stanza you're submitting (1, 2, 3), or any other input to abort submission"
                                 )

        msg = await client.wait_for_message(author=message.author)

        #check for proper input
        if(msg.content.startswith('1') or msg.content.startswith('2') or msg.content.startswith('3')):

            #number variable for later
            number = msg

            #get stanza
            await client.send_message(message.channel,
            "Please tell me the content of the stanza (Type `abort` to cancel stanza submission)"
                                     )

            #message variable for later
            msg = await client.wait_for_message(author=message.author)

            #check for "abort"
            if msg.content.startswith('abort'):
                #end command
                await client.send_message(message.channel,
                 "Aborting submission"
                                         )

            else:
                #thank the user for the stanza
                await client.send_message(message.channel, 
                                          "Thanks for submitting your dandy stanza!"
                                         )

                #write to file
                if(number.content == '1'):
                    submit1.append(msg.content)
                if(number.content == '2'):
                    submit2.append(msg.content)
                if (number.content == '3'):
                    submit3.append(msg.content)

        #not proper input
        else:
            await client.send_message(message.channel,
            "Thats not a valid entry, please try `!submitting` again"
                                     )
                                
    #!help : Show help page
    if message.content.startswith(invoker + '!help'):
        await client.send_message(message.channel,
        "```A bot designed for Haikus\nCommands available to everyone:\ndandyism!hello: H E L L O\ndandyism!toTheStars: be treated to a dandy haiku made from the txt files\ndandyism!submit: submit your own stanzas for review\ndandyism!help: shows the help page\ndandyism!credits: shows where credit is due\ncommands available to admins (Role Manegers)\ndandyism!view: allows you to look at the available stanzas and submissions\n```"
                                 )

    #!save: saves the current instances of stanzas to the txt file
    #if message.content.startswith(invoker + '!save'):
    #check to see if the caller is the bot owner
    #then overwrite the files with the current instants stanzas
    
    #!view : views available stanzas
    #if message.content.startswith(invoker + '!view'):
        #check for user to be bot owner
            #if user == bot owner
        #ask to see which database to look at
            #send_message("Do you want to see the ``stanzas`` or the ``submissions``?
                #if the reply is "stanzas"
                    #database = 1 = STANZA_DATABASE
                #if the reply is "submissions"
                    #database = 2 = SUBMISSION_DATABASE
        #ask to see which stanza they want to see
            #if the reply is 1
                #stanza = 0 = FIRST_STANZA
            #if the reply is 2
                #stanza = 1 = SECOND_STANZA
            #if the reply is 3
                #stanza = 2 = THIRD_STANZA
        #Generate the list for the message
            #for i = 0, i < database.length, i++
            #line = i+1 + stanza\n
        #

    #!invite : invite this bot to other servers
    if message.content.startswith(invoker + '!invite'):
        await client.send_message(message.channel,
        "https://discordapp.com/oauth2/authorize?client_id=410301890551873536&scope=bot"
                                 )

    #!credits : shows where credit is due
    if message.content.startswith(invoker + '!credits'):
        await client.send_message(message.channel,
        "```Credits:\nLonestar : creator and coder for the bot\nSangmillion: Provided the slayer soundfiles for transcription\nUbuyo: Helping with the transcription```"
                                 )
    
    #!exit : logs_out and updates databases
    if message.content.startswith(invoker + '!exit'):
        if message.author.id == '64917161432322048':
            #placeholder code for database saving
            msg = 'By your command...'.format(message)
            await client.send_message(message.channel, msg)
            print('logged out')
            client.logout()
            sys.exit(0)
        

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    

client.run('NDEwMzAxODkwNTUxODczNTM2.DVuTEw.KtQ4oTESGNUff06Z6CNAvXk09wA')
