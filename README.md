# Newspaper Headline Comparison

A small Python app that collects front-page headlines from Nigerian newspaper homepages and uses Google Gemini to compare their coverage, framing, and editorial tone.

## How it works

`main.py` registers `scrape_newspaper` as a Gemini tool. Gemini calls it for each newspaper URL in the prompt, and the scraper in `webscrapper_tool.py` fetches the page and extracts unique text from `<h2>` and `<h3>` elements. Up to 20 headlines per site are returned to Gemini for analysis.

The comparison is organized into:

- Shared top stories and differences in framing
- Unique angles or stories
- Overall editorial tone

The script tries the configured Gemini models in order and uses the first one that succeeds.

## Requirements

- Python 3.10 or newer
- A Google Gemini API key

## Setup

Create and activate a virtual environment, then install the dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install requests beautifulsoup4 google-genai python-dotenv
```

On Windows PowerShell, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

Create a `.env` file in the project directory and add your key:

```dotenv
GEMINI_API_KEY=your_gemini_api_key
```

`main.py` loads `.env` with `python-dotenv`, and the Google GenAI client reads `GEMINI_API_KEY` from the environment.

## Run

```bash
python main.py
```

The comparison is printed to the terminal. The newspaper URLs and prompt are currently defined in `main.py`; edit them there to compare different sites or change the requested analysis.

## Project files

- `main.py` — configures the Gemini client, tool, prompt, and model fallback order
- `webscrapper_tool.py` — fetches a page and extracts headlines from its HTML

## Notes and limitations

- Headline extraction is based on static HTML `<h2>` and `<h3>` tags. Sites that render content with JavaScript, use other elements, or block automated requests may return few headlines or none.
- The scraper skips navigation, header, footer, and aside elements and removes duplicate headlines. It returns a readable error string if a request fails.
- The analysis reflects the headlines available when the script runs; it does not verify story details or establish that a headline is an exclusive.
- Keep `.env` private and do not commit API keys.
# web_scrapping_agent
