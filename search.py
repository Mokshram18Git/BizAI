import requests
from bs4 import BeautifulSoup

def get_search_results(query, max_results=5):
    headers = {"User-Agent": "Mozilla/5.0"}
    search_url = f"https://html.duckduckgo.com/html/?q={query}"
    res = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    links = []
    for a in soup.find_all("a", class_="result__a", limit=max_results):
        href = a.get("href")
        if href and href.startswith("http"):
            links.append(href)
    return links
