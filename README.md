# Backend_Developer_Python_01

Welcome to the technical test for Python Backend Developer position! In this test, you will build a backend service using **FastAPI** that analyzes Twitter customer support data and returns actionable insights for companies. The goal is to implement a robust backend service with clean code, proper logging, and meaningful metrics—all while leveraging modern AI tools to derive additional insights.

---

## Project Description

You are tasked with building the **Customer Support Insights API**. This service processes Twitter data (using, for instance, the [Kaggle dataset](https://www.kaggle.com/datasets/thoughtvector/customer-support-on-twitter)) and provides companies with detailed metrics on their support interactions. The dataset includes the following columns:

- **tweet_id:** The unique ID for this tweet.
- **author_id:** The unique ID for the tweet author (anonymized for non-company users).
- **inbound:** Boolean indicating whether the tweet was sent (inbound) to a company.
- **created_at:** When the tweet was created.
- **text:** The text content of the tweet.
- **response_tweet_id:** The tweet that responded to this one, if any.
- **in_response_to_tweet_id:** The tweet this tweet was in response to, if any.

Assume the following:
- **Company tweets** are identified as non-inbound messages (i.e. `inbound` is False) or via a designated company identifier.
- **Customer tweets** are those with `inbound` set to True.

Your service must compute several metrics, such as:
- **Response Rate:** The percentage of customer (inbound) tweets that received at least one response.
- **Conversation Ratio:** The ratio of company responses to customer inquiries.
- **Volume Metrics:** Total counts of inbound versus outbound tweets for the specified company.
- *(Optional)* **Average Response Time:** The average delay between a customer tweet and the company’s response.

In addition, you will enhance the insights by integrating an AI component that utilizes a free hosted Hugging Face model (e.g., [LLaMA](https://huggingface.co/docs/transformers/en/model_doc/llama)) to analyze tweet texts and identify common problems or issues mentioned by customers.

---

## Technical Requirements

Your implementation should adhere to the following guidelines:

- **Framework:** FastAPI.
- **Programming Language:** Python 3.8+.
- **Database/Storage:** You may load the Kaggle dataset into an in-memory data structure (e.g., a pandas DataFrame) or use a lightweight database (e.g., SQLite).
- **Docker:** The application must be dockerized.
- **API Documentation:** Use FastAPI’s built-in OpenAPI docs.
- **Testing:** Include unit and integration tests with at least 80% coverage.
- **Code Quality:** Follow PEP8 guidelines, use type hints, and include linting (e.g., flake8) and formatting (e.g., black).
- **Logging:** Implement logging for HTTP requests and key backend events.
- **Security:** Implement token-based (JWT) authentication and secure sensitive configurations via environment variables.

---

## API Endpoints

### 1. Data Ingestion (Optional / Bootstrap)
- **POST** `/ingest`: An endpoint to load the tweet dataset into the application (e.g., from a CSV file or local disk). This can be used once to initialize the in-memory or persistent storage.

### 2. Company Insights
- **GET** `/companies/{company_id}/insights`: Given a company identifier (e.g., the company’s author_id or a dedicated ID), return aggregated metrics including:
  - Total inbound tweets (customer inquiries).
  - Total outbound tweets (company responses).
  - **Response Rate:** The percentage of inbound tweets that received at least one response.
  - **Conversation Ratio:** The ratio of responses to inquiries.
  - *(Optional)* **Average Response Time:** If applicable, the average time taken by the company to respond.
  - *(Optional)* Any additional insights, such as conversation trends over time.

### 3. AI-Enhanced Common Issues Analysis (Optional Bonus)
- **GET** `/companies/{company_id}/ai-insights`: Leverage a free hosted Hugging Face model (e.g., LLaMA, as detailed [here](https://huggingface.co/docs/transformers/en/model_doc/llama)) to analyze customer tweets for the given company. The endpoint should:
  - Analyze tweet texts and extract the top common issues or complaints.
  - Return a list (e.g., the top 5 issues) with associated metrics such as the percentage of tweets mentioning each issue.
  - Optionally, include a brief sentiment or topic summary for each identified issue.
  
  *Note:* You may call the Hugging Face Inference API or use any available hosted model to implement this functionality. Integration of these AI-enhanced insights is optional but will be considered a bonus.

---

## Dockerization

- Provide a **Dockerfile** to build your FastAPI application.
- Include a **docker-compose.yml** file to facilitate local deployment (this should also cover any ancillary services like a database if used).

---

## Logging and Monitoring

- Implement logging to capture:
  - All incoming HTTP requests and responses.
  - Key backend events (e.g., data ingestion, error occurrences, metrics computation).
- You may use Python’s built-in logging module or a third-party library (e.g., loguru).

---

## Security

- Implement basic security for API endpoints (e.g., JWT-based authentication) to ensure that only authorized users can access insights.
- Use environment variables to secure sensitive configurations (e.g., database credentials, secret keys).

---

## Testing

- Write unit tests and integration tests ensuring at least 80% code coverage.
- Include clear instructions on how to run the tests in your README.

---

## Aspects to Evaluate

During the review, we will assess:

1. **Functionality:** The API should correctly process the dataset and return the expected insights.
2. **Efficiency:** Evaluate the performance and efficiency of data processing and aggregation logic.
3. **Code Quality:** Code should be clean, modular, well-documented, and adhere to best practices (proper error handling, type hints, PEP8).
4. **Project Organization:** Logical module structuring with clear separation of concerns (routers, services, models).
5. **Testing:** Quality and coverage of tests (unit and integration).
6. **Dockerization & Deployment:** Ease of setting up and running the application using Docker.
7. **Logging & Security:** Implementation of comprehensive logging and basic API security.
8. **AI-Enhanced Metrics (Bonus):** Effective integration of a Hugging Face hosted model to provide additional insights on common customer issues.

---

## Tasks to Perform

1. **Project Setup:**
   - Create a FastAPI project with a modular structure.
   - Set up dependency management (e.g., `requirements.txt`, Pipenv, or Poetry).

2. **Data Handling:**
   - Implement functionality to load and process the provided dataset.
   - Choose an appropriate storage method (in-memory with pandas or a lightweight database) and justify your choice in the README.

3. **API Implementation:**
   - Develop the endpoints as specified above.
   - Ensure proper input validation (e.g., company IDs).

4. **Logging & Security:**
   - Implement logging for HTTP requests and key backend operations.
   - Secure endpoints using JWT-based authentication.

5. **Dockerization:**
   - Create a Dockerfile for the FastAPI application.
   - Provide a `docker-compose.yml` file for local deployment (including any necessary services).

6. **Testing:**
   - Write unit tests and integration tests with at least 80% coverage.
   - Include test instructions in the README.

7. **Documentation:**
   - Update the README with:
     - Setup instructions.
     - How to run the application locally and via Docker.
     - How to run tests and view code coverage.
     - API usage examples and sample requests (including authentication details).

8. **Optional AI Enhancements (Bonus):**
   - Integrate a free hosted Hugging Face model (e.g., LLaMA) to analyze customer tweets for common issues.
   - Implement the `/companies/{company_id}/ai-insights` endpoint (or integrate this functionality into the existing insights endpoint) with clear labeling for AI-enhanced metrics.
   - Document how the model is used and any relevant configuration in the README.

---

## Test Delivery

- Deliver your source code by forking the repository provided for the test.
- The branch name should follow this convention: `test/your-name`.
- Ensure the README.md includes:
  - Setup instructions.
  - How to run the application (locally and via Docker).
  - How to run tests and view code coverage.
  - API usage examples and sample requests.

---

Good luck, and we look forward to reviewing your work!

---

This technical test is intended to assess your backend development skills, your ability to integrate modern AI tools into data processing, and your proficiency in creating scalable, secure, and maintainable Python services with FastAPI.


---
# Tweets Analyzer API
## Setup instructions
Make sure to have python and docker installed.

## Run application
To run the application:
1. Clone the repo
2. Run docker compose up --build this will generate a docker image and run a docker container with the fastapi API
3. Once the API is running you can acces it at http://localhost:8000

The API has three endpoints:
- **POST /ingest**
  Here you can load a csv file containing the following columns: tweet_id,author_id,inbound,created_at,text,response_tweet_id,in_response_to_tweet_id.
  
- **GET /companies/{company_id}/insights**
  Here you can choose one company to calculate the metrics of the responses (described above).
      
- **GET /companies/{company_id}/ai-insights**
  Here you can choose one company to analyze the most common issues addressed by the customers.
  
## Run tests
To run the tests you should create an environment using the requirements.txt file and then run pytest tests

## API usage examples

