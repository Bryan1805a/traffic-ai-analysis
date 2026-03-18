# Vietnam Traffic Accident Monitor

This project is an automated system that collects news about traffic accidents from official news outlets, uses Artificial Intelligence (Gemini AI) to extract multidimensional data (location, casualties, vehicle types), and visualizes it on a Dark Mode map styled as a global monitoring dashboard.

## Key Features
* **Fully Automated (Auto-Scraping):** Automatically scans RSS Feeds every hour to update the latest news without any manual intervention.
* **AI NLP Extraction:** Integrates Google Gemini 2.5 Flash to understand article context, filter out noise, and extract precise data into a structured JSON format.
* **Geocoding:** Automatically converts location names into exact GPS coordinates (Latitude/Longitude).
* **Monitoring Dashboard (Dark Mode):** A real-time Streamlit interface featuring overview statistics and an interactive map that highlights accident "black spots" across Vietnam.

## Tech Stack
* **Language:** Python 3.10+
* **Web Scraping:** `requests`, `BeautifulSoup`
* **AI / NLP:** `google-genai` (Gemini API)
* **Mapping & Geocoding:** `geopy`, `folium`, `streamlit-folium`
* **UI & Data Processing:** `streamlit`, `pandas`, `sqlite3`
* **Automation:** `schedule`

## Folder Structure
```text
traffic_ai_project/
├── data/
│   └── traffic_data.db       # SQLite database storing records (auto-generated)
|-- web_extraction/
|   |-- scraper.py            # Module for parsing HTML from news articles
|   |-- ai_extractor.py       # Module for calling Gemini API to extract JSON
|   |-- geocoder.py           # Module for fetching GPS coordinates
|   |-- database.py           # Module for SQLite operations
|   |-- auto_pipeline.py      # Background worker that scrapes news hourly
├── main.py                   # Streamlit UI Dashboard (Frontend)
└── README.md                 # Project documentation
```

# Installation & Setup
## Step 1: Initialize the Environment
Using Miniconda/Anaconda is highly recommended to manage the environment:
```
conda create -n traffic_ai python=3.10 -y
conda activate traffic_ai
pip install requests beautifulsoup4 google-genai python-dotenv geopy schedule streamlit folium streamlit-folium pandas lxml
```
## Step 2: Configure API Key
Create a .env file in the root directory and add your Google Gemini API Key:
```
GEMINI_API_KEY=your_google_gemini_api_key_here
```
## Step 3: Run the System
You need to open 2 independent Terminal windows:
Terminal 1 (Data Update Worker):
This process will initialize the Database, scan for new articles immediately, and continue running in the background every hour.
```
python auto_pipeline.py
```
Terminal 2 (Streamlit Dashboard):
Launch the UI Dashboard on your browser.
```
streamlit run main.py
```
Navigate to http://localhost:8501 to view the map.

# Disclaimer
This project is built for educational purposes to study the application of AI in spatial data analysis. The data is collected from public news sources and may not reflect the entirety of the actual traffic situation.
