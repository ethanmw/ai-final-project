import praw

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
		
		data_object_list.append("COMMENT,SCORE,SUBREDDIT\n")
		for comment in top_level_comments:
			try:
				data_object = "{}\n".format(comment.body.replace("\n","").replace("\t"," ").rstrip())
				data_object_list.append(data_object)
			except:
				pass

with open("data/aww.txt", "w+", encoding="utf-8") as f:
	for data_object in data_object_list:
		f.write(data_object)