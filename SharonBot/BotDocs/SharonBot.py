from random import randint
import discord
import shlex
import re
import asyncio
import datetime
import sys

#discord client
client = discord.Client()

#base stanzas for the !haiku function
baseStanza1= [line.rstrip('\n') for line in open('FirstDandyStanzas.txt')]
baseStanza2= [line.rstrip('\n') for line in open('SecondDandyStanzas.txt')]
baseStanza3= [line.rstrip('\n') for line in open('ThirdDandyStanzas.txt')]

#helpTxt List
helpTxtList = {}

#custom stanza list and 
stanzaList = []

#botban list
botBanList = []

#serverList
serverList= []

#current invokers for the bot
invoker = 'dandy'

#token for the bot
token = [line.rstrip('\n') for line in open('tokenFile.txt')]
token = token[0]

#UserID for botOwner
botOwner = "64917161432322048"

#stanza class
class stanza:
    content = ""
    position = 0
    author = 0
    server = 0
    active = False
    SID = 0

#options class
class options:
    server = 0
    submitable = True
    announceChannel = 0
    


@client.event
async def on_server_join(server):
#whenever the bot joins a new server...
    
    #make new options, set the server to the server id and add it to the list
    newOptions = options()
    newOptions.server = server.id
    serverList.append(newOptions)

@client.event
async def on_message(message):
    #if the message is not the bot, starts with the invoker, and is not a PM
    if (message.author != client.user) and (message.content.startswith(invoker + "!")) and (message.server != None):
        
        #split the input up                               
        strippedMessage = shlex.split(message.content.lower())

        #get the command from the split input and remove the invoker
        invLength = len(invoker)+1

        command = strippedMessage.pop(0)
        command = command[invLength:]

        #if the command is in the list
        if command in commandList:
            #call the command from the list and do it
            await commandList[command](client, message, strippedMessage)

#Saves the stanzas and servers every so often
async def periodicSave(client):
    await client.wait_until_ready()
    while not client.is_closed:
        await save()
        print("data saved " + str(datetime.datetime.now()))

        await asyncio.sleep(60)
        
#H E L L O
async def hello(client, message, strippedMessage):
    await client.send_message(message.channel, "<:HelloPenguini:410292057622708235>")

#Displays the credits
async def credit(client, message, strippedMessage):
    await client.send_message(message.channel, "```Credits:\nLonestar : creator and coder for the bot\nSangmillion: Provided the slayer soundfiles for transcription\nUbuyo: Helping with the transcription\nFraw and Squaswin: for helping my dumbass out with the finer thing of coding for python discord bots```")

#gives the user a dandy haiku
async def haiku(client, message, strippedMessage):

    useBase = True
    allStanzas = False
    
    if "nobase" in strippedMessage:
        useBase = False
        
    if "all" in strippedMessage:
        allStanzas = True
        
    customStanza1 = []
    customStanza2 = []
    customStanza3 = []

    #gather the stanzas for the server where stanza.server = message.server
    #& stanza.active = true
    
    if len(stanzaList) != 0:
       
        #if the user requested all custom stanzas be used
        if allStanzas:
            for x in stanzaList:
                if (x.active == True) and (x.position == "1"):
                    customStanza1.append(x.content)
            for x in stanzaList:
                if (x.active == True) and (x.position == "2"):
                    customStanza2.append(x.content)
            for x in stanzaList:
                if(x.active == True) and (x.position == "3"):
                    customStanza3.append(x.content)
        
        #otherwise
        else:
            for x in stanzaList:
                if(x.server == message.server.id) and (x.active == True) and (x.position == "1"):
                    customStanza1.append(x.content)
            for x in stanzaList:
                if(x.server == message.server.id) and (x.active == True) and (x.position == "2"):
                    customStanza2.append(x.content)
            for x in stanzaList:
                if(x.server == message.server.id) and (x.active == True) and (x.position == "3"):
                    customStanza3.append(x.content)

    #append the base stanzas with the server stanzas
    if useBase:
        for x in baseStanza1:
            customStanza1.append(x)
        for x in baseStanza2:
            customStanza2.append(x)
        for x in baseStanza3:
            customStanza3.append(x)
        
    #get the parts
    if len(customStanza1) != 0 and len(customStanza2) != 0 and len(customStanza3) != 0:    
        part1 = customStanza1[randint(0,len(customStanza1)-1)]
        part2 = customStanza2[randint(0,len(customStanza2)-1)]
        part3 = customStanza3[randint(0,len(customStanza3)-1)]

        #put together the messege
        msg = "```" + part1 + "\n" + part2 + "\n" + part3 + "```".format(message)
        await client.send_message(message.channel, msg)
    
    #not enough parts
    else:
        msg = "not enough stanzas present, aborting".format(message)
        await client.send_message(message.channel, msg)

