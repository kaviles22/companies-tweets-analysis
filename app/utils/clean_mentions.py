import re

def clean_mentions(tweet):
    return re.sub(r'@[\w]+', '', tweet)