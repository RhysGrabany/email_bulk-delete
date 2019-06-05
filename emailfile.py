import configparser as cfg
import imaplib
import pprint

import imapclient


def sensitiveInfo():
    conf = cfg.ConfigParser()

    conf.read("config.ini")

    user = conf["email info"]["from_email"]
    passw = conf["email sens info"]["from_pass"]
    app_pass = conf["email sens info"]["app_pass"]

    return user, passw, app_pass

def emailInfo():
    conf = cfg.ConfigParser()

    conf.read("config.ini")

    smtp_ser = conf["email info"]["smtp_server"]
    smtp_port = conf["email info"]["smtp_port"]

    return smtp_ser, smtp_port

def login(server, user, app_pass):
    mailServer = imapclient.IMAPClient(server, ssl=True)
    imaplib._MAXLINE = 10000000
    mailServer.login(user, app_pass)

    pprint.pprint(mailServer.list_folders())


    #if ('[Google Mail]/All Mail') not in mailServer.list_folders():
    #    mailServer.select_folder('[Gmail]/All Mail', readonly=True)
    #    inboxPath = '[Gmail]/All Mail'
    #else:
    mailServer.select_folder('[Google Mail]/All Mail', readonly=True)
    inboxPath = '[Google Mail]/All Mail'
    
    rawUIDs = mailServer.search('All')
    rawMessages = mailServer.fetch(rawUIDs, ['BODY[]'])


    return mailServer, inboxPath, rawMessages, rawUIDs