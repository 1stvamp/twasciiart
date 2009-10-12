#!/usr/bin/env python

from twitter import Api
import sys
import time
import re
import getopt

def usage():
    print """twasciiart.py accepts text sent via stdin, with optional arguments:
echo "test" | ./twasciiart.py -u user42 -p somepass123 [-l -d]
-u --username : twitter username
-p --password : twitter password
-l --length : maximum post length (default 140)
-ll --linelength : maximum line length (default 80)
-d --delay : delay between tweets (default 120 seconds)
-t --tag : optional hash to prepend (don't include the hash symbol, #)
-n --linenumber : number of lines to split on, if used twasciiart will attempt
to stuff input into a single tweet separated by carriage returns
-r --replacer : character to replace whitespace with (default ".")
"""

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "u:p:l:ll:d:t:n:r:", ["username=", "password=",
            "length=", "linelength=", "delay=", "tag=", "linenumber=",
            "replacer="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    username = None
    password = None
    length = 140
    line_length = 80
    delay = 120
    tag = ""
    line_number = None
    replacer = "."
    for opt, arg in opts:
        if opt in ("-u", "--username"):
            username = arg
        elif opt in ("-p", "--password"):
            password = arg
        elif opt in ("-l", "--length"):
            length = arg
        elif opt in ("-ll", "--linelength"):
            length = arg
        elif opt in ("-d", "--delay"):
            delay = arg
        elif opt in ("-t", "--tag"):
            tag = arg
        elif opt in ("-n", "--linenumber"):
            line_number = arg
        elif opt in ("-r", "--replacer"):
            replacer = arg
    if not username or not password:
        print "username and password are required"
        usage()
        sys.exit(2)
    tag = (" #%s" % tag) if tag else ""
    length = length - len(tag)
    tweets = []
    tw = Api(username=username, password=password)

    if not len(sys.stdin):
        print "No input from stdin"
        usage()
        sys.exit(2)

    for l in sys.stdin.readlines():
            line = line.sub(r'\s', replacer)
            if len(line) > length:
                    print "Lines too long to fit in a single tweet, change lines (or hashtag if present"
                    usage()
                    sys.exit(2)
            else:
                    tweets.append("%s%s" % (tag, line))

    if tweets:
            for i, tweet in enumerate(tweets):
                    time.sleep(delay)
                    print 'Sending tweet %d of %d: "%s"' % (i, len(tweets), tweet)
                    tw.PostUpdate(tweet)
                    print "Sent!"
    print "Done."

if __name__ == "__main__":
        main(sys.argv[1:])
