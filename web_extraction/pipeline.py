from scraper import scrape_article
from ai_extractor import extract_location

def process_traffic_article(url):
    print(f"[State 1] Scraping data from URL: \n{url}")
    article_text = scrape_article(url)

    if not article_text:
        print("ERROR: Unable to retrieve the article content.")
        print("Stop processing.")
        return None
    
    print("Successfully!")
    print(f"The number of characters obtained is: {len(article_text)}")
    print("------")

    print("[State 2] Sending content to Gemini to extract location...")

    location = extract_location(article_text)

    print("-" * 40)
    print(f"RESULT: {location}")
    print("-" * 40)

    return location

if __name__ == "__main__":
    test_url = "https://congan.com.vn/giao-thong-24h/ba-nguoi-trong-mot-gia-dinh-thuong-vong-tren-cao-toc-cam-lam-vinh-hao_190172.html"

    process_traffic_article(test_url)