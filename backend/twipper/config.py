from datetime import datetime, timedelta
import os
from pathlib import Path

OLDEST_TWEET_DATE = datetime.now() - timedelta(days=180)
FETCH_INTERVAL_DURATION = timedelta(days=30)
THREAD_COUNT = 1

BASE_PATH = Path(os.path.dirname(__file__)).parent

LDA_SAVE_LOCATION = Path(BASE_PATH, 'resource','lda_model.pkl')
