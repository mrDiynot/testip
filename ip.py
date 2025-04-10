import streamlit as st
import requests

# Fetch IP directly from the API
response = requests.get("https://api.ipify.org")
ip_address = response.text

# Store in variable and display
st.write(f"Your IP address is: {ip_address}")

# If you still want to show the iframe for some reason
st.markdown('<iframe src="https://api.ipify.org" width="100%" height="50"></iframe>', unsafe_allow_html=True)
