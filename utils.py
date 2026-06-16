# utils.py
import requests 
from bs4 import BeautifulSoup

def extract_from_url(url): 
    try: 
        headers = {"User-Agent": "Mozilla/5.0"}
        # fetch all data from the url 
        response = requests.get(
            url, 
            headers=headers, 
            timeout=10
        )
        # parse the data
        soup = BeautifulSoup(
            response.text,
            "html.parser",
        )

        # Get all paragraph text
        paragraphs = soup.find_all("p")
        text = " ".join([p.get_text() for p in paragraphs])
        return text[:5000]  # limit length
    except Exception as e:
        return f"Could not fetch URL: {str(e)}"
    