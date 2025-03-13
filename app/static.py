import pandas as pd

def calc_response_rate(df, company_id):
    # Select company tweets
    company_tweets = df[df.author_id == company_id]
    # Select customer tweets to the company
    customer_tweets = df[df.receiver == company_id]
    # Select customer tweets addressed to the company and were responded by the company
    root_tweets = df.reindex(company_tweets.in_response_to_tweet_id.dropna())
    root_tweets = root_tweets[root_tweets.receiver == company_id]
    # From the tweets that were responded to, select only the ones that are customer tweets 
    # (knowing that one tweet can be a response to only one tweet)
    customer_responded_tweets = root_tweets[root_tweets.inbound == True]
    # Calculate response rate
    response_rate = len(customer_responded_tweets) / len(customer_tweets)
    return response_rate

def calc_conversation_ratio(df, company_id):
    # Select company tweets
    company_tweets = df[df.author_id == company_id]
    # Select customer tweets addressed to the company
    customer_tweets = df[df.receiver == company_id]
    # Select company tweets that were a response to another tweet
    company_response_tweets = company_tweets.in_response_to_tweet_id.dropna()
    conversation_ratio = company_response_tweets.count()/customer_tweets.receiver.count()
    
    return conversation_ratio

def calc_volume_metrics(df, company_id):
    # Select company tweets (outbound tweets)
    company_tweets = df[df.author_id == company_id]
    # Select customer tweets addressed to the company (inbound tweets)
    customer_tweets = df[df.receiver == company_id]
    volume_metrics = len(customer_tweets)/len(company_tweets)
    return volume_metrics

def calc_get_response_time(df, row):
    try:
        response_time = df.loc[int(row.in_response_to_tweet_id)].created_at
        return response_time
    except:
        return None

def get_response_time(df, row):
    try:
        response_time = df.loc[int(row.in_response_to_tweet_id)].created_at
        return response_time
    except:
        return None

def calc_average_response_time(df, company_id):
    # Select company tweets
    company_tweets = df[df.author_id == company_id]
    # Select customer's tweets time
    company_tweets['inquiry_time'] = company_tweets.apply(lambda row: get_response_time(df, row), axis=1)
    # Calculate the average response time
    company_tweets.created_at = pd.to_datetime(company_tweets.created_at)
    company_tweets.inquiry_time = pd.to_datetime(company_tweets.inquiry_time)
    company_tweets['time_difference'] = company_tweets.created_at - company_tweets.inquiry_time
    average_time = company_tweets['time_difference'].mean()
    total_minutes = average_time.total_seconds() // 60
    
    return total_minutes