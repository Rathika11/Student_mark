import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

st.title("🌦 5-Day Weather Forecast Dashboard")

API_KEY = "YOUR_API_KEY"  # Get free key from https://openweathermap.org/api
city = st.text_input("Enter a city name", "Chennai")

if st.button("Get Forecast"):
    if API_KEY == "YOUR_API_KEY":
        st.error("Please add your OpenWeatherMap API key in the code.")
    else:
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            forecast_list = data["list"]

            forecast_data = []
            for item in forecast_list:
                forecast_data.append({
                    "Datetime": item["dt_txt"],
                    "Temp": item["main"]["temp"],
                    "Feels Like": item["main"]["feels_like"],
                    "Humidity": item["main"]["humidity"],
                    "Description": item["weather"][0]["description"].capitalize()
                })

            df = pd.DataFrame(forecast_data)

            # Show preview
            st.subheader(f"📍 5-Day Forecast for {city}")
            st.dataframe(df.head(10))

            # Daily average temperature
            df["Date"] = pd.to_datetime(df["Datetime"]).dt.date
            daily_avg = df.groupby("Date")["Temp"].mean()

            # Plot
            fig, ax = plt.subplots()
            daily_avg.plot(kind="line", marker="o", ax=ax)
            ax.set_title(f"Average Temperature for Next 5 Days in {city}")
            ax.set_ylabel("Temperature (°C)")
            ax.set_xlabel("Date")
            plt.xticks(rotation=45)
            st.pyplot(fig)

            st.success("✅ Forecast loaded successfully!")
        else:
            st.error("City not found. Please try again.")
