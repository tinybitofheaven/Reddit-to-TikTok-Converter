import praw
import json

# reddit settings
SUBREDDIT = "AmITheAsshole"
POST_LIMIT = 3

# local config settings
json_data = open('config.json')
config = json.load(json_data)

# Read-only instance
reddit_read_only = praw.Reddit(client_id=config["client_id"],         # your client id
                            client_secret=config["client_secret"],      # your client secret
                            user_agent=config["user_agent"])        # your user agent

#retrieves user input data
def set_subreddit(gui_input):
    SUBREDDIT = gui_input

def check_subreddit_valid():
    try:
        reddit_read_only.subreddit(SUBREDDIT)
        return True
    except:
        print("Error: invalid subreddt, subreddit is privated, banned or doesn't exist: " + SUBREDDIT)
        return False

def get_threads_from_subreddit(subreddit, post_limit) -> list[praw.models.Submission]:
    subreddit = reddit_read_only.subreddit(subreddit)
    return list(filter(filter_threads, subreddit.hot(limit=post_limit)))

def get_thread_from_url(url: str) -> praw.models.Submission:
    return reddit_read_only.submission(url=url)

# Filter threads that we keep from parsing reddit.
# - no pinned posts.
def filter_threads(thread):
    if(thread.stickied):
        return False
    if(thread.over_18):
        return False
    return True

def testsubmit(mystring):
    print(mystring)