#!/usr/bin/python3

from emailfile import sensitiveInfo, emailInfo, login
from datastructfile import addingEtoD, summing, ascendingDescending
from guifile import mainmenu, printToTerminal

# save variables from config file
username, password, app_pass = sensitiveInfo()
server, port = emailInfo()

# login using sensitive info 
mailServer, inboxPath, rawMessages, rawUIDs  = login(server, username, app_pass)

# add raw emails to a dictionary
emailDict = addingEtoD(rawMessages, rawUIDs)

# counting number of emails and adding to a dictionary
sumDict = summing(emailDict)
# sort the emails from most-least
sortDict = ascendingDescending(sumDict, True)

# moving to the mainmenu
mainmenu(mailServer, sumDict, sortDict, emailDict, rawMessages, rawUIDs, inboxPath)
