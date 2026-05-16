import re
import requests
from bs4 import BeautifulSoup
from serpapi_client import search_google


def find_pycon_floorplan_url():
    results = search_google(
        'Booth Assignments PyCon US 2026 sheet python.org floorplan2026',
        num=5
    )

    for item in results:
        link = item.get("link", "")
        if "python.org/floorplan2026" in link:
            return link

    return "https://www.python.org/floorplan2026/"


def extract_google_sheet_url(floorplan_url):
    html = requests.get(floorplan_url, timeout=10).text
    soup = BeautifulSoup(html, "html.parser")

    for a in soup.find_all("a", href=True):
        text = a.get_text(" ", strip=True).lower()
        href = a["href"]

        if "booth assignments" in text and "docs.google.com" in href:
            return href

    return None


def google_sheet_to_csv_url(sheet_url):
    match = re.search(r"/spreadsheets/d/([a-zA-Z0-9-_]+)", sheet_url)

    if not match:
        return None

    sheet_id = match.group(1)
    return f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"


def find_org_booth(org_name):
    floorplan_url = find_pycon_floorplan_url()
    sheet_url = extract_google_sheet_url(floorplan_url)

    if not sheet_url:
        return {
            "found": False,
            "error": "Could not find booth assignment Google Sheet.",
            "floorplan_url": floorplan_url
        }

    csv_url = google_sheet_to_csv_url(sheet_url)

    response = requests.get(csv_url, timeout=15)
    csv_text = response.text

    org_lower = org_name.lower()

    matching_lines = [
        line for line in csv_text.splitlines()
        if org_lower in line.lower()
    ]

    if not matching_lines:
        return {
            "found": False,
            "org": org_name,
            "floorplan_url": floorplan_url,
            "sheet_url": sheet_url,
            "message": f"{org_name} was not found in the PyCon US 2026 booth assignment sheet."
        }

    return {
        "found": True,
        "org": org_name,
        "matches": matching_lines,
        "floorplan_url": floorplan_url,
        "sheet_url": sheet_url
    }