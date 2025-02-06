import praw
import tweepy
import datetime
import warnings
import config  # Import the config file with credentials
warnings.simplefilter("ignore", SyntaxWarning)

# Reddit API credentials from config
reddit = praw.Reddit(
    client_id=config.REDDIT_CLIENT_ID,
    client_secret=config.REDDIT_CLIENT_SECRET,
    user_agent=config.REDDIT_USER_AGENT
)

# Twitter API credentials (OAuth 2.0 User Context)
client = tweepy.Client(
    consumer_key=config.consumer_key,
    consumer_secret=config.consumer_secret,
    access_token=config.access_token,
    access_token_secret=config.access_token_secret
)

# Fetch the top post from the last day from r/ufos
subreddit = reddit.subreddit('ufos')
top_posts = subreddit.top(time_filter='day', limit=1)

for post in top_posts:
    post_title = post.title
    post_score = post.score
    reddit_post_url = f"https://reddit.com{post.permalink}"  # Direct link to the Reddit post

    # Format the message to be posted on Twitter
    tweet_content = f"Top post from r/UFOs in the last day. #UFOx:\n\n{post_title}\nScore: {post_score}\n{reddit_post_url} #ufotwitter #UFOs #UAP"

    # Ensure the tweet content does not exceed Twitter's 280-character limit
    if len(tweet_content) > 280:
        truncated_title = post_title[:(280 - len(f"Top post from r/ufos in the last day:\n\nScore: {post_score}\n{reddit_post_url}")) - 3] + "..."
        tweet_content = f"Top post from r/UFOs in the last day. #UFOx:\n\n{truncated_title}\nScore: {post_score}\n{reddit_post_url}"

    # Post to Twitter using Tweepy with API v2
    try:
        response = client.create_tweet(text=tweet_content)
        print("Tweet posted successfully!")
        print(tweet_content)
    except Exception as e:
        print(f"Error posting tweet: {e}")

    break  # Since we only want the top post, we break after the first post