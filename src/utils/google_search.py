from googlesearch import search
from re import search as re_search
from re import IGNORECASE

from urllib.parse import urlparse


def google_search(query) -> str:
    results = []
    for url in search(query, num_results=5):
        if any(job_board in url.lower() for job_board in ['linkedin', 'glassdoor', 'indeed', 'wuzzuf']):
            continue
        if not is_valid_url(url):
            continue
        if re_search(rf"{query}", url, IGNORECASE):
            continue
        else:
            results.append(url)

    if len(results) > 0:
        return results[0]

    return "not found"  # If no valid URL found


def is_valid_url(url: str) -> bool:
    parsed = urlparse(url)
    return bool(parsed.scheme) and bool(parsed.netloc)