#displays the helptext for each command
async def helpTxt(client, message, strippedMessage):

    helpList = "```Available commands: \n hello, credits, haiku, submit \n Mod commands: \n View, options```"
    #If stripped message contains a command on the list...
    if (len(strippedMessage) != 0):
        
        #get the help text from the dict...
        
        helpCommand = strippedMessage[0]
        
        #and send the message to the channel
        
        if helpCommand in helpTxtList:
            
            await client.send_message(message.channel, helpTxtList[helpCommand])
        
        else:
            
            #display command list
            await client.send_message(message.channel, helpList)
    
    #if not...
    else:
        #display command list
        await client.send_message(message.channel, helpList)

#Submits the users stanza to the database
async def submit(client, message, strippedMessage):
    
    #set up the properties for the new stanza
    position = 0
    content = ""

    #ask for the position of the stanza
    question = "please tell me the position of the stanza (1, 2, 3) or anything else to abort"
    await client.send_message(message.channel, question)

    #wait for a message from the user...
    ret = await client.wait_for_message(
    timeout=30,
    check=lambda m: (
        m.author == message.author and 
        m.channel == message.channel
        ))
    
    #if the returned message starts with 1, 2, or 3...
    if (ret != None) and (ret.content.lower() == "1" or ret.content.lower() == "2" or ret.content.lower() == "3"):
        
        #get the first part of the reply and make that the position
        reply = shlex.split(ret.content.lower())
        position = int(reply.pop(0))

        #then ask for the content of the stanza
        question = "please tell me the content of the stanza (type ``abort`` to abort submission)"
        await client.send_message(message.channel, question)

        #wait for a message from the user...
        ret = await client.wait_for_message(
        timeout=30,
        check=lambda m: (
        m.author == message.author and 
        m.channel == message.channel 
        )
        )
        
        #if the message is NOT abort:
        if (ret is not None) and (ret.content.lower() != "abort"):
            
            #set the content of the message to the reply
            content = ret.content

            #thank the user for the stanza
            question = "Thanks for submitting your stanza!"
            await client.send_message(message.channel, question)

            #set up and add the stanza to the base
            newStanza = stanza()
            newStanza.content = content
            #print(content)
            newStanza.position = position
            #print(position)
            newStanza.server = message.server.id
            #print(server)
            newStanza.active = False
            #print(active)
            newStanza.author = message.author.id
            #print(author)
            newStanza.SID = randomID(stanzaList)
            #print(newStanza.SID)
            stanzaList.append(newStanza)

        #if it IS abort or it times out
        else:
            
            #abort the submission
            question = "Aborting Submission"
            await client.send_message(message.channel, question)

    #if its not a number or times out
    else:
        question = "Aborting Submission"
        await client.send_message(message.channel, question)
        
#creates a random SID while making sure the rest in the list dont match it
def randomID(stanzaList):
    
    #repeat until valid SID is made
    while(True):
        
        #new SID = random 5 digit integer
        newSID = randint(10000, 99999)
        
        #if theres a stanza in the list:
        if len(stanzaList) != 0:
            
            #for each stanza in the list
            for x in stanzaList:
                
                #if the stanza x's SID matches the new SID:
                if x.SID == newSID:
                    
                    #scrap the newSID and begin again
                    continue
            
            #if its gone through the entire list without matching, use the new SID
            return newSID
        
        #if there are no stanzas on the list
        else:
            #return the new SID
            return newSID

#Manual Save, caused by message
async def saveMessage(client, message, strippedMessage):

    #save the stanzas to a file
    saveFile = open('storedStanzas.txt',"w+")
    for x in stanzaList:
        saveFile.write(x.content + "|" + str(x.position) + "|" + str(x.author) + "|" + str(x.server) + "|" + str(x.active) + "|" + str(x.SID) +"\n")

    saveFile.close()
    
    #save the server settings in a file
    serverFile = open('storedServers.txt',"w+")
    for x in serverList:
        serverFile.write(str(x.server) + "|" + str(x.submitable) + "|" + str(x.announceChannel) + "\n")
    
    serverFile.close()
    
    await client.send_message(message.channel, "Saved successfully!")

