#! /usr/bin/env python

import email, getpass, imaplib, os, re

pattern_uid = re.compile('\d+ \(UID (?P<uid>\d+)\)')

def parse_uid(data):
    match = pattern_uid.match(data)
    return match.group('uid')

detach_dir = '.' # directory where to save attachments (default: current)
user = raw_input("Enter your GMail username:")
pwd = getpass.getpass("Enter your password: ")

# connecting to the gmail imap server
m = imaplib.IMAP4_SSL("imap.gmail.com")
m.login(user,pwd)
#print m.list()
m.select("[Gmail]/Trash") # here you a can choose a mail box like INBOX instead
# use m.list() to get all the mailboxes

resp, items = m.search(None, "ALL") # you could filter using the IMAP rules here (check http://www.example-code.com/csharp/imap-search-critera.asp)
items = items[0].split() # getting the mails id

if len(items):
    print '------------About to move messages'
    
    for emailid in items:
        # First get UID
        resp, data = m.fetch(emailid, "(UID)")
        msg_uid = parse_uid(data[0])    
        
        # Log email summary data
        resp, data = m.fetch(emailid, "(RFC822)") # fetching the mail, "`(RFC822)`" means "get the whole stuff", but you can ask for headers only, etc
        email_body = data[0][1] # getting the mail content
        mail = email.message_from_string(email_body) # parsing the mail content to get a mail object
        
        print "["+mail["From"]+"] :" + mail["Subject"] , 
        
        result = m.uid('COPY', msg_uid, 'zzzz_toArchive')
        if result[0] == 'OK':
            mov, data = m.uid('STORE', msg_uid , '+FLAGS', '(\Deleted)')
            m.expunge()
            print " - SUCCESS"
        else:
            print " - FAIL"


    print '------------Done'
