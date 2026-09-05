#!/usr/bin/env python3

from pathlib import Path

from pypdf import PdfReader


PDF_PATH = Path(
    "data/staging/raw/city_austin/"
    "initial_draft_recommendation/2026-01-21/source.pdf"
)

reader = PdfReader(PDF_PATH)

print("Physical PDF pages:", len(reader.pages))
print()

keywords = (
    "Transportation",
    "Parks",
    "Watershed",
    "Library",
    "Libraries",
    "Public Safety",
    "Public Health",
    "Cultural",
    "Fleet",
    "Animal",
    "Court",
    "Strategic Alignment",
    "Critical Asset",
    "Community Consideration",
    "Efficiency",
    "Timeliness",
    "Climate Resilience",
)

for page_number, page in enumerate(reader.pages, start=1):
    text = page.extract_text() or ""

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    hits = [
        keyword
        for keyword in keywords
        if keyword.lower() in text.lower()
    ]

    print("=" * 80)
    print(f"PHYSICAL PAGE {page_number}")
    print("=" * 80)

    print("Keyword hits:", hits)

    print("\nFirst 25 extracted lines:")
    for line in lines[:25]:
        print(" ", line)

    print()