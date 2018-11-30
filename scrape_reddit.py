#!/usr/bin/env python3
import praw
import argparse

def parse_command_line():
	parser = argparse.ArgumentParser()

	parser.add_argument("-s", "--subreddits",
						action="append",
						dest="subreddits",
						required=True)

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
	
	parser.add_argument("-m", "--mode",
						choices=['alltime', 'today'],
						dest="mode",
						default='alltime')

	arguments = parser.parse_args()
	return arguments

if __name__ == "__main__":
	arguments = parse_command_line()
	subreddits = arguments.subreddits
	number_posts = arguments.number_posts
	min_number_comments = arguments.comment_threshold
	output_file = arguments.output_file
	mode = arguments.mode

	reddit = praw.Reddit(client_id="ihIhF1immoEi8A",
						client_secret="KV2ma1Fx41wUSYIMX8n_DUvxOwg",
						user_agent="erinhh:v1 (by /u/erinhh)")

	data_object_list = []

	for subreddit in subreddits:
		if mode == 'alltime':
			posts = reddit.subreddit(subreddit).top(limit=number_posts)
		elif mode == 'today':
			posts = reddit.subreddit(subreddit).top(time_filter="day", limit=number_posts)
		for submission in posts:
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
	with open(data_path, "w+", encoding="utf-8") as output_file:
		for data_object in data_object_list:
			output_file.write(data_object)