#automatic save
async def save():

    #save the stanzas to a file
    saveFile = open('storedStanzas.txt',"w+")
    for x in stanzaList:
        saveFile.write(x.content + "|" + str(x.position) + "|" + str(x.author) + "|" + str(x.server) + "|" + str(x.active) + "|" + str(x.SID) +"\n")

    saveFile.close()
    
    #save the server settings in a file
    serverFile = open('storedServers.txt',"w+")
    for x in serverList:
        serverFile.write(str(x.server) + "|" + str(x.submitable) + "|" + str(x.announceChannel) + "\n")
    
    serverFile.close()

#loads the server stuff
def load():
    #load user stanzas from file
    storedStanzas = [line.rstrip('\n') for line in open('storedStanzas.txt')]
    
    #for each line
    for x in storedStanzas:
        
        #split each line by the |
        newContent,newPosition,newAuthor,newServer,newActive,newSID = x.split("|")

        #make and asign the new properties to the stanza and add it to the database
        newStanza = stanza()
        newStanza.content = newContent
        newStanza.position = newPosition
        newStanza.author = newAuthor
        newStanza.server = newServer
        if newActive == "True":
            newStanza.active = True
        else:
            newStanza.active = False
        newStanza.SID = newSID

        stanzaList.append(newStanza)
        
    #load server options

    storedOptions = [line.rstrip('\n') for line in open('storedServers.txt')]

    for y in storedOptions:
        newServer, newSubmit, newAnnounce = y.split("|")
        newOptions = options()
        newOptions.server = newServer
        if newSubmit == "True":
            newOptions.submitable = True
        else:
            newOptions.submitable = False
        newOptions.announceChannel = newAnnounce

        serverList.append(newOptions)
        
    #load helpTxt
    helpFile = [line.rstrip('\n') for line in open('helpTxt.txt')]
    
    for x in helpFile:
        commandName, commandHelp = x.split("|")
        commandHelp = commandHelp.replace('\\n','\n')
        helpTxtList.update({commandName:commandHelp})

#clears up server options and sets up the serverList
async def initialize(client, message, strippedMessage):
    if str(message.author.id) == botOwner:
        for x in client.servers:
            newOptions = options()
            newOptions.server = x.id
            serverList.append(newOptions)
        
        await client.send_message(message.channel, "Server List initialized")

