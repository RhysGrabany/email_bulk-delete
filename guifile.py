
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
    
    # the input pathway for the program
    # if the user wishes to exit using keyboard interrupt, then the progam logsout 
    try:
        while True:
            rawinuser = input("-> ")

            # input checking
            if len(rawinuser) < 1:
                rawinuser = "NaN"
            
            inuser = rawinuser.split()
            command = str(inuser[0]).lower()

            # the various options allowed
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
        # logging out for keyboard interrupt
        exiting(mailServer)

def view(mailServer, sumDict, sortDict, emailDict, rawMessages, rawUIDs, inboxPath):
    os.system("clear")
    print("View\n")
    printToTerminal(sumDict, sortDict)
    print("Please use various commands to view emails from an address")

    # same sort of input menu
    # try-catch block not needed since it is in the main method
    while True:
        rawinuser = input("-> ")
        
        if len(rawinuser) < 1:
            rawinuser = "NaN"

        inuser = rawinuser.split()

        command = str(inuser[0]).lower()

        if len(inuser) > 1:
            number = int(inuser[1])
            sender = str(inuser[2]).capitalize()

        # checking if email is in the raw email dictionary
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
            # choosing emails based on relevance
            if command in ("first", "f", "recent", "r", "last", "l"):
                number = int(inuser[1])
                sender = str(inuser[2])
            # or just selecting all emails
            elif command in ("a", "all"):
                number = None
                addresses = inuser[1:]
                sender = []
                for address in addresses:
                    sender.append(address.capitalize())

        # input based on number of characters
        if (len(inuser) > 0):
            if command in ("m", "mm", "main", "menu"):
                mainmenu(mailServer, sumDict, sortDict, emailDict, rawMessages, rawUIDs, inboxPath)
            elif command in ('quit', 'q', 'exit', 'e'):
                exiting(mailServer)
            elif (command in ("first", "f", "recent", "r", "last", "l", "a", "all")) and (len(inuser) >= 2):
                if command in ("first", "f", "recent", "r", "last", "l"):
                    
                    # check if email is in the raw email dictionary
                    if sender not in emailDict.keys():
                        print("No address by that name")
                        return

                    # a check if they want to delete the emails selected and print the emails in focus
                    getInfo(emailDict, sender, command, number, rawMessages, rawUIDs)
                    print("Delete these emails?")
                    
                    outcome = yesNo()
                    if outcome is True:
                        deleteEmails(mailServer, emailDict, sender, command, number, inboxPath)
                        refresh(mailServer, sumDict, sortDict, emailDict, rawMessages, rawUIDs)

                # delete emails in bul
                elif command in ("a", "all"):

                    # delete emails from the list of emails address stored in sender
                    print("Delete all emails from {} ?".format(sender))

                    outcome = yesNo()
                    if outcome is True:
                        for address in sender:
                            # email delete method
                            deleteEmails(mailServer, emailDict, address, command, number, inboxPath)

# logging out
def exiting(mailServer):
    os.system("clear")
    print("Exiting Program")
    mailServer.logout()
    sys.exit()

# method for the help screen
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

# print th dictionaries to file
# raw contains the uids of the emails
# emaildict contains the number of emails for each address
def printDicts(rawMessages, rawUIDs, emailDict):
    rawOutputToFile(rawMessages, rawUIDs)
    dictOutPutToFile(emailDict)

# refresh logs out the user then logs them back in and reverts back to main menu
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

# change the ascending/descending nature of the emails on the main menu
def changeOrder(mailServer, sumDict, sortDict, emailDict, rawMessages, rawUIDs, inboxPath, asc):
    os.system("clear")
    sortDict = ascendingDescending(sumDict, asc)
    mainmenu(mailServer, sumDict, sortDict, emailDict, rawMessages, rawUIDs, inboxPath)

# print the emails to the terminal
def printToTerminal(sumDict, sortDict):

    # only prints the top 100
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

# fetches the info for a selection of emails
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
        # this makes it look nicer and prints the subject, from address, and to address
        message = pyzmail.PyzMessage.factory(rawMessages[i][b'BODY[]'])
        
        subject = message.get_subject()
        froma = message.get_address('from')
        toa = message.get_address('to')


        print("Subject: " + subject)
        print("From: " + str(froma))
        print("To: " + str(toa) + "\n")

# user input for the email deleting
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

# deleting the actual emails from the server
def deleteEmails(mailServer, emailDict, sender, relevance, number, folderPath):
    
    # moves readonly to false
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
        mailServer.delete_messages(uid)
        mailServer.expunge()

    # moves readonly back to true
    mailServer.select_folder(folderPath, readonly=True)
