from datetime import datetime, timedelta
import os
from pathlib import Path

OLDEST_TWEET_DATE = datetime(2022, 8, 1) - timedelta(days=30*6)
FETCH_INTERVAL_DURATION = timedelta(days=1)
THREAD_COUNT = 1

BASE_PATH = Path(os.path.dirname(__file__)).parent

LDA_SAVE_LOCATION = Path(BASE_PATH, 'resource','lda_model.pkl')
KERAS_SAVE_LOCATION = Path(BASE_PATH, 'resource','checkpoint')
