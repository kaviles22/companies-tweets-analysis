import logging
from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException
import pandas as pd
from typing import List, Dict
import csv
import re
from io import StringIO
from static import calc_response_rate, calc_conversation_ratio, calc_volume_metrics, calc_average_response_time
from transformers import LlamaTokenizer, LlamaForCausalLM
import os
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-1B")
model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.2-1B")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),  # Log to console
        logging.FileHandler("app.log")  # Also log to a file
    ]
)

# Create FastAPI instance
app = FastAPI()

# Global data storage
datos: pd.DataFrame = pd.DataFrame()

os.makedirs('data', exist_ok=True)

def extract_user(tweet: str) -> str:
    """
    Extracts the username (receiver) mentioned in a tweet.
    
    Args:
        tweet (str): The text of the tweet.
    
    Returns:
        str: The username mentioned in the tweet, or None if no username is found.
    """
    match = re.search(r'@(\w+)', tweet)  # Regex to find the text following "@"
    if match:
        return match.group(1)  # Return the username after "@"
    return None  # Return None if no username is found

def process_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Processes the tweet DataFrame by extracting the receiver from the text and removing rows with no receiver.
    
    Args:
        df (pd.DataFrame): The input DataFrame containing tweet data.
    
    Returns:
        pd.DataFrame: The processed DataFrame with 'receiver' column and rows with valid receivers.
    """
    logging.info("Processing DataFrame to extract receivers and clean data.")
    
    # Set 'tweet_id' as the index
    df.set_index('tweet_id', inplace=True)
    
    # Extract the receiver (username) for each tweet using the extract_user function
    df['receiver'] = df.text.map(extract_user)
    
    # Calculate and log the percentage of tweets without a receiver
    percentage_no_receiver = len(df[df.receiver.isna()]) * 100 / len(df)
    logging.info(f"{percentage_no_receiver:.2f}% of tweets will be removed due to missing receiver.")
    
    # Remove rows where 'receiver' is None
    df = df[df.receiver.notna()]
    
    logging.info(f"DataFrame processed. {len(df)} tweets remain after cleaning.")
    return df

@app.post("/ingest")
async def ingest_tweets(file: UploadFile = File(...)) -> Dict[str, str]:
    """
    Ingests tweets from a CSV file, processes them, and saves them to the local disk.
    
    Args:
        file (UploadFile): The uploaded CSV file containing tweet data.
    
    Returns:
        dict: A message indicating how many tweets were successfully loaded.
    """
    global datos
    
    try:
        logging.info("Starting tweet ingestion.")
        
        # Read the content of the uploaded file
        contents = file.file.read()
        buffer = StringIO(contents.decode('utf-8'))
        csv_reader = csv.DictReader(buffer)
        
        # Count rows and prepare output file
        row_count = 0
        output_filename = 'data/input_data.csv'

        with open(output_filename, mode='w', newline='') as file:
            fieldnames = csv_reader.fieldnames  # Column names from the CSV file
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            
            # Write the header and rows to the new file
            writer.writeheader()
            for row in csv_reader:
                row_count += 1
                writer.writerow(row)
        
        # Close the buffer and read the saved CSV into a DataFrame
        buffer.close()
        
        # Process the data and log the operation
        datos = pd.read_csv(output_filename)
        datos = process_df(datos)
        
        logging.info(f"{row_count} tweets successfully ingested and processed.")
        
        return {"message": f"{row_count} tweets successfully loaded."}
    
    except Exception as e:
        logging.error(f"Error during tweet ingestion: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing file: {e}")

@app.get("/companies/{company_id}/insights")
async def get_company_insights(company_id: str) -> Dict[str, float]:
    """
    Fetches business insights related to response rates, conversation ratios, and other metrics for a given company.
    
    Args:
        company_id (str): The ID of the company whose insights are being requested.
    
    Returns:
        dict: A dictionary containing the insights such as response rate, conversation ratio, etc.
    """
    global datos
    
    logging.info(f"Fetching insights for company {company_id}.")
    
    # Ensure that the data is available before proceeding
    if datos.empty:
        logging.warning("No data available. Please ingest tweets first.")
        raise HTTPException(status_code=400, detail="No data available. Please ingest tweets first.")
    
    # Calculate the required insights and log each step
    response_rate = calc_response_rate(datos, company_id)
    conversation_ratio = calc_conversation_ratio(datos, company_id)
    volume_metrics = calc_volume_metrics(datos, company_id)
    average_minutes = calc_average_response_time(datos, company_id)

    insights = {
        "response_rate": response_rate,
        "conversation_ratio": conversation_ratio,
        "volume_metrics": volume_metrics,
        "average_response_time": average_minutes
    }
    
    logging.info(f"Insights successfully fetched for company {company_id}.")
    
    return insights

@app.get("/companies/{company_id}/ai-insights")
async def get_ai_insights(company_id: str) -> Dict[str, str]:
    """
    Returns AI-generated insights (currently a placeholder) for a given company.
    
    Args:
        company_id (int): The ID of the company.
    
    Returns:
        dict: A dictionary with AI insights (currently returns 'None').
    """
    global datos
    logging.info(f"AI insights requested for company {company_id}.")
    print(datos.iloc[0])
    tweets = datos['text'].dropna().tolist()
    document = "\n".join(tweets)
    prompt = f"Extract the top 5 common issues from the following tweets:\n{document}\n\nTop 5 issues:"

    inputs = tokenizer(prompt, return_tensors="pt")

    # Generate the response
    output = model.generate(inputs['input_ids'], max_length=1000, num_return_sequences=1, do_sample=False)

    # Decode the output
    extracted_issues = tokenizer.decode(output[0], skip_special_tokens=True)

    # Placeholder print for debugging
    return {"top_issues": extracted_issues}
