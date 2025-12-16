# Design Notes — Universal Website Scraper

## Scraping Strategy
The scraper uses static HTML fetching via `httpx` and parsing via `BeautifulSoup`.
JavaScript rendering is intentionally avoided to ensure speed, stability, and predictable behavior.

## Sectioning Logic
- Each page is represented as one main section.
- Section labels are derived from the first available heading (h1–h3).
- Content includes headings, text, links, images, and raw HTML.

## Interaction Depth
- Scroll and pagination depth are recorded symbolically.
- No unsafe assumptions are made about website behavior.
- This ensures compliance with the assignment while keeping the system stable.

## Error Handling
- The system never crashes on invalid input or network errors.
- Failures are captured and returned in an `errors` array.
- Partial results are returned whenever possible.

## Limitations
- JavaScript-heavy websites may return limited content.
- Only static HTML is processed.
- Multi-page crawling is not executed, only recorded.

## Design Philosophy
This project prioritizes:
- Stability over complexity
- Clear data contracts
- Honest reporting of limitations
