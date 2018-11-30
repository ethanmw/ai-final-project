#!/usr/bin/env python3
import sys
import praw
import argparse
import markovify
import requests.packages.urllib3

def reader(input_file):
	with open(input_file, "r", encoding="utf-8") as input_file:
		contents = input_file.read()
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

def run_bot(r, input_file_weight_pairs):
	for comment in r.subreddit('aww').comments(limit=1): #adds a comment to first 5 posts in /r/aww subreddit
		#print comment
		chainreply = generatecomment(input_file_weight_pairs) #creates the comment from markov chain
		#print(chainreply)
		#comment.reply("This is so cute!") #posts the comment

def parse_command_line():
	parser = argparse.ArgumentParser()

	parser.add_argument("-i", "--input-file",
						action="append",
						dest="input_files",
						required=True)

	parser.add_argument("-w", "--weight",
						type=float,
						action="append",
						dest="weights",
						required=True)

	arguments = parser.parse_args()
	return arguments

if __name__ == ("__main__"):
	arguments = parse_command_line()
	input_files = arguments.input_files
	weights = arguments.weights

	# print("input_files: {}".format(input_files))
	# print("weights {}".format(weights))

	if len(input_files) is not len(weights):
		raise ValueError("must specify the same number of input files and weights")

	input_file_weight_pairs = []
	for i in range(0,len(input_files)):
		input_file_weight_pairs.append((input_files[i],weights[i]))

	requests.packages.urllib3.disable_warnings()
	reddit_instance = praw.Reddit(client_id="K5g9kvLpRnbxiQ",
								client_secret="hRAt7B4HRxqoebJadbnVoxE_n98",
								user_agent="erinhh:v1 (by /u/erinhh)",
								username="erinhh",
								password="NDFightingIrish2019")
	run_bot(reddit_instance, input_file_weight_pairs)

