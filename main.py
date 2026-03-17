import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import sqlite3

# Page configuration
st.set_page_config(page_title="Vietnam Traffic Accident Monitor", layout="wide")
st.title("VIETNAM TRAFFIC ACCIDENT MONITOR")

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

# Metrics
if not df.empty:
    total_cases = len(df)
    total_deaths = int(df['deaths'].sum())
    total_injuries = int(df['injuries'].sum())

    # The province that has highest accident cases
    top_location = df['location'].value_counts().idxmax() if not df["location"].empty else "Nothing"

    # The vehicle that has highest appearance
    top_vehicle = df['vehicles'].value_counts().idxmax() if not df['vehicles'].empty else "Nothing"
else:
    total_cases = total_deaths = total_injuries = 0
    top_location = top_vehicle = "Nothing"

# Web layout
met1, met2, met3, met4 = st.columns(4)
with met1:
    st.metric(label="Total number of cases", value=f"{total_cases} Cases")
with met2:
    st.metric(label="Casualties (Deaths / Injuries)", value=f"{total_deaths} / {total_injuries}")
with met3:
    st.metric(label="Province on red alert", value=top_location)
with met4:
    st.metric(label="Popular means of transport", value=top_vehicle)

st.markdown("---")

col1, col2 = st.columns([1, 2.5])

# Left column: Statistics and articles
with col1:
    st.subheader("Statistics by region")

    if not df.empty:
        stats = df['location'].value_counts()
        st.bar_chart(stats)

        st.markdown("Detailed data")
        for index, row in df.iterrows():
            st.markdown(f"- **{row['location']}** (Deaths: {row['deaths']} | Injuries: {row['injuries']}): [View the news]({row['url']})")
    else:
        st.info("No data available. Please run the pipeline.py file.")

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
                popup_html = f"""
                <div style='font-family: Arial; min-width: 150px;'>
                    <h4 style='margin-top: 0; color: #d63031;'>{row['location']}</h4>
                    <b>Tử vong:</b> {row['deaths']}<br>
                    <b>Bị thương:</b> {row['injuries']}<br>
                    <b>Phương tiện:</b> {row['vehicles']}
                </div>
                """

                folium.Marker(
                    location=[row['latitude'], row['longitude']],
                    popup=folium.Popup(popup_html, max_width=300),
                    tooltip=f"{row['location']} - Click để xem chi tiết",
                    icon=folium.Icon(color="red", icon="info-sign")
                ).add_to(m)

    st_folium(m, width=900, height=600)