import requests
import time

def retrieve(url):
    time.sleep(2)
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/114.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "DNT": "1",
    }

    r = requests.get(url, headers=headers)
    r.raise_for_status()
    print(f'Extracting {url} info......')
    
    with open("file.html", "w", encoding="utf-8") as fw:
        fw.write(r.text)
    
    print("✅ HTML saved to file.html successfully.")

retrieve("https://www.mayoclinic.org/diseases-conditions/atrial-fibrillation/symptoms-causes/syc-20350624")
