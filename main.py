## Boring API imports and setup ###
import os
import discord
import random
from keep_alive import keep_alive

TOKEN = os.environ['TOKEN']

intents = discord.Intents(messages=True, guilds=True, message_content=True, reactions=True)

client = discord.Client(intents=intents)
####################################


### Here's the dictionary which will contain "bugs" and the problems that they are associated with. This will be updated with each project, and hopefully this time people will actually log bugs in this dictionary. But realistaclly that's wishful thinking... ###

## IMPORTANT: Should you ever need to restart the bot, dm it "!print" to have it print out the dictionary so that you can save it. Otherwise, the bugs stored in the dictionary will be lost!

methodsDict = {}

# Here are the old methodsDict values from last year! We can maybe reuse them or alternatively it's fun to go back and relive all the most painful bugs. Remember Cheatle? Good times.
"""
DYNAMIC PROGRAMMING:

{
  'LoHiStress': ["If you're shooting just a bit high on the tester, make sure you aren't taking a high stress job on the last day!"],
  'ScavHunt': ["Keep in mind that it should be impossible for the largest possible point value starting at time A to be less than time B if time A is before time B. Double check that your array is set up so that scaveHunt[0] isn't the greatest possible point value IF YOU DO THE FIRST ACTIVITY but instead the greatest point value OVERALL.", "No helper methods with for loops >:(. Think of the poor big O..."],
  'CookieMonster': ["The grid won't always be square!"]
}"""

"""
HUFFMAN:

{'HuffmanCodeGenerator Constructor': ['We have learned about both BufferedReaders and Scanners for reading text from a file. Choose carefully!', "Mr. Stout gets the frequencies of chars that aren't in the file. So you need to store frequency counts for all chars with ascii values up to 128! This will show up as a null pointer exception in the tester."], 'getFrequency()': ['Check the constructor! This should be a one line method!'], 'HuffmanNode Class' : ['To be able to store the nodes in a PriorityQueue, it needs to implement Comparable!', 'The default Comparable interface requires a compareTo(Object o) method. But we don\'t want to compare to just any object, we want to compare to HuffmanNodes. The Comparable interface allows specification to avoid this problem! For instance, instead of implementing Comparable you can implement Comparable<HuffmanNode> and only have to write a compareTo(HuffmanNode o)'], 'getCode()':['🥳 recursion!!! 🥳\nLike all recursion problems, remember to start with 1) a base case and 2) a recursive step. Trees are a recursive datastructure - use this to your advantage!'], 'makeTree()':['you only need to store the head of your tree! That\'s the beauty of trees!'], "No clue what happened this is a nightmare...": ["Is your code spitting out really weird characters? Check that you're using UTF-8"]}
"""

"""
CHEATLE:

{'beginGame()': ['array = otherArray is bad'], 'makeGuess()': ['double counting letters!!', "when you are updating your possible list/tree/hashThingy, if you are using a for each loop, don't delete inside the for each loop. It will recognize that the indexes all got shifted and freak out and crash."], 'isAllowable()': ["you didn't add the solutions to your allowable guesses in the constructor!", 'check your reset function. Mr Stout wrote his tester so that it resets before testing isAllowable()'], 'constructor': ["make sure you add the possible solutions to your possible guesses list --> it's counter intuitive, but wordle doesn't do that naturally"], 'toString()': ["it doesn't exist lol"], 'numGuesses()': [], 'numRemaining()': ['check your isAllowable function and wherever you update your possibleSolutions list (probably makeGuess?)']}"""


# filter out python slander... but hopefully this feature will never need to be used >:)
illegal = [
"bad", 
"sucks", 
"terrible",
"awful",
"worse",
"atrocious",
"monstrosity", 
"SUCKS", 
"java is better",
"worst", 
"BAD", 
"SUCKS", 
"TERRIBLE",
"AWFUL",
"WORSE",
"ATROCIOUS",
"MONSTROSITY",
"hate", 
"HATE",
"screw",
"SCREW",
"gross",
"GROSS",
"ew",
"EW",
"abysmal",
"ABYSMAL"
]

