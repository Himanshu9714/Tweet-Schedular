import logging
import os
import time
from datetime import datetime, timedelta

import gspread
import tweepy
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# Twitter configuration
CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_SECRET = os.environ.get('ACCESS_SECRET')

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth)

# Configure google spreadsheet
GOOGLE_SPREADSHEET_KEY = os.environ.get('GOOGLE_SPREADSHEET_KEY')
gc = gspread.service_account(filename='gsheet_credentials.json')
sh = gc.open_by_key(GOOGLE_SPREADSHEET_KEY)
worksheet = sh.sheet1

INTERVAL = int(os.environ.get('INTERVAL'))
DEBUG = os.environ.get('DEBUG') == '1'

# Script that runs at particular interval and publish a tweet.
def main():
    while True:
        tweet_records = worksheet.get_all_records()
        current_time = datetime.utcnow() + timedelta(hours=5, minutes=30)
        logger.info(f"{len(tweet_records)} tweets found at {current_time.time()}")
        time.sleep(INTERVAL)

        for idx, tweet in enumerate(tweet_records, start=2):
            msg = tweet['message']
            time_str = tweet['time']
            done = tweet['done']
            date_time_obj = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
            if not done:
                now_time_india = datetime.utcnow() + timedelta(hours=5, minutes=30)
                if date_time_obj < now_time_india:
                    logger.info("This should be tweeted!")
                    try:
                        api.update_status(msg)
                        worksheet.update_cell(idx, 3, 1)
                    except Exception as e:
                        logger.error(f"Exception during tweet! {e}")


if __name__ == '__main__':
    main()
