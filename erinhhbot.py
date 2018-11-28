#!/usr/bin/env python3
import sys
import praw
import markovify
import requests.packages.urllib3

def usage():
	print('Usage: {} {}'.format('erinhhbot.py',  'inputfile'))
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

def generatecomment(inputfiles):
	chains = list()
	weights = list()
	for filepair in inputfiles:	
		t = reader(filepair[0])
		commentchain = buildchain(t)
		chains.append(commentchain)
		weights.append(filepair[1])
	model_combo = markovify.combine(chains, weights)
	sentence = model_combo.make_sentence(tries = 100)
	print(sentence)
	return sentence	

def run_bot(r, files):
	for comment in r.subreddit('aww').comments(limit=1): #adds a comment to first 5 posts in /r/aww subreddit
		#print comment
		chainreply = generatecomment(files) #creates the comment from markov chain
		#print chainreply
		#comment.reply("This is so cute!") #posts the comment


if __name__ == ("__main__"):
	args = sys.argv[1:]
	if len(args) < 1:
		usage()


	modelfiles = list()
	second = False
	filepair = ["file.txt", 0]
	for arg in args:
		if second:
			second = False
			try:
				filepair[1] = float(arg)
				modelfiles.append((filepair[0], filepair[1]))
			except:
				print("failed parsing number: {}".format(arg))
				usage()
		else:
			second = True
			filepair[0] = arg
	if second:
		print("wrong number of arguments!")
		usage()


	requests.packages.urllib3.disable_warnings()
	r = bot_login()
	run_bot(r, modelfiles)

