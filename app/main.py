from flask import Flask, render_template
import gspread
from dotenv import load_dotenv
import os

load_dotenv()

# Create flask app
app = Flask(__name__)

# Configure google spreadsheet
GOOGLE_SPREADSHEET_KEY = os.environ.get('GOOGLE_SPREADSHEET_KEY')
gc = gspread.service_account(filename='gsheet_credentials.json')
sh = gc.open_by_key(GOOGLE_SPREADSHEET_KEY)
worksheet = sh.sheet1


class Tweet:
    def __init__(self, message, time, done, row_idx):
        self.message = message
        self.time = time
        self.done = done
        self.row_idx = row_idx


@app.route("/")
def tweet_list():
    tweet_records = worksheet.get_all_records()
    tweets = []
    # Here row_idx start with 2, 
    # because in spreadsheet the indices starts with 1 
    # and at row index 1 we have column names
    for idx, tweet in enumerate(tweet_records, start=2):
        tweet = Tweet(**tweet, row_idx=idx)
        tweets.append(tweet)

    n_open_tweets = sum(1 for tweet in tweets if not tweet.done)
    return render_template('base.html', tweets=tweets, n_open_tweets=n_open_tweets)