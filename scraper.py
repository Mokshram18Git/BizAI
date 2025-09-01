import requests
from bs4 import BeautifulSoup

def scrape_content(urls):
    documents = []
    headers = {"User-Agent": "Mozilla/5.0"}

    for url in urls:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")

            paragraphs = soup.find_all(["p", "h2", "h3"])
            text = "\n".join(p.get_text().strip() for p in paragraphs)
            if len(text) > 200:
                documents.append({"url": url, "text": text})
        except Exception:
            continue

    return documents
