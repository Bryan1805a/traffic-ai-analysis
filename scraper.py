import requests
from bs4 import BeautifulSoup

def scrape_article(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        
        paragraphs = soup.find_all('p')
        article_text = "\n".join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])

        return article_text
    except requests.exceptions.RequestException as e:
        print(f"Error while loading web: {e}")
        return None

if __name__ == "__main__":
    test_url = "https://vnexpress.net/xe-khach-tong-xe-tai-tren-cao-toc-cam-lo-la-son-2-nguoi-chet-4720448.html"

    print(f"Getting data from: {test_url}\n")
    content = scrape_article(test_url)

    if content:
        print("ARTICLE CONTENT AFTER SCRAPING")
        print(content[:500] + "\n...\n[The back section has been trimmed.]")
    else:
        print("Cannot load data. Please check URL or internet connection")