## More boring setup stuff to start the code ##
@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
###############################################

  
## Setting up variables. There's a lot of stuff to keep track of, and I don't want to explain every boolean. However the general idea is that when someone calls the command for "hey I have a question" the bot sets a boolean so that it knows that it's waiting to hear the user's question and then appends that question to a list. Same for... well, all the other features. Lots and lots of booleans and pending lists.
questions = {}
pendingQuestions = {}
waiting = False
authorName = ""
settingUp = False
admin = ["Noman#8525", "dragonstout#1047"]
adminID = [1012891586251735150, 0]
mods = ["Noman", "clairebear", "Obsol", "TheCaptain157", "exoskeleton"]
mods2 = ["clairebear#5674", "Obsol#2212", "TheCaptain157#0073", "exoskeleton#1729"]
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
currentHelp = 0
adminChannel = client.get_channel(1012891586251735150)
helpedCounter = 0
waitingReview = []
waitingForQuote = False
quoteAuthor = ""
prevNum = 0
pendingBugs = []
pausedChannels = []
###########################


## Ah, the infamous stout quotes feature. This year I'm not doing images because those were too hard to maintain and difficult for people to submit. As genius as putting "I'm a baby killer. -Mr. Stout" on a picture of a child in a raincoat was, we're using a text file this time so that the process of adding quotes can be easily automated. ##



"""stoutImages = ['StoutQuoteImages/StoutQuote1.png', 'StoutQuoteImages/StoutQuote2.png', 'StoutQuoteImages/StoutQuote3.png', 'StoutQuoteImages/StoutQuote4.png', 'StoutQuoteImages/StoutQuote5.png', 'StoutQuoteImages/StoutQuote6.png', 'StoutQuoteImages/StoutQuote7.png', 'StoutQuoteImages/StoutQuote8.png',
'StoutQuoteImages/StoutQuote9.PNG',
'StoutQuoteImages/StoutQuote10.jpg.png',
'StoutQuoteImages/StoutQuote11.png']"""


