import praw
from config import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT, SURVEY_LINK, REDIRECT_URI


# Initialize Reddit instance
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    user_agent=REDDIT_USER_AGENT
)


# Generate the authentication URL
auth_url = reddit.auth.url(["identity", "submit", "read"], "unique_state_string", "permanent")
print("Visit this URL to authorize the bot and obtain the authentication code:")
print(auth_url)

# After authorization, enter the code provided by Reddit
auth_code = input("Enter the code from the URL: ")

# Exchange the code for a refresh token
refresh_token = reddit.auth.authorize(auth_code)
print("Your refresh token is:", refresh_token)
