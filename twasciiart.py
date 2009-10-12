#!/usr/bin/env python

from twitter import Api
import sys
import time 

tag = "#"
length = 140 - (len(tag)+1)
tweets = []
tw = Api(username="", password="")

for l in sys.stdin.readlines():
	line = l.replace("\n", "")
	if "<" not in line:
		line = line.replace(" ", ".")
	if (len(line) + length) < 90:
		line.ljust((90 - (len(line)+length)), ".")
	if len(line) > length:
		print "Lines too long to fit in a single tweet, change lines of hashtag"
		sys.exit(1)
	else:
		tweets.append("%s %s" % (tag, line))

if tweets:
	for tweet in tweets:
		time.sleep(120)
		tw.PostUpdate(tweet)
		print tweet

