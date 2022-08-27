General Idea:

This bot aims to provide an easy way for people to work together on CS projects while staying within the bounds of the honor code. 

The bot stores a database of errors people have encountered (see Bug Submission) in a way that’s easy to access for the community. It will provide a means for people to more easily discover the errors in their code, giving them a list of potential bugs related to a specified method that have caused problems for other people. It will not, however, provide the solution to these bugs – that is for the user to figure out on their own. 

To make sure the bot stays within the honor code, several precautions have been put in place. Bug submissions are regulated by admin who have the power to approve/deny bugs before they go to the database. Furthermore, these admin can edit and remove existing bugs ane methods. In addition to all this, the bot will contain code that scans all messages sent on the server for signs of copy pastable code (semicolons, if{}, etc.) and censor messages it thinks violate the honor code.

Bug Submission

Admin:

Admin can submit any bug in any channel using the !bug command
Their messages will be color coded gold
They will also be able to edit both bugs and method names using !editName and !editBug

Normal Users

To add a bug, non-admin users will have to go through the following process through direct messages with the bot:

1) Normal bug submission input. Same as admin except it is coded BLUE so that it is easy to differentiate


2) The bug will be sent to an admin channel in the larger server that only admins/mods have access to. Here, the teachers/admins can use emojis (naturally placed by the bot) to indicate whether or not the bug should be added.

3) The person who submitted the bug gets a friendly notification telling them either that their bug was approved or that it won’t be added

4) Bugs that got approved will be added to the database while bugs that got denied will not be added.

Helpful Features 

!help - This method is the core of the bot. The user uses reactions to indicate which method they want help on and the bot gives them a list of probable bugs.

!syntax - This method provides a faster way for students to access (cue spooky music) THE DOCS. In addition to linking people to the java oracle docs, this function will provide some basic information about the desired data structure including constructor syntax, common methods, and big O for some crucial tasks.

Question and Answer

In addition to logging bugs, this bot will have a feature to save questions and responses students have about certain methods. There is an !ask command that allows the user to anonymously submit a question to a public Q&A channel. Anyone will be able to respond to the question, however admin will have the power to use the !respond command. This command will allow the admin to select which question they are responding to and isolate the answer in a separate #responses channel. The person who submitted the question will also be notified. 

Why do this instead of just use a normal chat? Well, this is just a nice way to make sure that 1) a teacher's answer doesn't get buried by conversation and 2) students can submit questions anonymously instead of using a group chat.

