import os
from datetime import datetime, timedelta

import gspread
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request

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

    tweets.reverse()
    n_open_tweets = sum(1 for tweet in tweets if not tweet.done)
    return render_template('base.html', tweets=tweets, n_open_tweets=n_open_tweets)


def get_date_time(date_time_str):
    date_time_obj = None
    error_code = None
    try:
        date_time_obj = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")
    except ValueError as e:
        error_code = f"Error! {e}"

    if date_time_obj is not None:
        now_time_india = datetime.utcnow() + timedelta(hours=5, minutes=30)
        if not date_time_obj > now_time_india:
            error_code = f"Error! time must be in the future"
    return date_time_obj, error_code


@app.route("/tweet", methods=['POST'])
def add_tweet():
    message = request.form['message']
    if not message:
        return "No message"
    
    if len(message) > 280:
        return "Message too long! It should <= 280 characters"

    time = request.form['time']
    if not time:
        return "No time entered"

    password = request.form['password']
    if not password or password != "12345":
        return "Wrong password!"

    date_time_obj, error_code = get_date_time(time)
    if error_code is not None:
        return error_code
    
    tweet = [str(date_time_obj), message, 0]
    worksheet.append_row(tweet)

    return redirect('/')


@app.route("/delete/<int:row_idx>")
def delete_tweet(row_idx):
    worksheet.delete_rows(row_idx)
    return redirect('/')
