import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import sqlite3

# Page configuration
st.set_page_config(page_title="Vietnam Traffic Accident Terminal", layout="wide")
st.title("Vietnam Traffic Accident Analysis Map")

# Read data from database
def load_data():
    try:
        conn = sqlite3.connect("data/traffic_accident_data.db")
        df = pd.read_sql_query("SELECT * FROM accidents", conn)
        conn.close()
        return df
    except Exception as e:
        return pd.DataFrame()

df = load_data()

st.markdown("---")
# Web layout
met1, met2, met3, met4 = st.columns(4)

with met1:
    st.metric(label="Total number of incidents (Recorded)", value="150", delta="+3")
with met2:
    st.metric(label="Casualties", value="45", delta="-2% compared to last week", delta_color="inverse")
with met3:
    st.metric(label="Province on red alert", value="Đồng Nai")
with met4:
    st.metric(label="Popular means of transport", value="Truck")

st.markdown("---")

col1, col2 = st.columns([1, 2.5])

# Left column: Statistics and articles
with col1:
    st.subheader("Statistics by region")

    if not df.empty:
        stats = df['location'].value_counts()
        st.bar_chart(stats)

        st.markdown("Latest News")
        for index, row in df.iterrows():
            st.markdown(f"- {row['location']}: [See the article]({row['url']})")
    else:
        st.info("No data available. Please run the pipeline.py file to scrape news.")

# Right column: Vietnam map
with col2:
    st.subheader("Black Spot Distribution Map")

    m = folium.Map(
        location=[16.047079, 108.206230],
        zoom_start=6,
        tiles="cartodbdark_matter"

    )

    if not df.empty:
        for index, row in df.iterrows():
            if pd.notna(row['latitude']) and pd.notna(row['longitude']):
                folium.Marker(
                    location=[row["latitude"], row['longitude']],
                    popup=f"Province/City: {row['location']}",
                    tooltip="Click to view details",
                    icon=folium.Icon(color="red", icon="info-sign")
                ).add_to(m)

    st_folium(m, width=900, height=600)