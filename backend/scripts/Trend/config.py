from datetime import datetime, timedelta

LDA_SIZE = 8
TRENDS_NUMBER = 5
DAILY_MAX_TREND = 480

ARCHIVE_BASE_URL = 'https://archive.twitter-trending.com/'
HEADER = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 '
                  'Safari/537.36 QIHU 360SE '
}

OLDEST_TREND_DATE = datetime.now() - timedelta(days=30*6+1)