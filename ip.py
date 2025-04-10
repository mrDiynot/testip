import streamlit as st
import requests

# Get public IP address from ipify API
response = requests.get('https://api.ipify.org?format=json')

if response.status_code == 200:
    ip_data = response.json()
    ip_address = ip_data['ip']
    st.write("Your IP address is:", ip_address)
else:
    st.error("Failed to fetch IP address.")
