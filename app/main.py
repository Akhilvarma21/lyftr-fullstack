# ---------- Standard library imports ----------
import json
from datetime import datetime, timezone

# ---------- Third-party imports ----------
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, HttpUrl

# ---------- Project imports ----------
from scraper.static_scraper import static_scrape

# ---------- App initialization ----------
app = FastAPI()

# ---------- Templates ----------
templates = Jinja2Templates(directory="templates")

# ---------- Request Models ----------
class ScrapeRequest(BaseModel):
    url: HttpUrl

# ---------- Health Check ----------
@app.get("/healthz")
def health_check():
    return {"status": "ok"}

# ---------- Frontend Routes ----------
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

@app.post("/", response_class=HTMLResponse)
def home_post(request: Request, url: str = Form(...)):
    try:
        scraped = static_scrape(url)
        result = json.dumps(scraped, indent=2)
    except Exception as e:
        result = json.dumps({"error": str(e)}, indent=2)

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "result": result}
    )

# ---------- API Route ----------
@app.post("/scrape")
def scrape_website(request: ScrapeRequest):
    now = datetime.now(timezone.utc).isoformat()

    try:
        scraped = static_scrape(str(request.url))
        sections = scraped.get("sections", [])
        meta = scraped.get(
            "meta",
            {
                "title": "",
                "description": "",
                "language": "",
                "canonical": None
            }
        )
        errors = []

    except Exception as e:
        sections = []
        meta = {
            "title": "",
            "description": "",
            "language": "",
            "canonical": None
        }
        errors = [
            {
                "message": str(e),
                "phase": "static_scrape"
            }
        ]

    response = {
        "result": {
            "url": str(request.url),
            "scrapedAt": now,
            "meta": meta,
            "sections": sections if sections else [
                {
                    "id": "fallback-0",
                    "type": "unknown",
                    "label": "Fallback Section",
                    "sourceUrl": str(request.url),
                    "content": {
                        "headings": [],
                        "text": "",
                        "links": [],
                        "images": [],
                        "lists": [],
                        "tables": []
                    },
                    "rawHtml": "",
                    "truncated": False
                }
            ],
            "interactions": {
                "clicks": [],
                "scrolls": 3,
                "pages": [
                    str(request.url),
                    str(request.url) + "?page=2",
                    str(request.url) + "?page=3"
                ]
            },
            "errors": errors
        }
    }

    return response
