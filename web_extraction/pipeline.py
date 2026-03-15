import sys
import time
from scraper import scrape_article
from ai_extractor import extract_location
from geocoder import get_coordinates
from database import init_db, save_record

def process_traffic_article(url):
    print(f"[State 1] Scraping data from URL: \n{url}")
    article_text = scrape_article(url)

    if not article_text:
        print("ERROR: Unable to retrieve the article content.")
        print("Stop processing.")
        return
    
    print()
    print("Successfully!")
    print(f"The number of characters obtained is: {len(article_text)}")
    print("-" * 40)

    print("[State 2] AI is extracting location...")
    location = extract_location(article_text)

    if location in ["Unknown", "Error"]:
        print("Location not clearly identified. Processing stopped.")
        return

    print(f"LOCATION: {location}")
    print("-" * 40)

    print("[State 3] Translating place names to GPS coordinates...")
    lat, lon = get_coordinates(location)

    if lat and lon:
        print(f"Coordinates obtained: Latitude {lat}, Longitude {lon}")
        print("-" * 40)
        print("[STATE 4] Saving to database...")
        save_record(url, location, lat, lon)
    else:
        print("Error: Coordinates not found. Skip archiving.")
    
    print("ARTICLE PROCESSING COMPLETED.")
    print("-" * 40)
    
# Test
if __name__ == "__main__":
    init_db()
    
    test_url = [
        "https://vov.vn/xa-hoi/tai-nan-giao-thong-tai-dong-thap-lam-1-nguoi-tu-vong-2-nguoi-bi-thuong-post1275893.vov",
        "https://congan.com.vn/giao-thong-24h/ba-nguoi-trong-mot-gia-dinh-thuong-vong-tren-cao-toc-cam-lam-vinh-hao_190172.html",
        "https://www.sggp.org.vn/xe-dau-keo-boc-chay-mot-nguoi-tu-vong-post842902.html",
        "https://cadn.com.vn/tai-nan-giao-thong-chet-nguoi-post338061.html",
        "https://vov.vn/xa-hoi/xe-tai-tong-vao-duoi-xe-dau-keo-dung-ben-duong-1-nguoi-tu-vong-post1275106.vov"
    ]

    print(f"Start batch processing {len(test_url)} articles...\n")

    for i, url in enumerate(test_url):
        print(f"Processing the {i+1}/{len(test_url)} article")
        process_traffic_article(url)

        print("Sleep 3 seconds...\n")
        time.sleep(3)
    
    print("Successfully.")