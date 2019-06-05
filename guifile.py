
import sys
import os
import pprint
import pyzmail
import numpy
import imapclient

from emailfile import sensitiveInfo, emailInfo, login
from datastructfile import addingEtoD, summing, ascendingDescending
from outputfile import rawOutputToFile, dictOutPutToFile

def mainmenu(mailServer, sumDict, sortDict, emailDict, rawMessage, rawUIDs, inboxPath):
    os.system("clear")
    print("Main Menu\n")
    printToTerminal(sumDict, sortDict)
    print("Please chose an option on how to use this program")
    
    try:
        while True:
            rawinuser = input("-> ")

            if len(rawinuser) < 1:
                rawinuser = "NaN"
            
            inuser = rawinuser.split()
            command = str(inuser[0]).lower()

            if command in ('v', 'view'):
                view(mailServer, sumDict, sortDict, emailDict, rawMessage, rawUIDs, inboxPath)

            elif command in ('d', 'del', 'delete'):
                delete(mailServer, sumDict, sortDict, emailDict, rawMessage, rawUIDs, inboxPath)

            elif command in ('e', 'exit'):
                exiting(mailServer)

            elif command in ('h', 'help'):
                helping(mailServer, sumDict, sortDict, emailDict, rawMessage, rawUIDs, inboxPath)

            elif command in ('r', 'ref', 'refresh'):
                refresh(mailServer, sumDict, sortDict, emailDict, rawMessage, rawUIDs, inboxPath)

            elif command in ('a', 'asc'):
                changeOrder(mailServer, sumDict, sortDict, emailDict, rawMessage, rawUIDs, inboxPath, True)

            elif command in ('desc'):
                changeOrder(mailServer, sumDict, sortDict, emailDict, rawMessage, rawUIDs, inboxPath, False)

            elif command in ('print', 'p'):
                printDicts(rawMessage, rawUIDs, emailDict)

    except KeyboardInterrupt:
        exiting(mailServer)

def view(mailServer, sumDict, sortDict, emailDict, rawMessages, rawUIDs, inboxPath):
    os.system("clear")
    print("View\n")
    printToTerminal(sumDict, sortDict)
    print("Please use various commands to view emails from an address")

    while True:
        rawinuser = input("-> ")
        
        if len(rawinuser) < 1:
            rawinuser = "NaN"

        inuser = rawinuser.split()

        command = str(inuser[0]).lower()

        if len(inuser) > 1:
            number = int(inuser[1])
            sender = str(inuser[2]).capitalize()

        if (len(inuser) is 3) and sender not in emailDict.keys():
            print("No address by that name")
        else:
            if command in ("m", "mm", "main", "menu"):
                mainmenu(mailServer, sumDict, sortDict, emailDict, rawMessages, rawUIDs, inboxPath) 
            elif command in ('quit', 'q', 'exit', 'e'):
                exiting(mailServer)
            elif (command in ("first", "f", "recent", "r", "last", "l")) and (len(inuser) is 3):
                getInfo(emailDict, sender, command, number, rawMessages, rawUIDs)

def delete(mailServer, sumDict, sortDict, emailDict, rawMessages, rawUIDs, inboxPath):
    os.system("clear")
    print("Delete\n")

    printToTerminal(sumDict, sortDict)
    print("Please use various commands to delete emails from an address")

    while True:
        rawinuser = input("-> ")
        
        if len(rawinuser) < 1:
            rawinuser = "NaN"

        inuser = rawinuser.split()

        command = str(inuser[0]).lower()

        if len(inuser) > 1:
            if command in ("first", "f", "recent", "r", "last", "l"):
                number = int(inuser[1])
                sender = str(inuser[2])
            elif command in ("a", "all"):
                number = None
                addresses = inuser[1:]
                sender = []
                for address in addresses:
                    sender.append(address.capitalize())

        if (len(inuser) > 0):
            if command in ("m", "mm", "main", "menu"):
                mainmenu(mailServer, sumDict, sortDict, emailDict, rawMessages, rawUIDs, inboxPath)
            elif command in ('quit', 'q', 'exit', 'e'):
                exiting(mailServer)
            elif (command in ("first", "f", "recent", "r", "last", "l", "a", "all")) and (len(inuser) >= 2):
                if command in ("first", "f", "recent", "r", "last", "l"):
                    
                    if sender not in emailDict.keys():
                        print("No address by that name")
                        return

                    getInfo(emailDict, sender, command, number, rawMessages, rawUIDs)
                    print("Delete these emails?")
                    
                    outcome = yesNo()
                    if outcome is True:
                        deleteEmails(mailServer, emailDict, sender, command, number, inboxPath)
                        refresh(mailServer, sumDict, sortDict, emailDict, rawMessages, rawUIDs)

                elif command in ("a", "all"):

                    print("Delete all emails from {} ?".format(sender))

                    outcome = yesNo()
                    if outcome is True:
                        for address in sender:
                            deleteEmails(mailServer, emailDict, address, command, number, inboxPath)

def exiting(mailServer):
    os.system("clear")
    print("Exiting Program")
    mailServer.logout()
    sys.exit()

