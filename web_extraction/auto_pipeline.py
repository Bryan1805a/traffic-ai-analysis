import time
import schedule
import requests
from bs4 import BeautifulSoup

from scraper import scrape_article
from ai_extractor import extract_accident_info
from geocoder import get_coordinates
from database import init_db, save_record

def get_latest_new_urls():
    rss_url = "https://vnexpress.net/rss/thoi-su.rss"
    print(f"Scanning for the latest news from: {rss_url}")

    try:
        response = requests.get(rss_url)
        soup = BeautifulSoup(response.content, features="xml")

        links = soup.findAll("link")
        urls = [link.text for link in links if "vnexpress.net" in link.text and ".html" in link.text]
        return urls
    except Exception as e:
        print(f"Error when scanning RSS: {e}")
        return []
    
def process_traffic_article(url):
    print(f"[-] Processing URL: {url}")
    article_text = scrape_article(url)
    if not article_text: return

    info = extract_accident_info(article_text)
    if not info or info.get("location") in ["Unknow", "Error", None]:
        print("This isn't a clear traffic accident report. Ignore it.")
        return
    
    location = info["location"]
    deaths = info.get("deaths", 0)
    injuries = info.get("injuries", 0)
    vehicles = info.get("vehicles", "Nothing")

    print(f"Analysing: {location} | Deaths: {deaths} | Injuries: {injuries}")
    lat, lon = get_coordinates(location)

    if lat and lon:
        save_record(url, location, lat, lon, deaths, injuries, vehicles)
    else:
        print("Coordinate error.")

def hourly_job():
    print(f"\n{'=' * 50}")
    print(f"BEGIN THE UPDATE CYCLE: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\n{'=' * 50}")

    urls = get_latest_new_urls()    
    print(f"[!] Found {len(urls)} new articles in RSS.")

    for url in urls:
        process_traffic_article(url)
        time.sleep(3)
    
    print(f"\n SUCCESSFULLY.")

if __name__ == "__main__":
    init_db()

    hourly_job()

    schedule.every(1).hours.do(hourly_job)

    print("\n The Auto-Update system is running in the background. Press Ctrl+C to exit.")
    while True:
        schedule.run_pending()
        time.sleep(60)