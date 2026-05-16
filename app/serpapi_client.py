import os
import serpapi
from dotenv import load_dotenv

load_dotenv()


def get_serpapi_client():
    api_key = os.getenv("SERPAPI_KEY")

    if not api_key:
        raise ValueError("SERPAPI_KEY missing")

    return serpapi.Client(api_key=api_key)


def search_google(query: str, num: int = 5):
    client = get_serpapi_client()

    results = client.search({
        "engine": "google",
        "q": query,
        "location": "Austin, Texas, United States",
        "google_domain": "google.com",
        "gl": "us",
        "hl": "en",
        "num": num
    })

    return results.get("organic_results", [])