## OK, this function will trigger any time someone puts an emoji on a message. This will let us use emojis as buttons! ##
@client.event
async def on_raw_reaction_add(payload):
  # Debug code. 
  print(payload)
  #############

  ## There's almost certainly a better way to do this than what I'm doing here but I did it and I'm too lazy to redo it so we're stuck with 6 global variables. ##
  global currentHelp
  global adminChannel
  global helpedCounter
  global waitingReview
  global answering
  global pausedChannels
  ##################################################################################

  ## This makes sure the computer doesn't trigger itself. Otherwise we get some nasty infinite loops and no one wants that ##
  # NOTE: EVERY TIME YOU MAKE A NEW BOT USING THIS SOURCE CODE, YOU MUST CHANGE THIS USER_ID
  if payload.user_id == 1012929070130024510:
    return
  #################################################################################
  messageID = payload.message_id

  ## You can never be too safe... Never have used this feature, and hopefully never will. ##
  if payload.emoji.name == "⌛" and payload.member.name in mods:
    pausedChannels.append(client.get_channel(payload.channel_id))
    embed=discord.Embed(title="This channel has been temporarily paused because it was flagged as making people uncomfortable", color=discord.Color.red())
    await client.get_channel(payload.channel_id).send(embed=embed)
    print(pausedChannels)
  ####################################################################
  
  ## This part of the code does the main help function, and it's very convoluted. Buckle up! ##
  emojis = ["zero", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

  # If this message is someone who JUST ASKED for help and the emoji is selecting a bug, select that bug
  # This way each help message can only be triggered once
  if messageID == currentHelp and payload.emoji.name in emojis:
    currentHelp = 0
    counter = 1

    # print the bugs
    embed=discord.Embed(title="Bugs:", color=discord.Color.blue())
    print(emojis.index(str(payload.emoji.name)))
    for methodName in methodsDict.keys():
      if counter == emojis.index(str(payload.emoji.name)):
        print("YES")
        for bug in methodsDict[methodName]:
          embed.add_field(name=":beetle:", value=bug, inline=False)
      counter += 1
    channel = client.get_channel(payload.channel_id)
    print(channel)
    await channel.send(embed = embed)
    """user = await client.fetch_user(adminID[0])
    print(user)
    await user.send(embed = embed)"""
    helpedCounter += 1

  # This part is where the admins review the bugs. These approval messages will pop up in the admin channel to make sure that nobody tries to abuse the bot to cheat. #
  for message in waitingReview:
    if message[0] == payload.message_id:
      user = await client.fetch_user(message[3])
      if payload.emoji.name == "✅":

        try: 
          methodsDict[message[1]].append(message[2])
        except:
          methodsDict[message[1]] = [message[2]]

        # Confirm approval to the user who submitted it
        embed=discord.Embed(title="Congrats! Your bug was accepted!", color=discord.Color.blue())
        await user.send(embed = embed)
        
        # Confirm approval to the admins
        embed=discord.Embed(title="Bug approved!", color=discord.Color.gold())
        await adminChannel.send(embed = embed)

      # Same thing but this time we reject the bug
      else:
        embed=discord.Embed(title="Uh oh... Your bug was declined. Thanks anyways though!", color=discord.Color.red())
        await user.send(embed = embed)
        embed=discord.Embed(title="Bug denied!", color=discord.Color.gold())
        await adminChannel.send(embed = embed)

      # Reset waitingReview
      waitingReview.remove(message)
      return

  # This lets the admin pick which question they're answering
  if payload.message_id == respondingMessage:
    try:
      num = emojis.index(payload.emoji.name) - 1
    except:
      return

    counter = 0
    for q in pendingQuestions.keys():
      if counter == num:
        answering = [q, pendingQuestions[q]]
        embed=discord.Embed(title="Answering the question: " + q, color=discord.Color.gold())
        await client.get_channel(payload.channel_id).send(embed = embed)
        del pendingQuestions[q]
        break
      counter += 1
      

  

respondingMessage = 0
answering = []
awaitingQuestions = []

# when a message is sent...
@client.event
async def on_message(message):

  ## Here we go again... I really should be more organized ##
  global adminChannel
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
  global currentHelp
  global stoutQuotes
  global waitingForQuote
  global quoteAuthor
  global pendingBugs
  global prevNum
  global pendingQuestions
  global questions
  global awaitingQuestions
  global respondingMessage
  global answering
  global pausedChannels
  global mods2
  global methodsDict
  ##################################################

  print(message)
  print(message.content)
  
  # we don't want to respond to our own messages! That's a bug waiting to happen
  if message.author == client.user:
    return

  # End of the pause channel feature
  if message.content.startswith('!unpause') and message.author in admin or message.author in mods2:
    embed = discord.Embed(title="This channel has now been unpaused", color=discord.Color.green())
    for channel in pausedChannels:
      await channel.send(embed=embed)
    pausedChannels = []
    
  if message.channel in pausedChannels:
    try:
      await message.delete()
    except:
      pass
    
  # Sending the answer to a question
  if str(message.author) in admin and answering != []:
    questions[answering[0]] = message.content
    embed=discord.Embed(title="Check #responses in the server - your question was just answered!!", color=discord.Color.gold())
    await answering[1].send(embed = embed)
    embed=discord.Embed(title="question answered", color=discord.Color.gold())
    await message.channel.send(embed = embed)
    answerChannel = client.get_channel(1012891534544338965)
    embed=discord.Embed(title="Question: " + answering[0], color=discord.Color.gold())
    embed.add_field(name=message.content, value="answer submitted by " + str(message.author), inline=False)
    # Sometimes we'll be able to submit the answer as an embed. Other times it goes over the text limit.
    try: 
      await answerChannel.send(embed = embed)
    except:
      embed1=discord.Embed(title="Question: " + answering[0], color=discord.Color.gold())
      await answerChannel.send(embed=embed1)
      try:
        embed=discord.Embed(title=message.content+"\nanswer submitted by " + str(message.author), color=discord.Color.gold())
        await answerChannel.send(embed=embed)
      except:
        embed=discord.Embed(title="Answer submitted by" +str(message.author), color=discord.Color.gold())
        await answerChannel.send(embed=embed)
        await answerChannel.send(message.content)
    answering = []
    
    
  # Responding to questions
  if str(message.author) in admin and message.content.startswith('!respond'):
    embed=discord.Embed(title="Pending questions:", color=discord.Color.gold())
    
    emojis = ["zero", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

    counter = 1
    
    for q in pendingQuestions.keys():
      embed.add_field(name=emojis[counter] + " " + q, value=pendingQuestions[q].name, inline=False)
      counter += 1
    
    compMessage = await message.channel.send(embed = embed)
    
    for i in range(counter):
      if i != 0:
        print(emojis[i])
        await compMessage.add_reaction(emojis[i])

    respondingMessage = compMessage.id


  if len(awaitingQuestions) > 0:
    counter = 0
    for q in awaitingQuestions:
      if message.author == q[0] and message.channel == q[1]:
        pendingQuestions[message.content] = q[0]
        print(pendingQuestions)
        embed=discord.Embed(title="Question submitted ✅", color=discord.Color.blue())
        await message.channel.send(embed = embed)

        print (message.channel.id)

        questionChannel = client.get_channel(1012891427165966378)
        embed=discord.Embed(title=message.content, color=discord.Color.blue())
        await questionChannel.send(embed = embed)
        awaitingQuestions.remove(q)
        counter += 1
        break
        

  # Asking questions – sends to admin channel
  if message.content.startswith('!ask'):
    try:
      
      await message.delete()
      embed=discord.Embed(title=":red_square::red_square::red_square:\n Please use dm's to ask questions! This is because we want to allow questions to stay anonymous (to other students) and don't want the channels to become too cluttered!", color=discord.Color.red())
      await message.channel.send(embed = embed)
      return
    except:
      pass
    embed=discord.Embed(title="What is your question?", color=discord.Color.blue())
    await message.channel.send(embed = embed)
    awaitingQuestions.append([message.author, message.channel])
    print(awaitingQuestions)


  ## SHHHHHHHHH this code detection stops the cheaters, but if people know how it works I'm sure they'll find ways to get around it. Or alternatively they'll send images... but there's not much we can do about that. Anyways, at the very least no code will be copy-pastable ##
  if any (word in message.content for word in ["public", "if", "int", "String", "try", "new", "for (", "{", "return", "while", "\n"]):
    if ";" in message.content:
      censorString = ""
      counter = 0
      for letter in message.content:
        if counter % 3 == 0:
          censorString += "🟥"
        if letter == "\n":
          censorString += "🟥\n"
          counter = 0
        counter += 1
      await message.delete()
      try:
        embed=discord.Embed(title=censorString + "\nThis message has been censored because it looked like it could contain code. Friendly reminder to make sure you don't copy paste!",   color=discord.Color.red())
        await message.channel.send(embed = embed)
      except:
        await message.channel.send("***This message has been censored because it looked like it could contain code. Friendly reminder to make sure you don't copy paste!***")
        await message.channel.send(censorString)
  
  # Link to the github project! 
  if message.content.startswith('!source') and str(message.author) in admin:
    embed=discord.Embed(title="Source Code", url = "https://github.com/AlwaysUsePython/Community-Coding-Bot/tree/main",  color=discord.Color.gold())
    await message.channel.send(embed = embed)
    embed=discord.Embed(title="Repl Join Link", url = "https://replit.com/join/idhylmxjwm-elliotlichtman",  color=discord.Color.gold())
    await message.channel.send(embed = embed)

  # This feature was on the old version of the bot and it would remind about the help feature, but more often than not it would only either rub salt in wounds or trigger randomly out of nowhere. So It's gone now.
  """
  if any(word in message.content for word in needsHelp):
    embed=discord.Embed(title="Sounds like you need some help! Remember: if you type !help, I'll try my best! :thumbsup:", color=discord.Color.blue())
    #await message.channel.send(embed = embed)"""

  # Stout quotes. The least productive feature, but also the most used feature. All this is 100% renovated
  if message.content.startswith('!stout'):

    stoutQuotes = []

    file = open("stout_quotes", "r")

    for quote in file:
      stoutQuotes.append(quote[0:len(quote)-1])
      
    
    randomNum = prevNum
    while randomNum == prevNum:
      randomNum = random.randint(0, len(stoutQuotes)-1)
    print(randomNum)
    quote = "\"" + stoutQuotes[randomNum] + "\"\n- Mr. Stout"
    embed=discord.Embed(title=quote, color=discord.Color.green())
    await message.channel.send(embed=embed)

    prevNum = randomNum

    file.close()

  if message.content.startswith('!submit'):

    file = open("stout_quotes", "a")


    quoteIndexes = []
    counter = 0 
    for letter in message.content:
      if letter == "\"":
        quoteIndexes.append(counter)
      counter += 1

    try:
      string = message.content[quoteIndexes[0]+1:quoteIndexes[1]] + "\n"
    except:
      string = ""
    
    if string != "":
      file.write(string)

    file.close()

    embed=discord.Embed(title="Thank you for your submission!", color=discord.Color.green())
    await message.channel.send(embed=embed)

    

  
  ## The most helpful feature of them all, by a LONG SHOT. I think I got everything, but feel free to add datastructures/objects if they come up! ##
  # Here's the template for adding something new:
  """
  if any(word in message.content for word in [LIST ALL THE WAYS THEY MIGHT TYPE THE NAME OF THE THING]):
    embed = discord.Embed(title="NAME OF THE THING", url = "LINK TO JAVA ORACLE DOCS", color=discord.Color.green())
    embed.add_field(name="Syntax:", value="ALL THE RELEVANT SYNTAX")
    embed.add_field(name="Important Methods:", value="ALL THE IMPORTANT METHODS", inline=False)
    embed.add_field(name="Efficiency:", value="EFFICIENCY STATS", inline=False)
    await message.channel.send(embed=embed)
  """
    
  if message.content.startswith('!syntax'):
    print("syntax")
    if any(word in message.content for word in ["BufferedReader", "buffered reader", "Buffered reader", "bufferedreader", "bufferedReader"]):
      embed=discord.Embed(title="BufferedReader", url="https://docs.oracle.com/javase/8/docs/api/java/io/BufferedReader.html", color=discord.Color.green())
      embed.add_field(name = "Syntax:", value="import java.io.BufferedReader;\nBufferedReader reader = new BufferedReader(new FileReader(fileName));\nreader.ready() to see if there's a next character\n(char)reader.read(); to read the next character\nREMEBER TO reader.close() AT THE END!!!")
      await message.channel.send(embed=embed)
    elif any(word in message.content for word in ["Scanner", "scanner"]):
      embed=discord.Embed(title="Scanner", url="https://docs.oracle.com/javase/8/docs/api/java/util/Scanner.html", color=discord.Color.green())
      embed.add_field(name = "Syntax:", value="import java.util.Scanner;\nScanner reader = new Scanner(newFile(fileName));\n reader.hasNext() to see if there's a next word\nreader.next() to read the next character\nreader.nextLine() to read the next line")
      await message.channel.send(embed=embed)
    elif any(word in message.content for word in ["PrintWriter", "print writer", "Print writer", "printwriter", "printWriter"]):
      embed=discord.Embed(title="PrintWriter", url="https://docs.oracle.com/javase/8/docs/api/java/io/PrintWriter.html", color=discord.Color.green())
      embed.add_field(name = "Syntax:", value="import java.io.PrintWriter;\nimport java.io.FileWriter;\nPrintWriter out = new PrintWriter(new FileWriter(fileName));\nout.print(); to write\nREMEBER TO out.close() AT THE END!!!")
      await message.channel.send(embed=embed)
    elif any(word in message.content for word in ["ArrayList", "arrayList", "array list", "Array List", "arraylist"]):
      embed=discord.Embed(title="ArrayList", url = "https://docs.oracle.com/javase/7/docs/api/java/util/ArrayList.html",  color=discord.Color.green())
      embed.add_field(name = "Syntax:", value="import java.util.ArrayList;\nArrayList<ObjectType> variableName = new ArrayList<ObjectType>();", inline=False)
      embed.add_field(name="Important Methods:", value="add(value)\nget(index)\nsize()", inline=False)
      embed.add_field(name="Efficiency:", value="Adding: O(1) --> worst case O(n)\nGetting: O(1)\nRemoving: O(n)", inline=False)
      await message.channel.send(embed = embed)
    elif any(word in message.content for word in ["Priority Queue", "PriorityQueue", "priority queue", "priorityQueue", "priorityqueue"]):
      embed=discord.Embed(title="PriorityQueue", url = "https://docs.oracle.com/javase/7/docs/api/java/util/PriorityQueue.html",  color=discord.Color.green())
      embed.add_field(name = "Syntax:", value="import java.util.PriorityQueue;\nPriorityQueue<E> pq = new PriorityQueue<E>();", inline=False)
      embed.add_field(name="Important Methods:", value="add(value)\npeek(index)\nsize()", inline=False)
      embed.add_field(name="Efficiency:", value="Adding: O(log(n))\nGetting (limited): O(1)", inline=False)
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
      embed.add_field(name = "Syntax:", value="import java.util.LinkedList;\nLinkedList<valueType> variableName = new LinkedLIst<valueType>();", inline=False)
      embed.add_field(name="Important Methods:", value="add(value)\nsize()\nremove(Object) or remove(index)\ngetFirst()\ngetLast()", inline=False)
      embed.add_field(name="Efficiency:", value="Adding: O(1)\nGetting: O(n)\nRemoving: O(1)", inline=False)
      await message.channel.send(embed = embed)
    else:
      embed=discord.Embed(title="!syntax",url = "https://learnpython.com/blog/python-or-java/", color=discord.Color.green())
      embed.add_field(name = "ERROR datastructure not found exception", value="please type !syntax followed by the name of the datastructure you want. Some examples:\n - ArrayList\n - HashMap\n - TreeSet\n - LinkedList\n - PriorityQueue\n - PrintWriter\n - BufferedReader\n - Scanner", inline=False)
      await message.channel.send(embed=embed)
  
  if message.content.startswith('!info'):
    embed=discord.Embed(title="Hi!!!! I'm here to help you find the bugs in your code!" , color=discord.Color.green())
    embed.add_field(name="How I work:", value="I store a database of all the errors people in the DnD community have been encountering. When you are stuck, type !help and select the method you're working on and I'll give you a list of some potential bugs you might have!", inline=False)
    embed.add_field(name="Logging Bugs", value="To add a bug, type the !bug command and follow my instructions! The bug will be reviewed by an admin, but here are some general guidelines:\n - make it easy to identify so that people can recognize which bugs are in their own code\n - explain the problem in a helpful way but don't give your solution! the beauty of computer science (and the honor code) is seeing how everyone attacks the problem differently!\n - under absolutely NO circumstance should you send a fixed line of code for people to copy paste. That is not what this bot is for.", inline=False)
    embed.add_field(name="Honor Code", value="The honor code is important, so my brilliant creator added in a few features to make sure that I don't become a problem! Every bug that gets added has to get approved by an admin first, and I have some built in code to detect and block people sending copy pastable code snippets. Hopefully I can be a great resource but still stay fully within the rules set by the Computer Science department!", inline=False)
    embed.add_field(name="Privacy", value="I anticipate that many people may (understandably) have reservations about asking a bot for help on a group server. So, if you dm me !help, I'll respond in dms! Also any questions submitted using the !ask feature will be anonymous when posted in public channels but the teacher who reads the question will be able to see who submitted it.", inline=False)
    await message.channel.send(embed = embed)


  if str(message.author) not in admin:
    for i in range(len(pendingBugs)):
      if pendingBugs[i][0] == message.channel.id and pendingBugs[i][2]:
        print(pendingBugs[i])
        adminChannel = client.get_channel(1012891586251735150)
        embed=discord.Embed(title="Bug Submission From "+ str(message.author), color=discord.Color.gold())
        embed.add_field(name="Method Name", value=pendingBugs[i][3], inline=False)
        embed.add_field(name="New Bug", value=message.content, inline=False)
        adminMessage = await adminChannel.send(embed = embed)
        await adminMessage.add_reaction("✅")
        await adminMessage.add_reaction("❌")
        waitingReview.append([adminMessage.id, pendingBugs[i][3], message.content, message.author.id])
        embed=discord.Embed(title="Bug submitted for review", color=discord.Color.blue())
        await message.channel.send(embed = embed)
        print(methodsDict)
        del pendingBugs[i]
        print(pendingBugs)
  if str(message.author) not in admin:
    for i in range(len(pendingBugs)):
      if pendingBugs[i][0] == message.channel.id and pendingBugs[i][1]:
        print("match")
        pendingBugs[i].append(message.content)
        pendingBugs[i][1] = False
        pendingBugs[i][2] = True
        authorName = admin
        embed=discord.Embed(title="You have selected " + message.content + "\nWhat is the bug?", color=discord.Color.blue())
        await message.channel.send(embed = embed)
    
  if message.content.startswith('!bug') and str(message.author) not in admin:
    try:
      await message.delete()
      embed=discord.Embed(title=":red_square::red_square::red_square: Please use dm's to add bugs to the database! This is for honor code reasons because we want to give Mr. Stout a chance to censor bugs before they become public!",   color=discord.Color.red())
      await message.channel.send(embed = embed)
      return
    except:
      pass
    embed=discord.Embed(title="Type the name of the method:", color=discord.Color.blue())
    await message.channel.send(embed = embed)
    authorName = message.author
    pendingBugs.append([message.channel.id, True, False])
    print(pendingBugs)

  if message.content.startswith('!print') and str(message.author) in admin:
    print(methodsDict)

  if message.content.startswith('!reset') and str(message.author) in admin:
    print(methodsDict)
    methodsDict = {}
    embed=discord.Embed(title="Bugs Reset", color=discord.Color.gold())
    await message.channel.send(embed = embed)

  
  if appendingBug and str(message.author) in admin:
    for i in range(len(pendingBugs)):
      if pendingBugs[i][0] == message.channel.id:
        appendingBug = False
        try:
          methodsDict[pendingBugs[i][1]].append(message.content)
        except:
          methodsDict[pendingBugs[i][1]] = [message.content]
        embed=discord.Embed(title="Bug added", color=discord.Color.gold())
        await message.channel.send(embed = embed)
        print(methodsDict)
        pendingBugs.remove(pendingBugs[i])
        break
  
  if addingBug and str(message.author) in admin:
    for i in range(len(pendingBugs)):
      if pendingBugs[i][0] == message.channel.id:
        pendingBugs[i].append(message.content)
        addingBug = False
        appendingBug = True
        authorName = admin
        embed=discord.Embed(title="You have selected " + pendingBugs[i][1] + "\nWhat is the bug?", color=discord.Color.gold())
        await message.channel.send(embed = embed)
        break
    
  if message.content.startswith('!bug') and str(message.author) in admin:
    embed=discord.Embed(title="Type the name of the method:", color=discord.Color.gold())
    await message.channel.send(embed = embed)
    authorName = message.author
    addingBug = True
    pendingBugs.append([message.channel.id])
    
  """# basically gives them which thing they want
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
      
    await message.channel.send(embed = embed)"""
  
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
    compMessage = await message.channel.send(embed = embed)
    currentHelp = compMessage.id
    emojis = ["zero", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
    for i in range(counter):
      if i != 0:
        print(emojis[i])
        await compMessage.add_reaction(emojis[i])

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
    print(message.author.id)
    embed=discord.Embed(title="What is the new method called?", color=discord.Color.gold())
    await message.channel.send(embed = embed)
    authorName = message.author
    settingUp = True

  if any (word in message.content for word in ["python", "Python", "PYTHON"]):
    if any(word in message.content for word in illegal):
      embed=discord.Embed(title=":octagonal_sign: WARNING: Python slander is not tolerated :snake:",     color=discord.Color.red())
      await message.channel.send(embed = embed)


keep_alive()
try:
  client.run(TOKEN)
except:
  os.system("kill 1")

