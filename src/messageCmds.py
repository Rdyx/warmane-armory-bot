#!/usr/bin/env python
# -*- coding: utf-8 -*-

def aboutMessage(author):
    repoUrl = 'https://github.com/Rdyx/warmane-armory-bot'

    return """Hello **{}**, I'm very glad to see you have invited me to your discord!
My source code is totally open and available at **{}** ! :)
If you have any trouble, find a bug, want to do a suggestion, feel free to send a message to my creator **@Rdyx#7572**
""".format(author, repoUrl)


def welcomeMessage(guildsNumber, author):
    return """Hey **{}**! Thank you for your invitation, you're the **#{}** guild to invite me! :D 
I hope you\'ll find my services usefull for you and your mates!
Start with `$$help` if you want to know the commands and `$$help [command]` to have some informations on how to use a specific one :)
Have fun!
""".format(author, guildsNumber)