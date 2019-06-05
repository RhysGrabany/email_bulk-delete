import pyzmail
from collections import defaultdict


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

def summing(dict):

    sumDict = defaultdict(list)
    for k, v in dict.items():
        
        listd = list(dict[k])
        sum = len(listd)
        sumDict[sum].append(k)

        sum = 0

    return sumDict

def ascendingDescending(dict, asc):

    if asc is True:
        sort = sorted(dict.keys(), reverse=True)
    elif asc is False:
        sort = sorted(dict.keys(), reverse=False)
    
    return sort

