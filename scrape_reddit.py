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

	parser.add_option("-n", "--number-posts",
						type="int",
						dest="number_posts",
						default=30,
						help="number of posts to gather from each subreddit")

	parser.add_option("-t", "--comment-threshold",
						type="int",
						dest="comment_threshold",
						default=300,
						help="minimum number of comments to retrieve from a post")

	parser.add_option("-o", "--output-file",
						dest="output_file",
						default="output.txt",
						help="name of file to output to")

	options, args = parser.parse_args()

	return options

def get_comma_separated_args(option, opt, value, parser):
	setattr(parser.values, option.dest, value.split(','))

if __name__ == "__main__":
	options = parse_command_line()
	
	subreddits = options.subreddits
	number_posts = options.number_posts
	min_number_comments = options.comment_threshold
	output_file = options.output_file

	print("subreddits: {}".format(subreddits))
	print("number_posts: {}".format(number_posts))
	print("min_number_comments: {}".format(min_number_comments))

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
					for i in range(int(comment.score)):
						data_object_list.append(data_object)
				except:
					pass

	data_path = "data/{}".format(output_file)
	with open(data_path, "w+", encoding="utf-8") as f:
		for data_object in data_object_list:
			f.write(data_object)