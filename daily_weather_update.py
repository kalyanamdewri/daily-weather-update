#!/usr/bin/env python3
"""
Daily Weather Update
Personal Project

- Fetches weather forecast data from the Dark Sky API for a given location.
- Sends a daily weather email using Python's smtplib and ssl libraries.
"""

import requests
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ---------------------- Configuration ---------------------- #
# Dark Sky API configuration
DARK_SKY_API_KEY = "YOUR_DARK_SKY_API_KEY"  # Replace with your Dark Sky API key
LATITUDE = "YOUR_LATITUDE"                  # e.g., "37.8267"
LONGITUDE = "YOUR_LONGITUDE"                # e.g., "-122.4233"

# Email configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465                           # Port for SSL
EMAIL_SENDER = "YOUR_EMAIL@gmail.com"       # Your email address
EMAIL_PASSWORD = "YOUR_EMAIL_PASSWORD"      # Your email password or app-specific password
EMAIL_RECEIVER = "RECIPIENT_EMAIL@gmail.com"  # Recipient email address (can be the same as sender)
# ----------------------------------------------------------- #

def get_weather_data():
    """
    Fetches weather data from the Dark Sky API.
    
    Returns:
        dict: Parsed JSON response containing weather data.
        
    Raises:
        Exception: If the API call fails.
    """
    url = f"https://api.darksky.net/forecast/{DARK_SKY_API_KEY}/{LATITUDE},{LONGITUDE}?units=us"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch weather data: {response.status_code} - {response.text}")

def format_weather_email(weather_json):
    """
    Formats the weather data into a plain-text email message.
    
    Args:
        weather_json (dict): The JSON data from the Dark Sky API.
    
    Returns:
        str: The formatted email message.
    """
    current = weather_json.get("currently", {})
    summary = current.get("summary", "No summary available")
    temperature = current.get("temperature", "N/A")
    humidity = current.get("humidity", "N/A")
    wind_speed = current.get("windSpeed", "N/A")
    
    message = (
        "Daily Weather Update:\n\n"
        f"Summary: {summary}\n"
        f"Temperature: {temperature}°F\n"
        f"Humidity: {humidity}\n"
        f"Wind Speed: {wind_speed} mph\n"
    )
    return message

def send_email(message):
    """
    Sends the weather update email using SMTP over SSL.
    
    Args:
        message (str): The email message content.
    """
    subject = "Daily Weather Update"
    email_message = MIMEMultipart()
    email_message["Subject"] = subject
    email_message["From"] = EMAIL_SENDER
    email_message["To"] = EMAIL_RECEIVER
    email_message.attach(MIMEText(message, "plain"))
    
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, email_message.as_string())

if __name__ == "__main__":
    try:
        weather_data = get_weather_data()
        email_content = format_weather_email(weather_data)
        send_email(email_content)
        print("Email sent successfully!")
    except Exception as e:
        print("Error:", e)
