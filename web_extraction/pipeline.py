import sys
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
    
    test_url = "https://congan.com.vn/giao-thong-24h/ba-nguoi-trong-mot-gia-dinh-thuong-vong-tren-cao-toc-cam-lam-vinh-hao_190172.html"
    process_traffic_article(test_url)