import streamlit as st
import pandas as pd
import requests
import time
import json
from datetime import datetime

# --- CONFIGURATION ---
URI = 'https://api.football-data.org/v4/matches'
HEADERS = {'X-Auth-Token': '8c43d15eed7f47fdbb5eb931ea127152'}

st.set_page_config(page_title="Football Match Scanner", layout="wide")

st.title("⚽ Football Match Scanner")
st.write(f"🔍 Monitoring API: football-data.org")

def get_match_data():
    try:
        response = requests.get(URI, headers=HEADERS)
        if response.status_code != 200:
            st.error(f"API Error {response.status_code}: {response.text}")
            return []
        data = response.json()
        return data.get('matches', [])
    except Exception as e:
        st.error(f"Connection Error: {e}")
        return []

placeholder = st.empty()

while True:
    with placeholder.container():
        raw_data = get_match_data()
        results = []

        if not raw_data:
            # If empty, let's explain why
            st.warning(f"No matches found at {time.strftime('%H:%M:%S')}.")
            st.info("💡 Tip: Matches may not be available at this time or API limits may apply.")
        else:
            for match in raw_data:
                # Extracting Data from football-data.org API
                home_team = match.get('homeTeam', {}).get('name', 'N/A')
                away_team = match.get('awayTeam', {}).get('name', 'N/A')
                competition = match.get('competition', {}).get('name', 'Other')
                status = match.get('status', 'UNKNOWN')
                
                # Current Score
                h_score = match.get('score', {}).get('fullTime', {}).get('home', 0)
                a_score = match.get('score', {}).get('fullTime', {}).get('away', 0)
                
                # Match time (if live)
                match_time = ''
                if status == 'IN_PLAY':
                    match_time = 'LIVE'
                elif status == 'PAUSED':
                    match_time = 'PAUSED'
                else:
                    match_time = status

                results.append({
                    "Status": match_time,
                    "Competition": competition,
                    "Match": f"{home_team} vs {away_team}",
                    "Score": f"{h_score}-{a_score}"
                })

        if results:
            df = pd.DataFrame(results)
            st.table(df)
            st.success(f"Successfully tracking {len(results)} matches.")

    time.sleep(60)