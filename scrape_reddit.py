#!/usr/bin/env python3
import praw
import argparse

def parse_command_line():
	parser = argparse.ArgumentParser()

	parser.add_argument("-s", "--subreddits",
						action="append",
						dest="subreddits",
						default=["aww"])

	parser.add_argument("-n", "--number-posts",
						type=int,
						dest="number_posts",
						default=30)

	parser.add_argument("-t", "--comment-threshold",
						type=int,
						dest="comment_threshold",
						default=300)

	parser.add_argument("-o", "--output-file",
						dest="output_file",
						default="output.txt")

	arguments = parser.parse_args()

	return arguments

def get_comma_separated_args(option, opt, value, parser):
	setattr(parser.values, option.dest, value.split(','))

if __name__ == "__main__":
	arguments = parse_command_line()
	
	subreddits = arguments.subreddits
	number_posts = arguments.number_posts
	min_number_comments = arguments.comment_threshold
	output_file = arguments.output_file

	# print("subreddits: {}".format(subreddits))
	# print("number_posts: {}".format(number_posts))
	# print("min_number_comments: {}".format(min_number_comments))
	# print("output_file: {}".format(output_file))

	reddit = praw.Reddit(client_id="ihIhF1immoEi8A",
						client_secret="KV2ma1Fx41wUSYIMX8n_DUvxOwg",
						user_agent="erinhh:v1 (by /u/erinhh)")

	data_object_list = []

	for subreddit in subreddits:
		for submission in reddit.subreddit(subreddit).top(limit=number_posts):
			top_level_comments = submission.comments
			top_level_comments.replace_more(limit=None, threshold=min_number_comments)
			for comment in top_level_comments:
				try:
					print(comment)
					data_object = "{}\n".format(comment.body.replace("\n","").replace("\t"," ").rstrip())
					for i in range(max(int(comment.score) / 1000.0, 1)):
						data_object_list.append(data_object)
				except:
					pass

	data_path = "data/{}".format(output_file)
	with open(data_path, "w+", encoding="utf-8") as f:
		for data_object in data_object_list:
			f.write(data_object)