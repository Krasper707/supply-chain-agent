import os
import requests
from dotenv import load_dotenv

load_dotenv()

def fetch_disruption_news():
    """
    Fetches news articles related to supply chain disruptions using the GNews API and prints them cuz why not.
    """
    # 1. Get the API key that we stored in the .env file
    api_key = os.getenv("GNEWS_API_KEY")
    if not api_key:
        print("Error: GNEWS_API_KEY not found. Please check your .env file.")
        return

    # 2. Define the search query. What we need to find articles for. So, ye.
    query = 'technology'
    
    # 3. Construct the full URL to send to the GNews API; blah blah boringggg. :o
    url = f"https://gnews.io/api/v4/search?q={query}&lang=en&max=10&token={api_key}"

    print("Fetching news from GNews API...")
    
    # 4. Use a try/except block for good error handling ; also to ensure it doesnt blow up in my face ://
    try:
        # Send the request
        response = requests.get(url)
        response.raise_for_status() 
        
        data = response.json()
        articles = data.get("articles", [])

        if not articles:
            print("No articles found for the query.")
            return

        print("\n--- Latest Supply Chain News ---")
        for i, article in enumerate(articles):
            print(f"{i+1}. Title: {article['title']}")
            print(f"   Source: {article['source']['name']}")
            print(f"   URL: {article['url']}\n")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching news: {e}")

if __name__ == "__main__":
    fetch_disruption_news()