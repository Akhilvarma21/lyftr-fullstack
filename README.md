# Universal Website Scraper — Lyftr AI Assignment

This project is a backend-focused universal website scraper built as part of the Lyftr AI internship assignment.

It accepts a website URL, performs safe static HTML scraping, structures the content into meaningful sections, and returns a clean JSON response. A minimal frontend is included for easy testing and visualization.

---

## 🚀 Features

- FastAPI backend with `/healthz` and `/scrape` endpoints  
- Static HTML scraping using `httpx` + `BeautifulSoup`  
- Extracts:
  - Page metadata (title, language, canonical)
  - Headings (h1–h3)
  - Text content
  - Links and images
- Section-based JSON structure
- Safe truncation of raw HTML
- Graceful error handling (no crashes)
- Minimal frontend UI for testing

---

## 📂 Project Structure

lyftr-fullstack/
│
├── app/
│ └── main.py
├── scraper/
│ └── static_scraper.py
├── templates/
│ └── index.html
├── requirements.txt
├── run.sh
├── README.md
├── design_notes.md
└── capabilities.json
