import os
import requests
from dotenv import load_dotenv

load_dotenv()

def fetch_disruption_news(query: str = "supply chain disruption"):
    """
    Fetches news articles related to supply chain disruptions using the GNews API and prints them cuz why not.
    """
    # 1. Get the API key that we stored in the .env file
    api_key = os.getenv("GNEWS_API_KEY")
    if not api_key:
        print("Error: GNEWS_API_KEY not found. Please check your .env file.")
        return []

    
    # 3. Construct the full URL to send to the GNews API; blah blah boringggg. :o
    url = f"https://gnews.io/api/v4/search?q={query}&lang=en&max=10&token={api_key}"

    print("Fetching news from GNews API...")
    
    # 4. Use a try/except block for good error handling ; also to ensure it doesnt blow up in my face ://
    try:
        response = requests.get(url)
        response.raise_for_status() 
        data = response.json()
        articles = data.get("articles", [])
        return articles # Return the list of articles

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching news: {e}")
        return [] # Return an empty list on error

# if __name__ == "__main__":
#     fetch_disruption_news()