from datetime import datetime, timedelta

OLDEST_TWEET_DATE = datetime.now() - timedelta(days=180)
FETCH_INTERVAL_DURATION = timedelta(days=30)
THREAD_COUNT = 1