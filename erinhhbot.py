import praw
import re
import time

def bot_login():
        reddit = praw.Reddit(client_id = 'IBrYom7_RAmYaA',
                        client_secret = 'Nyd35S8XkL6IodQOM3ptY94UnsI',
                        user_agent = '<console:ERINHH:0.0.1 (by /u/mcavanag>',
                        username='mcavanag',
                        password = 'AIproject')
        return r
        
def markovchainbabble():
        return comment
  
def run_bot(r):
        for comment in r.subreddit('aww').comments(limit=25):
                chainreply = markovchainbabble()
                comment.reply(chainreply)


r = bot_login()
run_bot(r)
