import praw
import tweepy
import datetime
import warnings
warnings.filterwarnings("ignore", category=SyntaxWarning)

# Reddit API credentials
reddit = praw.Reddit(
    client_id="",
    client_secret="",
    user_agent=""
)

# Twitter API credentials (OAuth 2.0 User Context)
client = tweepy.Client(
    consumer_key="",  # Twitter API Key
    consumer_secret="",  # Twitter API Secret
    access_token="",  # Twitter Access Token
    access_token_secret=""  # Twitter Access Token Secret
)

# Fetch the top post from the last day from r/yoursubreddit
subreddit = reddit.subreddit('yoursubreddit')
top_posts = subreddit.top(time_filter='day', limit=1)

for post in top_posts:
    post_title = post.title
    post_url = post.url
    post_score = post.score

    # Format the message to be posted on Twitter
    tweet_content = f"Top post from __ in the last day:\n\n{post_title}\nScore: {post_score}\n{post_url}"

    # Ensure the tweet content does not exceed Twitter's 280-character limit
    if len(tweet_content) > 280:
        truncated_title = post_title[:(280 - len(f"Top post from __ in the last day:\n\nScore: {post_score}\n{post_url}")) - 3] + "..."
        tweet_content = f"Top post from __ in the last day:\n\n{truncated_title}\nScore: {post_score}\n{post_url}"

    # Post to Twitter using Tweepy with API v2
    try:
        response = client.create_tweet(text=tweet_content)
        print("Tweet posted successfully!")
    except Exception as e:
        print(f"Error posting tweet: {e}")

    break  # Since we only want the top post, we break after the first post
