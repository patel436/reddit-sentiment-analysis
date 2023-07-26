# Reddit-Sentiment-Analysis

The aim of the project is to reveal customer opinions, feelings, and perceptions published on social media platform by using Reddit sentiment analysis.

# To Run

Install required dependencies using "pip install -r requirements.txt" and create "api_keys.py" file in reddit_sentiment_analyzer folder.  
api_keys.py contains the required credentials to connect reddit api in below format:

reddit_client_id = 'reddit app client id'<br/>
reddit_client_secret = 'reddit app client secret'<br/>
reddit_user_agent = 'useragent'<br/>

To visualize live tweets on real-time dashboard, docker instance should be running on the system and execute "redis" service from "docker-compose.yml" file.
