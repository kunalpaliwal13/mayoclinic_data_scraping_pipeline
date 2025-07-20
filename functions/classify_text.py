import re
from collections import defaultdict

section_headers = ["Symptoms", "Causes", "Diagnosis", "Treatment", "Prevention", "Overview", "Complications"]
noise_keywords = [
    "Mayo Clinic Press", "Newsletter", "Give Now", "CON-", "Advertising", "Terms and Conditions",
    "Sponsorship", "Locations", "Social media", "Connect with others", "Follow Mayo Clinic",
    "Explore careers", "Media Requests", "Medical Professionals", "Site Map", "Manage Cookies",
    "A Book:", "Products & Services", "Language:", "©"
]

def remove_noise(text):
    lines = text.splitlines()
    cleaned = []
    for line in lines:
        if line.strip() and not any(kw.lower() in line.lower() for kw in noise_keywords):
            cleaned.append(line.strip())
    return "\n".join(cleaned).strip()

def extract_sections_from_text(text):
    # Use regex to match section headers like "Symptoms" or "Symptoms of XYZ"
    pattern = re.compile(rf"(?P<header>\b(?:{'|'.join(section_headers)})\b[^\n\r:]*):?", re.IGNORECASE)

    matches = list(pattern.finditer(text))
    sections = defaultdict(str)

    for i, match in enumerate(matches):
        header_text = match.group("header").strip()
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        content = text[start:end].strip()

        # Normalize section name
        for h in section_headers:
            if h.lower() in header_text.lower():
                section_key = h.lower()
                break
        else:
            section_key = header_text.lower()

        cleaned = remove_noise(content)

        # Append, don't overwrite — many pages have repeated "Symptoms"
        if cleaned:
            if sections[section_key]:
                sections[section_key] += "\n\n" + cleaned
            else:
                sections[section_key] = cleaned

    return dict(sections)


def truncate_at(text, stop_phrases):
    for phrase in stop_phrases:
        idx = text.lower().find(phrase.lower())
        if idx != -1:
            return text[:idx]
    return text




with open("processed_files/text.txt", "r", encoding="utf-8") as f:
    plain_text = f.read()

text = truncate_at(plain_text, ["Get the Mayo Clinic app", "Mayo Clinic Minute:", "Show more"])


sections = extract_sections_from_text(text)

# Save each section
with open("extracted_sections.txt", "w", encoding="utf-8") as f:
    for section, content in sections.items():
        f.write(f"\n=== {section.title()} ===\n")
        f.write(content + "\n")