#allows moderators to manage the submitted stanzas on the server
async def view(client, message, strippedMessage):
    
    #set the server condition to the current server the message is in
    server = message.server.id
    adminMode = False

    #set up the editList from the stanzaList
    editList = []
    #for each stanza in the list
    for x in stanzaList:
        
        #if the stanza was made on the server
        if x.server == server:
            
            #add it to the edit pool
            editList.append(x)

    #set up the conditions for the program to use
    userCondition = ""
    activeCondition = ""
    positionCondition = ""
    
    #check to see if theres anything in the first message
    if len(strippedMessage) != 0:
        
        #if ~a was used and the author of the message was the bot owner
        if (strippedMessage[0] == "~a") and (str(message.author.id) == botOwner):
            
            #enable admin mode
            adminMode = True

    #if the author is a mod or admin mode was enabled
    if(message.author.server_permissions.ban_members) or adminMode:
        command = True

        #while the menu is still being used:
        while(command):
            
            #send a table displaying the current conditions made
            await client.send_message(message.channel, "Conditions for search:\nPosition = " + positionCondition + "\nActive = " + str(activeCondition) +" \nUser = " + userCondition + "\nPlease set the conditions for search (Type ``condition argument``), ``abort`` to abort the search, or ``begin`` to start the search")
            
            #wait for a message from the user that starts with position, active, user, abort, and begin
            ret = await client.wait_for_message(
            timeout=30,
            check=lambda m: (
            m.author == message.author and 
            m.channel == message.channel and
            (m.content.startswith("position") or m.content.startswith("active") or m.content.startswith("user") or m.content.startswith("abort") or m.content.startswith("begin"))
            )
            )
            
            #if a message is returned
            if ret != None:
                
                #split up the message
                reply = shlex.split(ret.content)
                #print(reply)
                
                #if the first part of the message is "Position"...
                if reply[0].lower() == "position":
                    
                    #and the second part is a valid number
                    if(reply[1] == "1" or reply[1] == "2" or reply[1] == "3"):
                        
                        #set the position condition to the number
                        positionCondition = reply[1]
                    
                    #if its "clear"
                    if(reply[1].lower() == "clear"):
                        
                        #clear the position condition out
                        positionCondition = ""
                
                #if the first part is active...
                if reply[0].lower() == "active":
                    
                    #and the second part is false
                    if reply[1].lower() == "false":
                        
                        #set the condition to false
                        activeCondition = False
                    
                    #and the second part is true
                    if reply[1].lower() == "true":
                        
                        #set the condition to true
                        activeCondition = True
                    
                    #and the second part is clear
                    if reply[1].lower()== "clear":
                        
                        #clear out the activeCondition
                        activeCondition = ""
                
                #if the first part is User
                if reply[0].lower() == "user":
                    
                    #and the second part is not clear
                    if reply[1].lower() != "clear":
                        
                        #extract the user id from the mention
                        userCondition = re.search("<@!?([0-9]{17,18})>", reply[1])
                        userCondition = userCondition.group(1)
                    
                    #if the reply is clear
                    else:
                        
                        #clear out the user condition
                        userCondition = ""
                
                #if the reply is abort
                if reply[0].lower() == "abort":
                    
                    #stop the loop and notify the user
                    command = False
                    await client.send_message(message.channel, "aborting search")

                #if the reply is begin
                if reply[0].lower() == "begin":
                    
                    #stop the loop and begin the viewEditList command
                    command = False
                    await viewEditList(client, message, userCondition, activeCondition, positionCondition, editList)
            
            #timeout message
            else:
                
                #stop the loop and notify the user
                command = False
                await client.send_message(message.channel, "Timed out, aboring search")

#second part of the view command               
async def viewEditList(client, message, userCondition, activeCondition, positionCondition, editList):
    
    #if the user condition is not blank:
    if userCondition != "":
        
        #for each stanza in the editList
        for x in editList:
            
            #if the author of the stanza doesnt match the user condition
            if x.author != userCondition:
                #remove it from this list
                #print(str(x.SID) + " removed")
                editList.remove(x)
    
    #if the active condition is not blank            
    if activeCondition != "":
        
        #for each stanza in the list
        for x in editList:

            #if the active condition doesnt match with the stanzas active condition
            if x.active != userCondition:
                #remove it from the list
                #print(str(x.SID) + " removed")
                editList.remove(x)
    
    #if the positionCondition is not blank:          
    if positionCondition != "":
        
        #for each stanza in the edit list
        for x in editList:
            
            #if the stanza position doesnt match the position condition
            if x.position != positionCondition:
                
                #remove it from the list
                #print(str(x.SID) + " removed")
                editList.remove(x)
    
    #while the menu is still in use
    command = True
    while(command):
        
        #set up the index and chart variable
        index = 1
        chart = ""
        
        #if theres something in the edit list
        if len(editList) != 0:
            
            #add the stanzas to the chart that will be sent to the user
            chart += "``position|content|user|active``\n"
            for x in editList:
                chart += str(str(index) + ".) " + str(x.position) + " | " + str(x.content) + " | " + str(x.author) + " | " + str(x.active) + "\n")
                index += 1
            
            ##send the chart as well as instructions
            await client.send_message(message.channel, chart)
            await client.send_message(message.channel, "Please choose the stanza you want to edit or delete (command, index):\n ``delete``, ``toggle``, ``done``")
            
            #wait for a message from the user that starts with done, toggle, or delete
            ret = await client.wait_for_message(
                timeout=60,
                check=lambda m: (
                m.author == message.author and 
                m.channel == message.channel and
                (m.content.startswith("done") or m.content.startswith("toggle") or m.content.startswith("delete"))
                )
                )
            
            #if the user sends a message
            if ret != None:
                
                #split up the message
                reply = shlex.split(ret.content)

                #print(reply)

                #if the message had more then one argument
                if len(reply) > 1:
                    
                    #turn the second part into a number
                    selected = int(reply[1])
                    selected = selected - 1
                    
                    #if the number is within the edit list range
                    if selected >= 0 and selected <= len(editList):
                        
                        #print(selected)
                        #print(editList[selected].SID)
                        
                        #and the first part is toggle:
                        if  reply[0] == "toggle":
                            
                            #get the stanza from the list
                            stanza = editList[selected]
                            #print(str(stanza.active))
                            
                            #go through the list and toggle the active property
                            for x in editList:
                                if x.SID == stanza.SID:
                                    #print(str(x.active))
                                    x.active ^= True
                                    #print(str(x.active))
                           
                        #and the first part is delete
                        if  reply[0] == "delete":
                            
                            #get the stanza...
                            stanza = editList[selected]
                            
                            #and remove it from both lists
                            stanzaList.remove(stanza)
                            editList.remove(stanza)
                
                #if the first part is done
                if reply[0] == "done":
                    
                    #stop using the menu and end the command
                    command = False
                    await client.send_message(message.channel, "Done editing")
            
            #timeout message
            else:
                command = False
                await client.send_message(message.channel, "Timed out, aboring search")
        
        #no stanzas present in editlist
        else:
            command = False
            await client.send_message(message.channel, "No stanzas present on list, aborting view")