def helping(mailServer, sumDict, sortDict, emailDict, rawMessages, rawUIDs, inboxPath):
    os.system("clear")
    print("Help")

    out = '''
        This is the Deleting and Email Viewing Automating System. There are a
        number of different commands and features that can be used for this
        program outlined below

        View -> (v, view) 
            Allows you to view a number of emails based on commands given

            [Relevance][number][address]

            [Relevance Commands]
            First/F
                The first number of emails from a specified email address
            Recent/R/Last/L
                The last/most recent number of emails from a specified 
                email address

        Delete -> (d, del, delete)
            Allows you to delete a number of emails based on commands given

            [Relevance][number][address]

            [Relevance Commands]
            First/F
                The first number of emails from a specified email address
            Recent/R/Last/L
                The last/most recent number of emails from a specified 
                email address
            All/A
                All emails from a specified email address

        Help -> (h, help)
            The help screen that displays all commands available

        Refresh -> (r, refresh)
            Allows the use to refresh the list of emails, useful for when 
            you want to delete and then view different emails from the same 
            address

        Ascending -> (a, asc)
            Changes the ordering of the list on the main menu

        Descending -> (desc)
            Changes the ordering of the list on the main menu
        
        Main Menu -> (Main/Menu/M/MM)
            Available on all screens to revert back to the main menu
        
        Exit -> (Quit/Q/Exit/E)
    '''

    print(out)

    while True:
        rawinuser = input("-> ")
        
        if len(rawinuser) < 1:
            rawinuser = "NaN"

        inuser = rawinuser.split()
        command = str(inuser[0]).lower()

        if len(inuser) > 1:
            number = int(inuser[1])

        if command in ("m", "mm", "main", "menu"):
            mainmenu(mailServer, sumDict, sortDict, emailDict, rawMessages, rawUIDs, inboxPath)
        elif command in ('quit', 'q', 'exit', 'e'):
            exiting(mailServer)

def printDicts(rawMessages, rawUIDs, emailDict):
    rawOutputToFile(rawMessages, rawUIDs)
    dictOutPutToFile(emailDict)

def refresh(mailServer, sumDict, sortDict, emailDict, rawMessages, rawUIDs, inboxPath):
    os.system("clear")
    print("Refreshing")

    mailServer.logout()

    username, password, app_pass = sensitiveInfo()
    server, port = emailInfo()
    mailServer, inboxPath, rawMessages, rawUIDs  = login(server, username, app_pass)
    
    emailDict = addingEtoD(rawMessages, rawUIDs)
    
    sumDict = summing(emailDict)
    sortDict = ascendingDescending(sumDict, True)

    os.system("clear")
    print("Refreshed\n")
    
    mainmenu(mailServer, sumDict, sortDict, emailDict, rawMessages, rawUIDs, inboxPath)

def changeOrder(mailServer, sumDict, sortDict, emailDict, rawMessages, rawUIDs, inboxPath, asc):
    os.system("clear")
    sortDict = ascendingDescending(sumDict, asc)
    mainmenu(mailServer, sumDict, sortDict, emailDict, rawMessages, rawUIDs, inboxPath)

def printToTerminal(sumDict, sortDict):

    top = sortDict[:100]

    for key, value in zip(top, sumDict.items()):
        if len(value) > 1:
            for value in list(sumDict[key]):
                v = str(value).replace("'", "")
                title = v.strip("[]")

                print(str(title) + " [" + str(key) + "]")
        else:
            v = str(value).replace("'", "")
            title = v.strip("[]")

            print(str(title) + " [" + str(key) + "]")
    
    print("\n")

def getInfo(emailDict, sender, relevance, number, rawMessages, rawUIDs):

    if relevance in ('first', 'f'):
        start = 0
        uidlist = list(emailDict[sender])
        cut = uidlist[:number]
    elif relevance in ('recent', 'r', 'last', 'l'):
        start = len(emailDict[sender])
        uidlist = list(emailDict[sender])
        cut = uidlist[-number:]
    
    print("\n")

    for i in cut:
        message = pyzmail.PyzMessage.factory(rawMessages[i][b'BODY[]'])
        
        subject = message.get_subject()
        froma = message.get_address('from')
        toa = message.get_address('to')


        print("Subject: " + subject)
        print("From: " + str(froma))
        print("To: " + str(toa) + "\n")

def yesNo():

    while True:

        rawinuser = input("(Y/n) -> ")
        inuser = rawinuser.split()
        if len(inuser) < 1:
            inuser = " "
        else:
            inuser = str(inuser[0]).lower()

        if inuser[0] in (" ", "y", "yes"):
            return True
        elif inuser[0] in ("n", "no"):
            return False 

def deleteEmails(mailServer, emailDict, sender, relevance, number, folderPath):
    
    mailServer.select_folder(folderPath, readonly=False)
    print(folderPath)

    if relevance in ('first', 'f'):
        start = 0
        uidlist = list(emailDict[sender])
        cut = uidlist[:number]
    elif relevance in ('recent', 'r', 'last', 'l'):
        start = len(emailDict[sender])
        uidlist = list(emailDict[sender])
        cut = uidlist[-number:]
    elif relevance in ('all', 'a'):
        cut = list(emailDict[sender])
    

    for uid in cut:
        print(uid)
        mailServer.delete_messages(uid)
        print(mailServer.get_flags(uid))
        mailServer.expunge()

    mailServer.select_folder(folderPath, readonly=True)
