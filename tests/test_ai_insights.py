import pytest
from fastapi.testclient import TestClient
from app.main import app
import pandas as pd

client = TestClient(app)

@pytest.fixture
def setup_data():
    # Set up sample data in app.state.datos
    data = {
        "tweet_id": [1, 2, 3, 4],
        "author_id":["user1", "user1", "user2", "user2"],
        "inbound":[True, True, False, False],
        "created_at":["Tue Oct 31 22:08:27 +0000 2017", "Tue Oct 31 22:10:27 +0000 2017", "Tue Oct 31 22:09:27 +0000 2017", "Tue Oct 31 22:15:27 +0000 2017"],
        "text": ["Hello @user2", "Hi @user2", "Hey @user1", "Hey @user1"],
        "response_tweet_id":[3,4,None,None],
        "in_response_to_tweet_id":[None,None,1,2],
        "receiver": ["user2", "user2", "user1", "user1"],
    }

    df = pd.DataFrame(data)
    df.set_index("tweet_id", inplace=True)
    client.app.state.datos = df

def test_get_ai_insights_success(setup_data):
    # Test successful retrieval of AI insights
    response = client.get("/companies/user2/ai-insights")
    
    assert response.status_code == 200
    assert "top_issues" in response.json()
    assert "top_counts" in response.json()

def test_get_ai_insights_no_data():
    # Test retrieval of AI insights when no data is available
    if hasattr(client.app.state, 'datos'):
        del client.app.state.datos  # Ensure no data is loaded
    
    response = client.get("/companies/user2/ai-insights")
    
    assert response.status_code == 400
    assert response.json()["detail"] == "No data available. Please ingest tweets first."