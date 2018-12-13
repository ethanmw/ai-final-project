#!/usr/bin/env python3
import praw
import argparse
import math

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

	parser.add_argument("-d", "--record-scores",
						type=bool,
						dest="record_scores",
						default=False)

	arguments = parser.parse_args()
	return arguments

if __name__ == "__main__":
	arguments = parse_command_line()

	subreddits = arguments.subreddits
	number_posts = arguments.number_posts
	min_number_comments = arguments.comment_threshold
	output_file = arguments.output_file
	mode = arguments.mode
	record_scores = arguments.record_scores

	reddit = praw.Reddit(client_id="ihIhF1immoEi8A",
						client_secret="KV2ma1Fx41wUSYIMX8n_DUvxOwg",
						user_agent="erinhh:v1 (by /u/erinhh)")

	if not record_scores:
		data_path = "data/weighted_comments/{}".format(output_file)
		with open(data_path, "w+", encoding="utf-8") as output_file:
			for subreddit in subreddits:
				if mode == 'alltime':
					posts = reddit.subreddit(subreddit).top(limit=number_posts)
				elif mode == 'today':
					posts = reddit.subreddit(subreddit).top(time_filter="day", limit=number_posts)

				submission_number = 0
				for submission in posts:
					submission_number = submission_number + 1
					top_level_comments = submission.comments
					top_level_comments.replace_more(limit=None, threshold=min_number_comments)
					
					comment_number = 0
					for comment in top_level_comments:
						comment_number = comment_number + 1

						try:
							data_object = "{}\n".format(comment.body.replace("\n","").replace("\t"," ").rstrip())
							comment_weight = int(math.log10(comment.score))
							for i in range(0, comment_weight):
								output_file.write(data_object)
							print("submission: {} comment: {} appended {} times".format(submission_number, comment_number, comment_weight))
						except:
							print("something went wrong appending submission: {} comment: {}".format(submission_number, comment_number))
	else:
		data_path = "data/scored_comments/{}".format(output_file)
		with open(data_path, "w+", encoding="utf-8") as output_file:
			for subreddit in subreddits:
				if mode == "alltime":
					posts = reddit.subreddit(subreddit).top(limit=number_posts)
				elif mode == "today":
					posts = reddit.subreddit(subreddit).top(time_filter="day", limit=number_posts)

				submission_number = 0
				for submission in posts:
					submission_number = submission_number + 1
					top_level_comments = submission.comments
					top_level_comments.replace_more(limit=None, threshold=min_number_comments)

					comment_number = 0
					for comment in top_level_comments:
						comment_number = comment_number + 1

						try:
							data_object = "{},{}\n".format(comment.body.replace("\n","").replace("\t"," ").rstrip(), int(comment.score))
							output_file.write(data_object)
							print("submission: {} comment: {} appended".format(submission_number, comment_number))
						except:
							print("something went wrong appending submission: {} comment: {}".format(submission_number, comment_number))

