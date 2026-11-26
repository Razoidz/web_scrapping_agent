import requests
from bs4 import BeautifulSoup


def scrape_article_headlines(url: str) -> list[str]:
    """Fetches a news URL and extracts clean headline text from h2/h3 tags."""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
        )
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Remove nav, header, and footer so we don't grab menu items
        for tag in soup(["nav", "header", "footer", "aside"]):
            tag.decompose()

        headlines = []
        seen = set()

        # Check both h2 and h3 (Premium Times uses h3 for most front-page stories)
        for tag in soup.find_all(["h2", "h3"]):
            text = tag.get_text(" ", strip=True)
            # Keep real headlines (> 20 chars) and deduplicate
            if len(text) > 20 and text not in seen:
                seen.add(text)
                headlines.append(text)

        return headlines
    except requests.RequestException as e:
        return [f"Error fetching URL: {e}"]

