import pyzmail
from collections import defaultdict

# adds the raw emails to the dictionary
def addingEtoD(rawMessages, rawUIDs):
    
    emailDict = defaultdict(list)

    for uid in rawUIDs:
        mess = pyzmail.PyzMessage.factory(rawMessages[uid][b'BODY[]'])
        fromRaw = mess.get_address("from")[0]
    
        stripped = fromRaw.strip()
        firstword = stripped.split()[0]
        fromA = firstword.capitalize()

        emailDict[fromA].append(uid)
    
    return emailDict

# adds up the emails in the dictionary and saves the result
def summing(dict):

    sumDict = defaultdict(list)
    for k, v in dict.items():
        
        listd = list(dict[k])
        sum = len(listd)
        sumDict[sum].append(k)

        sum = 0

    return sumDict

# changes order of the output
def ascendingDescending(dict, asc):

    if asc is True:
        sort = sorted(dict.keys(), reverse=True)
    elif asc is False:
        sort = sorted(dict.keys(), reverse=False)
    
    return sort

