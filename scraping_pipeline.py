from functions.retrieving_html import retrieve
from functions.mayo_doc_clean import extract_symptom_section, clean_html_article
import requests
import os

# Ensure output directory exists
os.makedirs("extracted_files", exist_ok=True)

with open("links.txt", "r") as file:
    links = file.readlines()

for link in links:
    link = link.strip()  # Remove any trailing newline
    if not link:
        continue

    try:
        disease_name = link.split("/")[4].title()
        print(f"\n🩺 Processing: {disease_name} ({link})")
        
        retrieve(link)  # May raise an error

        with open("file.html", "r", encoding="utf-8") as file:
            html_text = file.read()

        symptoms = extract_symptom_section(html_text)
        content = clean_html_article(html_text)

        with open(f"extracted_files/{disease_name}.txt", "w", encoding="utf-8") as f:
            f.write(content)

        print(f"✅ Done: {disease_name}\n")

    except requests.exceptions.HTTPError as e:
        print(f"❌ Skipping {link} due to HTTP error: {e}")
        continue
    except Exception as e:
        print(f"⚠️ Unexpected error with {link}: {e}")
        continue
