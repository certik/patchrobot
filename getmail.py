#! /usr/bin/env python
from optparse import OptionParser
from imaplib import IMAP4_SSL
from email import message_from_string
from ConfigParser import RawConfigParser

def parse_email(x):
    """
    Parses an email.
    x ... an email as a  string

    Returns a dictionary, for example:

    {'date': 'Wed, 20 Aug 2008 15:09:19 +0200', 'from': '"Ondrej Certik"
    <ondrej@certik.cz>', 'subject': 'ad'}

    See the implementation of this method for the list of keys that are
    implemented.
    """
    e = message_from_string(x)
    r = {}
    r["date"] = e["date"]
    r["from"] = e["From"]
    r["subject"] = e["subject"]
    if e.is_multipart():
        raise Exception("Multipart messages are not yet implemented")
    r["body"] = e.get_payload(decode=True)
    return r

def get_emails(server, user, password):
    """
    Logins to the gmail box using imap, returns the list of emails as strings.
    """
    emails = []
    M = IMAP4_SSL(server)
    M.login(user, password)
    try:
        try:
            M.select()
            ok, data = M.search(None, "All")
            if ok != "OK":
                raise Exception("Got wrong response from the server.")
            for num in data[0].split():
                ok, data = M.fetch(num, "(RFC822)")
                email = data[0][1]
                if ok != "OK":
                    raise Exception("Got wrong response from the server.")
                print 'Message %s\n' % (num)
                emails.append(email)
        finally:
            M.close()
    finally:
        M.logout()
    return emails

def run():
    config = RawConfigParser()
    config.read("config")
    server = config.get("account", "server")
    user = config.get("account", "user")
    password = config.get("account", "password")
    print "Downloading emails..."
    l = get_emails(server, user, password)
    print "Parsing..."
    l = [parse_email(x) for x in l]
    print "Formatting output..."

    for e in l:
        print "%20s %10s %s" % (e["from"], e["date"], e["subject"])

def create_config():
    config = RawConfigParser()
    config.add_section("account")
    config.set("account", "server", "imap.gmail.com")
    config.set("account", "user", "patch-robot@sympy.org")
    config.set("account", "password", "set_to_correct_password")
    config.write(open("config", "wb"))
    print "Configuration file 'config' created"

def main():
    usage = """%prog [options] configfile

Create a config file using:

$ %prog -c

Then set the correct password in there and run it with

$ %prog config"""
    parser = OptionParser(usage = usage)
    parser.add_option("-c", action = "store_true", dest = "create",
            default = False, help = "Create a config file")
    options, args = parser.parse_args()
    if options.create:
        create_config()
        return
    if len(args) == 1:
        run()
        return
    parser.print_help()


if __name__ == "__main__":
    main()
