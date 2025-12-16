import httpx
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def static_scrape(url: str):
    # ---------- SAFE DEFAULTS ----------
    headings = []
    links = []
    images = []
    raw_html = ""
    truncated = False

    # ---------- FETCH ----------
    response = httpx.get(url, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # ---------- META ----------
    title = ""
    if soup.title and soup.title.string:
        title = soup.title.string.strip()

    description = ""
    desc_tag = soup.find("meta", attrs={"name": "description"})
    if desc_tag and desc_tag.get("content"):
        description = desc_tag["content"].strip()

    language = ""
    html_tag = soup.find("html")
    if html_tag and html_tag.get("lang"):
        language = html_tag.get("lang")

    canonical = None
    canon_tag = soup.find("link", rel="canonical")
    if canon_tag and canon_tag.get("href"):
        canonical = canon_tag["href"]

    # ---------- HEADINGS ----------
    for h in soup.find_all(["h1", "h2", "h3"]):
        text = h.get_text(strip=True)
        if text:
            headings.append(text)

    # ---------- LINKS ----------
    for a in soup.find_all("a", href=True):
        href = urljoin(url, a["href"])
        text = a.get_text(strip=True)
        if href:
            links.append({
                "text": text,
                "href": href
            })

    # ---------- IMAGES ----------
    for img in soup.find_all("img", src=True):
        src = urljoin(url, img["src"])
        alt = img.get("alt", "")
        images.append({
            "src": src,
            "alt": alt
        })

    # ---------- RAW HTML ----------
    main_tag = soup.find("main") or soup.body
    if main_tag:
        raw_html = str(main_tag)

    MAX_HTML_LEN = 1000
    if len(raw_html) > MAX_HTML_LEN:
        raw_html = raw_html[:MAX_HTML_LEN]
        truncated = True

    # ---------- TEXT CONTENT ----------
    text_blocks = []
    for p in soup.find_all("p"):
        text = p.get_text(strip=True)
        if text:
            text_blocks.append(text)

    full_text = " ".join(text_blocks[:5])

    # ---------- LABEL ----------
    label = "Main Content"
    if headings:
        label = headings[0][:50]

    # ---------- SECTION ----------
    section = {
        "id": "section-0",
        "type": "section",
        "label": label,
        "sourceUrl": url,
        "content": {
            "headings": headings,
            "text": full_text,
            "links": links,
            "images": images,
            "lists": [],
            "tables": []
        },
        "rawHtml": raw_html,
        "truncated": truncated
    }

    # ---------- FINAL RETURN ----------
    return {
        "meta": {
            "title": title,
            "description": description,
            "language": language,
            "canonical": canonical
        },
        "sections": [section]
    }
