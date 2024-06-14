import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import numpy as np
from game import check_winner,make_move


# Streamlit app title
st.title("WeatherWins")

# API Key (Replace with your own API key)
API_KEY = "c8a573b569dac996b41c2d0cca8041d7"

# Function to fetch weather data
def get_weather_data(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    return response.json()

def get_forecast_data(city):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    return response.json()

# Predefined song recommendations based on weather conditions
song_recommendations = {
    "clear sky": ["Here Comes the Sun - The Beatles", "Walking on Sunshine - Katrina and the Waves"],
    "few clouds": ["Clouds - Imagine Dragons", "Cloudy - Simon & Garfunkel"],
    "scattered clouds": ["Cloudy Day - Tones And I", "Both Sides Now - Joni Mitchell"],
    "broken clouds": ["Clouds - Newton Faulkner", "Clouds - Zach Sobiech"],
    "shower rain": ["Umbrella - Rihanna", "Singing in the Rain - Gene Kelly"],
    "rain": ["Raindrops Keep Fallin' on My Head - B.J. Thomas", "Have You Ever Seen the Rain - CCR"],
    "thunderstorm": ["Thunderstruck - AC/DC", "Thunder - Imagine Dragons"],
    "snow": ["Let It Snow! Let It Snow! Let It Snow! - Dean Martin", "Snow (Hey Oh) - Red Hot Chili Peppers"],
    "mist": ["Misty - Ella Fitzgerald", "Foggy Notion - The Velvet Underground"]
}

# User input
city = st.text_input("Enter a city name", "New York")

if city:
    # Fetch current weather data
    weather_data = get_weather_data(city)

    if weather_data['cod'] == 200:
        st.subheader(f"Current Weather in {city}")
        st.write(f"Temperature: {weather_data['main']['temp']}°C")
        st.write(f"Humidity: {weather_data['main']['humidity']}%")
        st.write(f"Wind Speed: {weather_data['wind']['speed']} m/s")
        weather_description = weather_data['weather'][0]['description']
        st.write(f"Weather: {weather_description}")

        # Recommend songs based on weather
        songs = song_recommendations.get(weather_description, ["No song recommendations available for this weather."])
        st.subheader("Song Recommendations")
        st.write("***let's enjoy the songs!***")
        for song in songs:
            st.write(f"- {song}")

        # Fetch weather forecast data
        forecast_data = get_forecast_data(city)
        forecast_list = forecast_data['list']

        # Process forecast data
        dates = []
        temperatures = []
        for forecast in forecast_list:
            dates.append(forecast['dt_txt'])
            temperatures.append(forecast['main']['temp'])

        # Create a DataFrame
        forecast_df = pd.DataFrame({
            'Date': dates,
            'Temperature': temperatures
        })

        # Plot temperature trend
        fig = px.line(forecast_df, x='Date', y='Temperature', title=f'Temperature Forecast for {city}')
        st.plotly_chart(fig)
    else:
        st.write("City not found. Please enter a valid city name.")

# Initialize the game state (move this part to the end of the script)
if "board" not in st.session_state:
    st.session_state.board = np.full((3, 3), "", dtype=str)
    st.session_state.current_player = "X"
    st.session_state.winner = None

# Title for the Tic-Tac-Toe game
st.header("Play Tic-Tac-Toe!")
st.write("***hey,let's play game!***")
# Display the board
for row in range(3):
    cols = st.columns(3)
    for col in range(3):
        if cols[col].button(st.session_state.board[row, col], key=f"{row}-{col}"):
            make_move(row, col)

# Display the winner
if st.session_state.winner:
    st.write(f"Player {st.session_state.winner} wins!")
elif np.all(st.session_state.board != ""):
    st.write("It's a draw!")

# Reset button
if st.button("Restart Game"):
    st.session_state.board = np.full((3, 3), "", dtype=str)
    st.session_state.current_player = "X"
    st.session_state.winner = None