import os
import discord
from keep_alive import keep_alive

TOKEN = os.environ['TOKEN']

client = discord.Client()

methodsDict = {'beginGame()': ['array = otherArray is a nono'], 'makeGuess()': ['double counting letters!!', "when you are updating your possible list/tree/hashThingy, if you are using a for each loop, don't delete inside the for each loop. It will recognize that the indexes all got shifted and freak out and crash."], 'isAllowable()': ["you didn't add the solutions to your allowable guesses in the constructor!", 'check your reset function. Mr Stout wrote his tester so that it resets before testing isAllowable()'], 'constructor': ["make sure you add the possible solutions to your possible guesses list --> it's counter intuitive, but wordle doesn't do that naturally"], 'toString()': ["it doesn't exist lol"], 'numGuesses()': [], 'numRemaining()': ['check your isAllowable function and wherever you update your possibleSolutions list (probably makeGuess?)']}

# filter out python slander (mean statements courtesy of Isaac)
illegal = [
"python bad", 
"python is bad", 
"python sucks", 
"python shit", 
"python terrible",
"python awful",
"python worse than java",
"python simply bad",
"python very bad",
"python atrocious",
"python a monstrosity", 
"python is shit", #this one is courtesy of eric yoon :D
"PYTHON SUCKS"
]

# detect when someone is dying
needsHelp = ["dropping", "sad", "stuck", "need help", "having trouble", "nightmare", "need some help"]

# start the code
@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

waiting = False
authorName = ""
settingUp = False
admin = ["Noman#8525", "dragonstout#1047"]
addingBug = False
toAppend = ""
appendingBug = False
changingName = False
editingName = False
toEdit = ""
changingBug = False
editingBug = False
finalStep = False
bugNum = 0


