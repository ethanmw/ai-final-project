#!/usr/bin/env python3
import sys
import praw
import markovify
import requests.packages.urllib3

def usage():
	print('Usage: {} {}'.format('erinhhbot.py inputfile'))
	exit()
def bot_login():
	r = praw.Reddit(client_id = '82TduHVnWOFMyg',client_secret = '5NpSiJGJSZS1XT7AV3j8sg1iByo',user_agent = '<console:ERINHH:0.0.1 (by /u/mcavanag>',username='mcavanag',password = 'AIproject')
	#print 'Hello World'
	return r

def reader(inputfile):
	with open(inputfile, "r") as file:
		contents = file.read()
	return contents

def buildchain(text, chain = {}):
	chain = markovify.NewlineText(text)
	return chain

def generatecomment(inputfile):
	t = reader(inputfile)
	commentchain = buildchain(t)
	sentence = commentchain.make_sentence(tries = 100)
	print(sentence)
	return sentence	

def run_bot(r, file):
	for comment in r.subreddit('aww').comments(limit=1): #adds a comment to first 5 posts in /r/aww subreddit
		#print comment
		chainreply = generatecomment(file) #creates the comment from markov chain
		#print chainreply
		#comment.reply("This is so cute!") #posts the comment


if __name__ == ("__main__"):
	args = sys.argv[1:]
	if len(args) != 1:
		usage()
	inputfile = args[0]
	requests.packages.urllib3.disable_warnings()
	r = bot_login()
	run_bot(r, inputfile)