#globally bans a user from using the bot
async def botBan(client, message, strippedMessage):
    if str(message.author.id) == botOwner and len(strippedMessage) != 0:
        user = re.search("<@!?([0-9]{17,18})>", strippedMessage[0])
        user = user.group(1)
        print(user)
        botBanList.append(user)
        await client.send_message(message.channel, "User has been banned")

#removes a user from the global ban list
async def unBotBan(client, message, strippedMessage):
    if len(strippedMessage) != 0:
        user = re.search("<@!?([0-9]{17,18})>", strippedMessage[0])
        if str(message.author.id) == botOwner and (user in botBanList):
            botBanList.remove(user)
            await client.send_message(message.channel, "User has been unbanned")

#gives the option of modifying some of the options available
async def optionView(client, message, strippedMessage):
    
    adminMode = False

    if len(strippedMessage) != 0:
        
        #if ~a was used and the author of the message was the bot owner
        if (strippedMessage[0] == "~a") and (str(message.author.id) == botOwner):
            
            #enable admin mode
            adminMode = True

    #if the author is a mod or admin mode was enabled
    if(message.author.server_permissions.ban_members) or adminMode:
        #for each server in the server list
        for x in serverList:
            
            #if the server id the message came from matches the one in the list
            if message.server.id == str(x.server):
                
                #take the options and make it its own variable
                currentOptions = x
                
                #while the menu is in use
                command = True
                while(command):
                    
                    #send a list of available options
                    await client.send_message(message.channel, "Bot Options:\n Able to ``submit`` stanzas: " + str(currentOptions.submitable))
                    
                    #wait for a message from the user
                    ret = await client.wait_for_message(
                        timeout=60,
                        check=lambda m: (
                        m.author == message.author and 
                        m.channel == message.channel and
                        (m.content.startswith("done") or m.content.startswith("toggle"))
                        )
                        )
                        
                    #if the user sends a message
                    if ret != None:
    
                        #split the message up
                        reply = shlex.split(ret.content)
    
                        #print(reply)
                        
                        #if theres more then one part to the message
                        if len(reply) > 1:
                            
                           #if the first part of the reply is toggle
                            if  reply[0] == "toggle":
                                
                                #and the second part is submit
                                if reply[1] == "submit":
                                    
                                    #toggle the submittable option 
                                    currentOptions.submitable ^= True
                        
                        #if the first part is done
                        if reply[0] == "done":
                            
                            #close the menu and command
                            command = False
                            await client.send_message(message.channel, "Done editing options")
                            break
    
                    #timeout message
                    else:
                        command = False
                        await client.send_message(message.channel, "Timed out, aboring options")
                        break

#close down the bot
async def close(client, message, strippedMessage):
    if str(message.author.id) == botOwner:
        await save()
        await client.send_message(message.channel, "ded")
        sys.exit(0)        

#do the load function on startup 
load()

#command list available
commandList = {"hello":hello,"credits":credit,"haiku":haiku,"help":helpTxt, "submit":submit, "view":view, "botban":botBan,
"unbotban":unBotBan, "options":optionView, "save":saveMessage, "initialize":initialize, "close":close, "tothestars": haiku}   


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await periodicSave(client)

    
    

client.run(token)
