from webscrapper_tool import scrape_article_headlines
from google import genai
from google.genai import types
import time
from google.genai.errors import APIError
from dotenv import load_dotenv
load_dotenv()


def scrape_newspaper(url: str) -> str:
    """Scrapes the main front-page headlines from a given newspaper URL.

    Args:
        url: The full homepage URL of the newspaper (e.g., 'https://punchng.com').
    """
    raw_headlines = scrape_article_headlines(url)

    # Return up to 20 clean headlines to stay lightweight on free-tier tokens
    top_headlines = raw_headlines[:20]
    if not top_headlines:
        return "No headlines found."

    return "\n".join(f"- {h}" for h in top_headlines)


client = genai.Client()


models_to_try = [
    "gemini-3.7-flash",
    "gemini-3.8-flash",
    "gemini-3.6-flash",
    "gemini-3.5-flash-lite",
]

print("Available fallback order:", models_to_try)

system_instruction = """
You are a senior news editor. Your job is to fetch front-page headlines from 
requested newspapers using your `scrape_newspaper` tool, then analyze them.

Rules:
1. Call `scrape_newspaper` for EVERY newspaper URL provided by the user.
2. If one scraper call fails or returns empty text, note it and continue with the rest.
3. Compare the outlets across three sections:
   - Shared Top Stories (events covered by multiple papers & how their framing differs)
   - Unique Angles / Exclusive Stories (major stories only one paper is highlighting)
   - Overall Editorial Tone (e.g., political focus, business focus, sensational vs. neutral)
"""

prompt = """
Compare today's front-page headlines across these newspapers:
1. Punch Nigeria: https://punchng.com
2. Vanguard: https://vanguardngr.com
3. Premium Times: https://premiumtimesng.com
"""
# Using chats is best for agents so it remembers tool outputs across turns
for model_name in models_to_try:
    try:
        print(f"Running agent with {model_name}...")
        chat = client.chats.create(
            model=model_name,
            config=types.GenerateContentConfig(
                tools=[scrape_newspaper],
                system_instruction=system_instruction,
                temperature=0.2,
            ),
        )
        response = chat.send_message(prompt)
        print(response.text)
        break  
    except APIError as e:
        print(f"Skipping {model_name} ({e.code}): trying next model...")
        time.sleep(2)