#!/usr/bin/env python3
import praw
import optparse

def parse_command_line():
	usage = ("usage: %prog [options]\n")

	parser = optparse.OptionParser(usage=usage)

	parser.add_option("-s", "--subreddits",
						type="string",
						action="callback",
						callback=get_comma_separated_args,
						dest="subreddits",
						default=["aww"],
						help="subreddits to scrape")



	options, args = parser.parse_args()

	# if len(args) != 0:
	# 	parser.error("Invalid number of arguments provided.")

	return options

def get_comma_separated_args(option, opt, value, parser):
	setattr(parser.values, option.dest, value.split(','))

if __name__ == "__main__":
	# print("this is the program")
	# options = parse_command_line()
	# for subreddit in options.subreddits:
	# 	print(subreddit)

	subreddits = options.subreddits
	number_posts = 

	reddit = praw.Reddit(client_id="ihIhF1immoEi8A",
						client_secret="KV2ma1Fx41wUSYIMX8n_DUvxOwg",
						user_agent="erinhh:v1 (by /u/erinhh)")

	# get the comments from the top n posts in each subreddit
	number_posts = 30
	# get at least 300 comments from oeach of those posts
	min_number_comments = 300
	# subreddits to gather comments from
	subreddits = ["aww"]
	data_object_list = []

	for subreddit in subreddits:
		for submission in reddit.subreddit(subreddit).top(limit=number_posts):
			top_level_comments = submission.comments
			top_level_comments.replace_more(limit=None, threshold=min_number_comments)
			for comment in top_level_comments:
				try:
					print(comment)
					data_object = "{}\n".format(comment.body.replace("\n","").replace("\t"," ").rstrip())
					for i in range(int(comment.score)):
						data_object_list.append(data_object)
				except:
					pass

	with open("data/aww.txt", "w+", encoding="utf-8") as f:
		for data_object in data_object_list:
			f.write(data_object)