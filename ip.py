import streamlit as st
from datetime import datetime
import requests

st.set_page_config(page_title="IP Address Detector", page_icon="🔍")
st.title("IP Address Detector")

# Detect server-side IP
try:
    response = requests.get('https://api.ipify.org?format=json')
    ip_address = response.json()['ip']
except Exception as e:
    ip_address = "Failed to detect"
st.subheader("Your IP Address (detected server-side)")
st.write(ip_address)

# Placeholder for client-side IP
st.subheader("Client-side Detection")
client_ip_placeholder = st.empty()

# HTML with postMessage
html_code = """
<script>
    async function getClientIP() {
        const res = await fetch('https://api.ipify.org?format=json');
        const data = await res.json();
        const ip = data.ip;
        window.parent.postMessage({ type: 'CLIENT_IP', ip: ip }, '*');
    }
    getClientIP();
</script>
"""

st.components.v1.html(html_code, height=0)

# Get IP from postMessage
from streamlit_javascript import st_javascript

client_ip = st_javascript(
    """
    new Promise((resolve) => {
        window.addEventListener("message", (event) => {
            if (event.data.type === "CLIENT_IP") {
                resolve(event.data.ip);
            }
        }, false);
    });
    """
)

# Display result
if client_ip:
    client_ip_placeholder.write(f"Your IP Address (client-side): {client_ip}")
    st.session_state['client_ip'] = client_ip
