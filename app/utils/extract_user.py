import re

def extract_user(tweet: str) -> str:
    match = re.search(r'@(\w+)', tweet)
    if match:
        return match.group(1)
    return None