# when a message is sent...
@client.event
async def on_message(message):
  global authorName
  global waiting
  global settingUp
  global addingBug
  global toAppend
  global appendingBug
  global changingName
  global editingName
  global toEdit
  global changingBug
  global editingBug
  global finalStep
  global bugNum
  
  # we don't want to respond to our own messages! That's a bug waiting to happen
  if message.author == client.user:
    return

  if message.content.startswith('!source') and str(message.author) in admin:
    embed=discord.Embed(title="Source Code", url = "https://replit.com/@ElliotLichtman/DnD-Bot#main.py",  color=discord.Color.gold())
    await message.channel.send(embed = embed)
  
  if any(word in message.content for word in needsHelp):
    embed=discord.Embed(title="Sounds like you need some help! Remember: if you type !help, I'll try my best! :thumbsup:", color=discord.Color.blue())
    await message.channel.send(embed = embed)

  if message.content.startswith('!syntax'):
    if any(word in message.content for word in ["ArrayList", "arrayList", "array list", "Array List", "arraylist"]):
      embed=discord.Embed(title="ArrayList", url = "https://docs.oracle.com/javase/7/docs/api/java/util/ArrayList.html",  color=discord.Color.green())
      embed.add_field(name = "Syntax:", value="import java.util.ArrayList;\nArrayList<ObjectType> variableName = new ArrayList<ObjectType>();", inline=False)
      embed.add_field(name="Important Methods:", value="add(value)\nget(index)\nsize()", inline=False)
      embed.add_field(name="Efficiency:", value="Adding: O(1) --> worst case O(n)\nGetting: O(1)\nRemoving: O(n)", inline=False)
      await message.channel.send(embed = embed)
    elif any(word in message.content for word in ["TreeSet", "treeset", "tree set", "search tree", "Search Tree", "Search tree", "BST", "Binary Tree", "binary tree", "binary search tree", "Binary Search Tree"]):
      embed=discord.Embed(title="TreeSet", url = "https://docs.oracle.com/javase/7/docs/api/java/util/TreeSet.html", color=discord.Color.green())
      embed.add_field(name = "Syntax:", value="import java.util.TreeSet;\nTreeSet<ObjectType> variableName = new TreeSet<ObjectType>();", inline=False)
      embed.add_field(name="Important Methods:", value="add(value)\nclone()\nsize()\nfirst()\nremove(Object)", inline=False)
      embed.add_field(name="Efficiency:", value="Adding: O(log(n))\nGetting: O(log(n))\nRemoving: O(log(n))", inline=False)
      await message.channel.send(embed = embed)
    elif any(word in message.content for word in ["HashMap", "hashmap", "hash map", "Hash map", "Hash Map", "dictionary", "Dictionary"]):
      embed=discord.Embed(title="HashMap", url = "https://docs.oracle.com/javase/7/docs/api/java/util/HashMap.html", color=discord.Color.green())
      embed.add_field(name = "Syntax:", value="import java.util.HashMap;\nHashMap<keyType, valueType> variableName = new HashMap<keyType, valueType>();", inline=False)
      embed.add_field(name="Important Methods:", value="put(key, value)\nsize()\nremove(Object)", inline=False)
      embed.add_field(name="Efficiency:", value="Adding: O(1)\nGetting: O(1)\nRemoving: O(1)", inline=False)
      await message.channel.send(embed = embed)
    elif any(word in message.content for word in ["Linked List", "linked list", "LinkedList", "linkedList", "linkedlist"]):
      embed=discord.Embed(title="LinkedList",url = "https://docs.oracle.com/javase/7/docs/api/java/util/LinkedList.html", color=discord.Color.green())
      embed.add_field(name = "Syntax:", value="import java.util.LinkedList;\nHashMap<keyType, valueType> variableName = new HashMap<keyType, valueType>();", inline=False)
      embed.add_field(name="Important Methods:", value="add(value)\nsize()\nremove(Object) or remove(index)\ngetFirst()\ngetLast()", inline=False)
      embed.add_field(name="Efficiency:", value="Adding: O(1)\nGetting: O(n)\nRemoving: O(1)", inline=False)
      await message.channel.send(embed = embed)
  
  if message.content.startswith('!info'):
    embed=discord.Embed(title="Hi!!!! I'm here to help you find the bugs in your code!" , color=discord.Color.green())
    embed.add_field(name="How I work:", value="I store a database of all the errors people in the DnD community have been encountering. When you are stuck, type !help and select the method you're working on and I'll give you a list of some potential bugs you might have!", inline=False)
    embed.add_field(name="Logging Bugs", value="To add a bug, type the !bug command and follow my instructions! The bug will be reviewed by an admin, but here are some general guidelines:\n - make it easy to identify so that people can recognize which bugs are in their own code\n - explain the problem in a helpful way but don't give your solution! the beauty of computer science (and the honor code) is seeing how everyone attacks the problem differently!\n - under absolutely NO circumstance should you send a fixed line of code for people to copy paste. That is not what this bot is for.", inline=False)
    embed.add_field(name="Honor Code", value="The honor code is important, so my brilliant creator added in a few features to make sure that I don't become a problem! Every bug that gets added has to get approved by an admin first, and I have some built in code to detect and block people sending copy pastable code snippets. Hopefully I can be a great resource but still stay fully within the rules set by the Computer Science department!", inline=False)
    embed.add_field(name="Privacy", value="I anticipate that many people may (understandably) have reservations about asking a bot for help on a group server. So, if you dm me !help, I'll help you in less public environment!", inline=False)
    await message.channel.send(embed = embed)

  """if admin == "" and message.content.startswith('python is my favorite'):
    admin = message.author
    embed=discord.Embed(title="Congratulations "+ str(message.author) + ".\nYou are admin because you are clearly very wise.", color=discord.Color.gold())
    await message.channel.send(embed = embed)"""

  if appendingBug and str(message.author) in admin:
    appendingBug = False
    try:
      methodsDict[toAppend].append(message.content)
    except:
      methodsDict[toAppend] = [message.content]
    embed=discord.Embed(title="Bug added", color=discord.Color.gold())
    await message.channel.send(embed = embed)
    print(methodsDict)
  
  if addingBug and str(message.author) in admin:
    toAppend = message.content
    addingBug = False
    appendingBug = True
    authorName = admin
    embed=discord.Embed(title="You have selected " + toAppend + "\nWhat is the bug?", color=discord.Color.gold())
    await message.channel.send(embed = embed)
    
  if message.content.startswith('!bug') and str(message.author) in admin:
    embed=discord.Embed(title="Type the name of the method:", color=discord.Color.gold())
    await message.channel.send(embed = embed)
    authorName = message.author
    addingBug = True
    
  # basically gives them which thing they want
  if waiting and message.author == authorName:
    embed=discord.Embed(title="Bugs:", color=discord.Color.blue())
    waiting = False
    counter = 1
    print(message.content)
    for methodName in methodsDict.keys():
      if str(counter) == message.content:
        for bug in methodsDict[methodName]:
          embed.add_field(name=":beetle:", value=bug, inline=False)
      counter += 1
      
    await message.channel.send(embed = embed)
  
  # This will let them search the database!
  if message.content.startswith('!help'):
    words = ["zero", ":one:", ":two:", ":three:", ":four:", ":five:", ":six:", ":seven:", ":eight:", ":nine:", ":keycap_ten:", ":one: :one:", ":one: :two:", ":one: :three:", ":one: :four:", ":one: :five:"]
    embed=discord.Embed(title="Which method are you struggling with?", color=discord.Color.blue())
    counter = 1
    for methodName in methodsDict.keys():
      embed.add_field(name=words[counter] + " " + methodName, value=str(len(methodsDict[methodName])) + " errors logged", inline=False)
     
      counter += 1
    waiting = True
    authorName = message.author
    await message.channel.send(embed = embed)

  # basically gives them which thing they want to edit
  if finalStep and message.author == authorName:
    embed=discord.Embed(title="Bug changed from \""+methodsDict[toEdit][bugNum]+"\" to \""+message.content+"\"", color=discord.Color.gold())
    waiting = False
    methodsDict[toEdit][bugNum] = message.content
      
    await message.channel.send(embed = embed)
    finalStep = False

  if changingBug and message.author == authorName:
    changingBug = False
    for methodName in range(len(methodsDict[toEdit])):
      if str(methodName + 1) == message.content:
        bugNum = methodName
        break
    finalStep = True
    embed=discord.Embed(title="What would you like to change it to?", color=discord.Color.gold())
    await message.channel.send(embed = embed)
    
  # basically gives them which thing they want to edit
  if editingBug and message.author == authorName:
    words = ["zero", ":one:", ":two:", ":three:", ":four:", ":five:", ":six:", ":seven:", ":eight:", ":nine:", ":keycap_ten:", ":one: :one:", ":one: :two:", ":one: :three:", ":one: :four:", ":one: :five:"]
    embed=discord.Embed(title="Which bug?", color=discord.Color.gold())
    waiting = False
    counter = 1
    print(message.content)
    for methodName in methodsDict.keys():
      if str(counter) == message.content:
        toEdit = methodName
        break
      counter += 1
    for methodName in range(len(methodsDict[toEdit])):
      embed.add_field(name=words[methodName+1] + " " + methodsDict[toEdit][methodName], value="___", inline=False)
     
    
    changingBug = True
    authorName = message.author
    editingBug = False
    
    await message.channel.send(embed = embed)
  
  if message.content.startswith('!editBug') and str(message.author) in admin:
    words = ["zero", ":one:", ":two:", ":three:", ":four:", ":five:", ":six:", ":seven:", ":eight:", ":nine:", ":keycap_ten:", ":one: :one:", ":one: :two:", ":one: :three:", ":one: :four:", ":one: :five:"]
    embed=discord.Embed(title="Which method do you want to edit?", color=discord.Color.gold())
    counter = 1
    for methodName in methodsDict.keys():
      embed.add_field(name=words[counter] + " " + methodName, value=str(len(methodsDict[methodName])) + " errors logged", inline=False)
     
      counter += 1
    editingBug = True
    authorName = message.author
    await message.channel.send(embed = embed)


  # basically gives them which thing they want to edit
  if changingName and message.author == authorName:
    embed=discord.Embed(title="Name changed from "+toEdit+" to "+message.content, color=discord.Color.gold())
    waiting = False
    methodsDict[message.content] = []
    print(toEdit)
    for bug in methodsDict[toEdit]:
      methodsDict[message.content].append(bug)
    del methodsDict[toEdit]
      
    await message.channel.send(embed = embed)
    changingName = False
    
  # basically gives them which thing they want to edit
  if editingName and message.author == authorName:
    embed=discord.Embed(title="Type the desired name:", color=discord.Color.gold())
    waiting = False
    counter = 1
    print(message.content)
    for methodName in methodsDict.keys():
      if str(counter) == message.content:
        toEdit = methodName
        break
      counter += 1
    changingName = True
    authorName = message.author
    editingName = False
    
    await message.channel.send(embed = embed)
  
  if message.content.startswith('!editName') and str(message.author) in admin:
    words = ["zero", ":one:", ":two:", ":three:", ":four:", ":five:", ":six:", ":seven:", ":eight:", ":nine:", ":keycap_ten:", ":one: :one:", ":one: :two:", ":one: :three:", ":one: :four:", ":one: :five:"]
    embed=discord.Embed(title="Which method do you want to edit?", color=discord.Color.gold())
    counter = 1
    for methodName in methodsDict.keys():
      embed.add_field(name=words[counter] + " " + methodName, value=str(len(methodsDict[methodName])) + " errors logged", inline=False)
     
      counter += 1
    editingName = True
    authorName = message.author
    await message.channel.send(embed = embed)

  if settingUp and str(message.author) in admin:
    print(message.author)
    settingUp = False
    contained = False
    for key in methodsDict.keys():
      if key == message.content:
        contained = True
    if not contained:
      methodsDict[message.content] = []
      embed=discord.Embed(title="Method added!", color=discord.Color.gold())
      await message.channel.send(embed = embed)
    else:
      embed=discord.Embed(title="That's already in the dictionary!", color=discord.Color.red())
      await message.channel.send(embed = embed)
    print(methodsDict)

  if message.content.startswith('!setup') and str(message.author) in admin:
    embed=discord.Embed(title="What is the new method called?", color=discord.Color.gold())
    await message.channel.send(embed = embed)
    authorName = message.author
    settingUp = True

  if any(word in message.content for word in illegal):
    embed=discord.Embed(title=":octagonal_sign: WARNING: Python slander is not tolerated :snake:",     color=discord.Color.red())
    await message.channel.send(embed = embed)

  
keep_alive()
client.run(TOKEN)
