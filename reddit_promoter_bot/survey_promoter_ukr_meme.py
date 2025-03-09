# survey_bot.py - Main script to post survey comments

import praw
import time
import random
import logging
from config import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT, REDDIT_REFRESH_TOKEN, SURVEY_LINK

logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(levelname)s - %(message)s')

# Set up the Reddit API client
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT,
    refresh_token=REDDIT_REFRESH_TOKEN
)

# List of subreddits to monitor
subreddits = [
    'politics', 'foreignpolicy', 'Askpolitics', 'worldnews', 'Ukraine',
    'Global_News_Hub', 'WorldPolitics', 'geopolitics', 'uspolitics',
    , 'humanitarian', 'USPoliticalPolls', 'war', "Economics"
    'Charity', 'democrats', 'government'
    'PoliticalOpinions', 'InternationalRelation', 'republican',
]
random.shuffle(subreddits)  # Shuffle order to distribute activity

# Keywords to look for
keywords = [
    'ukraine', 'foreign policy', 'aid', 'ukraine war', 'Military aid to Ukraine',
    "U.S. military aid", "support for Ukraine", "trump and zelensky", "us military aid", 'zelensky'
]

# Comment templates
comments = [
    "I'm conducting a survey for my class project on U.S. aid to Ukraine. If you have a moment, I'd really appreciate your help: [Survey Link](%s). Thanks!" % SURVEY_LINK,
    "Hey everyone, I'm gathering public opinion on U.S. aid to Ukraine for a class project. If you can, please take this quick survey: [Survey Link](%s). Appreciate it!" % SURVEY_LINK,
    "Hi! For my class research, I'm collecting responses on U.S. support for Ukraine. If you could fill out this short survey, it would be a huge help: [Survey Link](%s). Thanks in advance!" % SURVEY_LINK,
    "Hey folks! I'm researching U.S. aid to Ukraine and need your input. Please take a moment to fill out my survey: [Survey Link](%s). I truly appreciate it!" % SURVEY_LINK,
    "Hello! I'm working on a project about U.S. foreign policy and public opinion. If you have a few minutes, please take my survey: [Survey Link](%s). Your input is invaluable!" % SURVEY_LINK
]

def main():
    logging.info("Bot is starting...")
    
    try:
        username = reddit.user.me()
        logging.info(f"Authenticated as: {username}")
    except Exception as e:
        logging.error(f"Authentication failed: {e}")
        return
    
    for subreddit_name in subreddits:
        try:
            logging.info(f"Checking r/{subreddit_name}...")
            subreddit = reddit.subreddit(subreddit_name)
            
            # Flag to control comment posting
            posted_comment = False
            
            for submission in subreddit.new(limit=10):
                if posted_comment:
                    break  # Exit the loop after posting one comment
                
                submission.comments.replace_more(limit=0)
                already_replied = any(comment.author and comment.author.name == username for comment in submission.comments.list())
                
                if already_replied:
                    logging.info(f"Already commented on {submission.id}, skipping")
                    continue
                
                post_text = (submission.title + " " + submission.selftext).lower()
                if any(keyword in post_text for keyword in keywords):
                    try:
                        comment_text = random.choice(comments)
                        submission.reply(comment_text)
                        logging.info(f"Commented on post {submission.id}")
                        posted_comment = True  # Set flag to true to move to next subreddit
                        time.sleep(random.randint(60, 120))  # Avoid rate limits
                    except Exception as e:
                        logging.error(f"Error commenting on post {submission.id}: {e}")
                
                time.sleep(random.randint(5, 10))
            
        except Exception as e:
            logging.error(f"Error processing subreddit r/{subreddit_name}: {e}")
    
    logging.info("Completed full cycle")

if __name__ == "__main__":
    main()
