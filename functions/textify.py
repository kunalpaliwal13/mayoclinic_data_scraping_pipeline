from bs4 import BeautifulSoup

# Load the HTML file
with open("file.html", "r", encoding="utf-8") as f:
    html = f.read()

# Parse HTML
soup = BeautifulSoup(html, "html.parser")

# Remove only irrelevant tags
for tag in soup(["script", "style", "noscript", "meta", "link"]):
    tag.decompose()

# Get all meaningful text including from <a>, <li>, etc.
text = soup.get_text(separator="\n", strip=True)

# Optional: Filter out very short/noisy lines
lines = [line for line in text.split("\n") if len(line.strip()) > 1]

# Save to file
with open("text.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"✅ Extracted {len(lines)} lines of visible text.")
