import configparser as cfg
import imaplib
import pprint

import imapclient

# fetches the sensitive info from the config
def sensitiveInfo():
    conf = cfg.ConfigParser()

    conf.read("config (copy).ini")

    user = conf["email info"]["from_email"]
    app_pass = conf["email sens info"]["app_pass"]

    return user, app_pass

# fetches the email info from the config
def emailInfo():
    conf = cfg.ConfigParser()

    conf.read("config (copy).ini")

    smtp_ser = conf["email info"]["smtp_server"]
    smtp_port = conf["email info"]["smtp_port"]

    return smtp_ser, smtp_port

# logs in the user to the gmail server
def login(server, user, app_pass):
    mailServer = imapclient.IMAPClient(server, ssl=True)
    imaplib._MAXLINE = 10000000
    print(user, app_pass)
    mailServer.login(user, app_pass)

    pprint.pprint(mailServer.list_folders())

    mailServer.select_folder('[Google Mail]/All Mail', readonly=True)
    inboxPath = '[Google Mail]/All Mail'
    
    rawUIDs = mailServer.search('All')
    rawMessages = mailServer.fetch(rawUIDs, ['BODY[]'])


    return mailServer, inboxPath, rawMessages, rawUIDs
