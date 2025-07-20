from bs4 import BeautifulSoup
import re

def clean_html_article(html_text):
    soup = BeautifulSoup(html_text, "html.parser")

    # Remove scripts, styles, noscripts, images, footers, buttons, etc.
    for tag in soup(['script', 'style', 'noscript', 'abbr', 'img', 'button', 'footer']):
        tag.decompose()

    # Remove common ad/dialog/modal classes
    for tag in soup.find_all(True, {'class': re.compile(r'(cta|ad|access-|dialog|modal|backdrop)', re.IGNORECASE)}):
        tag.decompose()

    # Use <main> if exists, else fallback to biggest <div> block
    main_content = soup.find("main") or max(
        soup.find_all("div"), key=lambda d: len(d.get_text(strip=True)), default=soup
    )

    # Collect content from headers, paragraphs, and lists
    content_parts = []
    for tag in main_content.find_all(['h1', 'h2', 'h3', 'p', 'ul', 'ol']):
        if tag.name in ['ul', 'ol']:
            for li in tag.find_all('li'):
                content_parts.append(f"- {li.get_text(strip=True)}")
        else:
            content_parts.append(tag.get_text(strip=True))

    # Join and normalize whitespace
    content = '\n'.join(content_parts)
    content = re.sub(r'\n+', '\n', content)

    return content.strip()

def extract_symptom_section(html_text):
    pattern = re.compile(r'<h2>\s*Symptoms.*?</h2>(?P<section>.*?)(?=<h2>)',
                         re.DOTALL | re.IGNORECASE)
    match = pattern.search(html_text)
    if match:
        symptoms_html = match.group('section')
        items = re.findall(r'<li>(.*?)</li>', symptoms_html, flags=re.DOTALL)
        symptoms = [re.sub(r'<.*?>', '', itm).strip() for itm in items]
        return symptoms
    return []

# Load the raw HTML file
with open("file.html", "r", encoding="utf-8") as file:
    html_text = file.read()

# Optional: Extract specific content like symptom list
symptoms = extract_symptom_section(html_text)
# if symptoms:
#     with open("symptoms.txt", "w", encoding="utf-8") as f:
#         f.write('\n'.join(symptoms))

# Extract cleaned readable content
content = clean_html_article(html_text)
# with open("extract.txt", "w", encoding="utf-8") as f:
#     f.write(content)
