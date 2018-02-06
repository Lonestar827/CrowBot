from random import randint
import discord
import sys

client = discord.Client()

#current invokers for the bot
invoker = 'To The Stars'

#stanzas based off of Slayers Instant Kill
stanza1= [line.rstrip('\n') for line in open('FirstDandyStanzas.txt')]
stanza2= [line.rstrip('\n') for line in open('SecondDandyStanzas.txt')]
stanza3= [line.rstrip('\n') for line in open('ThirdDandyStanzas.txt')]

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    #H E L L O
    if message.content.startswith(invoker + '!hello'):
        msg = '<:HelloPenguini:410292057622708235> \n ``「H E L L O」``'.format(message)
        await client.send_message(message.channel, msg)

    #!bitchass : If ya want to insult the bot
    if message.content.startswith(invoker + '!bitchass'):
        msg = 'WHAT DID YA SAY, SUCKA!? \n' + '<a:Gahn:395276099141238794><a:Frame:395276114064572426>'.format(message)
        await client.send_message(message.channel, msg)

    #!haiku : be treated to a dandy haiku
    if message.content.startswith(invoker + '!haiku'):
        #generate the stanzas
            part1 = stanza1[randint(0,len(stanza1))]
            part2 = stanza2[randint(0,len(stanza2))]
            part3 = stanza3[randint(0,len(stanza3))]

        #put together the messege
            msg = "```" + part1 + "\n" + part2 + "\n" + part3 + "```".format(message)
            await client.send_message(message.channel, msg)

    #!submit : submit a stanza for the bot
    if message.content.startswith(invoker + '!submit'):

        #see which stanza they want
        await client.send_message(message.channel,
        "Please tell me which stanza you're submitting (1, 2, 3), or any other input to abort submission")

        msg = await client.wait_for_message(author=message.author)

        #check for proper input
        if(msg.content.startswith('1') or msg.content.startswith('2') or msg.content.startswith('3')):

            #number variable for later
            number = msg

            #get stanza
            await client.send_message(message.channel,
            "Please tell me the content of the stanza (Type `abort` to cancel stanza submission)")

            #message variable for later
            msg = await client.wait_for_message(author=message.author)

            #check for "abort"
            if msg.content.startswith('abort'):
                #end command
                await client.send_message(message.channel,
                "Aborting submission")

            else:
                #thank the user for the stanza
                await client.send_message(message.channel, "Thanks for submitting your dandy stanza!")

                #write to file
                if(number.content == '1'):
                    with open('FirstDandySubmitions.txt', 'a') as the_file:
                                the_file.write(msg.content + '\n')
                if(number.content == '2'):
                    with open('SecondDandySubmitions.txt', 'a') as the_file:
                                the_file.write(msg.content + '\n')
                if (number.content == '3'):
                    with open('ThirdDandySubmitions.txt', 'a') as the_file:
                                the_file.write(msg.content + '\n')    

        #not proper input
        else:
            await client.send_message(message.channel,
            "Thats not a valid entry, please try `!submitting` again")
                                

    #!help : Show help page
    if message.content.startswith(invoker + '!help'):
        await client.send_message(message.channel,
        "```A bot designed for Haikus\nCommands available to everyone:\nTo The Stars!hello: H E L L O\nTo The Stars!haiku: be treated to a dandy haiku made from the txt files\nTo The Stars!submit: submit your own stanzas for review\nTo The Stars!help: shows the help page\nTo The Stars!credits: shows where credit is due\ncommands available to admins (Role Manegers)\nTo The Stars!view: allows you to look at the available stanzas and submissions\n```")

    #!view : views available stanzas
    if message.content.startswith(invoker + '!view'):
        await client.send_message(message.channel,
        "Placeholder")
        

    #!credits : shows where credit is due
    if message.content.startswith(invoker + '!credits'):
        await client.send_message(message.channel,
        "```Credits:\nLonestar : creator and coder for the bot\nSangmillion: Provided the slayer soundfiles for transcription\nUbuyo: Helping with the transcription```")

    
    #!exit : logs_out
    if message.content.startswith(invoker + '!exit'):
        if message.author.id == '64917161432322048':
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
    

client.run('MzQyNDI3NTMwMjk4NjU0NzIx.DVU4dw.HHls59SuDNb5ulgIeUMnG0Cmzt8')
