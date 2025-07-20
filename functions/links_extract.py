from bs4 import BeautifulSoup
from functions.retrieving_html import retrieve
import time

for i in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
    url = f"https://www.mayoclinic.org/diseases-conditions/index?letter={i}"

    retrieve(url)
    with open("file.html", "r") as file:
        text = file.read()

    soup = BeautifulSoup(text, "html.parser")
    pretty_html = soup.prettify()

    prefix = "https://www.mayoclinic.org/diseases-conditions/"
    hrefs = [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith(prefix)]


    for link in hrefs:
        with open("links.txt", "a") as file:
            file.write(link+"\n")
    time.sleep(2)

