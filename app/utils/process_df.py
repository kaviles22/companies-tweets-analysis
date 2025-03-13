import pandas as pd
import logging
from app.utils.extract_user import extract_user

def process_df(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Processing DataFrame to extract receivers and clean data.")
    
    df.set_index('tweet_id', inplace=True)
    df['receiver'] = df.text.map(extract_user)
    
    percentage_no_receiver = len(df[df.receiver.isna()]) * 100 / len(df)
    logging.info(f"{percentage_no_receiver:.2f}% of tweets will be removed due to missing receiver.")
    
    df = df[df.receiver.notna()]
    
    logging.info(f"DataFrame processed. {len(df)} tweets remain after cleaning.")
    return df