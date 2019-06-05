import pyzmail

def rawOutputToFile(raw, uids):
    textfile = open("rawoutput.txt", "w")

    for uid in uids:
        mess = pyzmail.PyzMessage.factory(raw[uid][b'BODY[]'])
        fromAd = mess.get_address("from")[0]
        fromA = fromAd.strip()
        output = fromA + " " + str(uid) + "\n"
        textfile.write(output)

def dictOutPutToFile(dict):
    textfile = open("dictoutput.txt", "w")
    for k, v in dict.items():
        output = k + " "
        textfile.write(output)
        for item in list(dict[k]):
            output = str(item) + " "
            textfile.write(output)
        textfile.write("\n")