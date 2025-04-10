import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="IP Address Detector", page_icon="🔍")
st.title("IP Address Detector")

# Get server-side IP address
try:
    response = requests.get('https://api.ipify.org?format=json')
    ip_data = response.json()
    ip_address = ip_data['ip']
except Exception as e:
    ip_address = "Failed to detect"

st.subheader("Your IP Address (server-side)")
st.write(ip_address)

# Show client-side detection
st.subheader("Client-side Detection")

# JavaScript to get client IP and set it into a hidden text input
st.components.v1.html("""
<script>
    async function getIP() {
        const res = await fetch('https://api.ipify.org?format=json');
        const data = await res.json();
        const ip = data.ip;
        const input = window.parent.document.querySelector('input[data-testid="stTextInput"]');
        if (input) {
            input.value = ip;
            const event = new Event('input', { bubbles: true });
            input.dispatchEvent(event);
        }
    }
    getIP();
</script>
""", height=0)

# Hidden text input to receive the IP
client_ip = st.text_input("Your IP Address (client-side)", value="", label_visibility="collapsed")

# If value was set via JS, show it
if client_ip:
    st.success(f"Detected client-side IP: {client_ip}")
