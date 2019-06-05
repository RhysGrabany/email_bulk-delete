#!/usr/bin/python3

from emailfile import sensitiveInfo, emailInfo, login
from datastructfile import addingEtoD, summing, ascendingDescending
from guifile import mainmenu, printToTerminal

username, password, app_pass = sensitiveInfo()
server, port = emailInfo()
mailServer, inboxPath, rawMessages, rawUIDs  = login(server, username, app_pass)

emailDict = addingEtoD(rawMessages, rawUIDs)

sumDict = summing(emailDict)
sortDict = ascendingDescending(sumDict, True)

mainmenu(mailServer, sumDict, sortDict, emailDict, rawMessages, rawUIDs, inboxPath)
