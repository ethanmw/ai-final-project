#!/usr/bin/env python3
import sys
import praw
import argparse
import markovify
import utils

def generate_comment(input_file_weight_pairs, state_size):
	'''
	A state_size of n indicates to markovify to consider n-1 words when
	choosing the next word in the sentence it creates.
	'''

	chains = list()
	weights = list()

	for file_weight_pair in input_file_weight_pairs:
		with open(file_weight_pair[0], encoding="utf-8") as input_file:
			comment_chain = markovify.NewlineText(input_text=input_file.read(), state_size=state_size)
			chains.append(comment_chain)
			weights.append(file_weight_pair[1])

	model_combo = markovify.combine(chains, weights)
	return model_combo.make_sentence(tries = 100)


def run_bot(r, input_file_weight_pairs):
	for comment in r.subreddit('aww').comments(limit=1): #adds a comment to first 5 posts in /r/aww subreddit
		#print comment
		chainreply = generate_comment(input_file_weight_pairs) #creates the comment from markov chain
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

	parser.add_argument("-s", "--state-size",
						type=int,
						dest="state_size",
						default=2)

	return parser.parse_args()


if __name__ == ("__main__"):
	arguments = parse_command_line()

	input_files = arguments.input_files
	weights = arguments.weights
	state_size = arguments.state_size

	if len(input_files) is not len(weights):
		raise ValueError("must specify the same number of input files and weights")

	input_file_weight_pairs = []
	for i in range(0,len(input_files)):
		input_file_weight_pairs.append((input_files[i],weights[i]))
	
	reddit_instance = praw.Reddit(client_id="K5g9kvLpRnbxiQ",
								client_secret="hRAt7B4HRxqoebJadbnVoxE_n98",
								user_agent="erinhh:v1 (by /u/erinhh)",
								username="erinhh",
								password="NDFightingIrish2019")

	# run_bot(reddit_instance, input_file_weight_pairs)

	generated_comment = generate_comment(input_file_weight_pairs, state_size)
	print("generated comment: {}".format(generated_comment))

	result = utils.ngram_similarity_absolute(generated_comment, input_files[0], state_size)
	print("the most ngrams that the generated comment shares with a sentence in the corpus is: {}".format(result[0]))
	print("that sentence in the corpus is: {}".format(result[1]))

	result = utils.ngram_similarity_percentage(generated_comment, input_files[0], state_size)
	print("the highest percentage of ngrams that a sentence in the corpus has in common with the generated comment is: {}".format(result[0]))
	print("that sentence in the corpus is: {}".format(result[1]))

	result = utils.support(generated_comment, input_files[0], state_size)
	print("the sentences in the corpus that provide support for the ngrams in the generated comment are: {}".format(result))
	
	result = utils.ngram_frequencies(generated_comment, input_files[0], state_size)
	print("the frequencies of the ngrams in the generated comment are: {}".format(result))