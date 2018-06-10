#! /usr/bin/env python

import email
import getpass
import imaplib
import os
import re
import sys
import time

pattern_uid = re.compile(r"\d+ \(UID (?P<uid>\d+)\)")

def parse_uid(data):
    match = pattern_uid.match(str(data))
    if match:
        return match.group("uid")
    else:
        return match

detach_dir = "." # directory where to save attachments (default: current)

try:
    from credentials import credentials_list
except:
    credentials_list = [{
        "user": raw_input("Enter your GMail username:"),
        "password": getpass.getpass("Enter your password: "),
        "from_address": "me@example.com",
    },]

# connecting to the gmail imap server
for cred in credentials_list:
    m = imaplib.IMAP4_SSL("imap.gmail.com")
    m.login(cred["user"], cred["password"])
    #print m.list()
    m.select("[Gmail]/Trash") # here you a can choose a mail box like INBOX instead
    # use m.list() to get all the mailboxes

    # you could filter using the IMAP rules here
    # (check http://www.example-code.com/csharp/imap-search-critera.asp)
    resp, items = m.search(None, "ALL")
    items = items[0].split() # getting the mails id

    ERROR_STRING = "ERROR OF SOME SORT"
    FAIL_STRING = "FAIL"
    if len(items):
        try:
            results_string = ''
            results_string += "------------About to move messages\n"

            for emailid in items:
                # First get UID
                resp, data = m.fetch(emailid, "(UID)")
                msg_uid = parse_uid(data[0])

                if msg_uid:
                    # Log email summary data
                    # fetching the mail, "`(RFC822)`" means "get the whole stuff",
                    # but you can ask for headers only, etc
                    resp, data = m.fetch(emailid, "(RFC822)")
                    email_body = data[0][1] # getting the mail content
                    # parsing the mail content to get a mail object
                    mail = email.message_from_string(email_body)


                    results_string += ("["+str(mail["From"])+"] :"
                                       + str(mail["Subject"]))

                    result = m.uid("COPY", msg_uid, "zzzz_toArchive")
                    if result[0] == "OK":
                        mov, data = m.uid("STORE", msg_uid, "+FLAGS", "(Deleted)")
                        m.expunge()
                        results_string += " - SUCCESS\n"
                    else:
                        results_string += " - %s  (%s)\n" % (FAIL_STRING, str(result))
                else:
                    results_string += ("UNABLE TO MOVE/COPY... ["
                                       + str(mail["From"]) + "] :"
                                       + str(mail["Subject"]))
            results_string += "------------Done\n"
            print results_string
            new_message = email.message.Message()
            new_message["From"] = cred["from_address"]
            new_message["Subject"] = "Messages moved from trash to archive"
            new_message.set_payload(results_string)
            m.append("INBOX", "", imaplib.Time2Internaldate(time.time()),
                     str(new_message))
        except ValueError as exc:
            print("Caught exception: %s" % str(exc))
            print(ERROR_STRING)
        finally:
            if ERROR_STRING in results_string or FAIL_STRING in results_string:
                sys.exit(1)
            else:
                sys.exit(0)
