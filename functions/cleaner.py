import re

def extract_symptoms_section(text):
    match = re.search(r"(?i)symptoms(.*?)\n[A-Z][^\n]{3,50}\n", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None

with open("meaningful_text.txt", "r")as file:
    text = file.read()
    print(text)

print(extract_symptoms_section(text))