import pytest
from fastapi.testclient import TestClient
from app.main import app
import pandas as pd
import os

client = TestClient(app)

@pytest.fixture
def sample_csv_file(tmpdir):
    # Create a sample CSV file for testing
    csv_data = """tweet_id,author_id,inbound,created_at,text,response_tweet_id,in_response_to_tweet_id
1,sprintcare,False,Tue Oct 31 22:10:47 +0000 2017,@115712 I understand. I would like to assist you. We would need to get you into a private secured link to further assist.,2,3
2,115712,True,Tue Oct 31 22:11:45 +0000 2017,@sprintcare and how do you propose we do that,,1
3,115712,True,Tue Oct 31 22:08:27 +0000 2017,@sprintcare I have sent several private messages and no one is responding as usual,1,4
4,sprintcare,False,Tue Oct 31 21:54:49 +0000 2017,@115712 Please send us a Private Message so that we can further assist you. Just click â€˜Messageâ€™ at the top of your profile.,3,5
"""
    file_path = tmpdir.join("sample.csv")
    with open(file_path, "w") as f:
        f.write(csv_data)
    return file_path

def test_ingest_tweets_success(sample_csv_file):
    # Test successful ingestion of tweets
    with open(sample_csv_file, "rb") as f:
        response = client.post("/ingest", files={"file": ("sample.csv", f)})
    
    assert response.status_code == 200
    assert response.json() == {"message": "4 tweets successfully loaded."}

    # Verify that the data was saved to disk
    assert os.path.exists("data/input_data.csv")

    # Verify that the data was loaded into memory
    assert hasattr(client.app.state, 'datos')
    assert isinstance(client.app.state.datos, pd.DataFrame)
    assert len(client.app.state.datos) == 4

def test_ingest_tweets_invalid_file():
    # Test ingestion with an invalid file
    response = client.post("/ingest", files={"file": ("invalid.txt", b"invalid data")})
    
    assert response.status_code == 500
    assert "Error processing file" in response.json()["detail"]