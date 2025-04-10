import streamlit as st
from datetime import datetime
import requests

st.set_page_config(page_title="IP Address Detector", page_icon="🔍")

st.title("IP Address Detector")

# Get IP address server-side and store in variable
try:
    response = requests.get('https://api.ipify.org?format=json')
    ip_data = response.json()
    ip_address = ip_data['ip']
   
    print(f"IP 1: {ip_address}")
except Exception as e:
    ip_address = "Failed to detect"
    print(f"Error detecting IP: {e}")

# Display the server-detected IP
st.subheader("Your IP Address (detected server-side)")
st.write(ip_address)

# Create HTML/JS component to get client IP and extract from iframe
html_code = """
<div style="padding: 10px; background-color: #f0f2f6; border-radius: 5px;">
    <p style="font-weight: bold;">Your IP Address (client-side): <span id="ip-result">Detecting...</span></p>
</div>

<div style="padding: 10px; background-color: #e6f7ff; border-radius: 5px; margin-top: 10px;">
    <p style="font-weight: bold;">IP from iframe: <span id="iframe-ip">Loading...</span></p>
    <iframe id="ip-iframe" src="https://api.ipify.org" width="100%" height="30" style="border:none;"></iframe>
</div>

<script>
// Function to get client IP from API
async function getIP() {
    try {
        const response = await fetch('https://api.ipify.org?format=json');
        const data = await response.json();
        
        // Display the IP
        document.getElementById('ip-result').innerHTML = data.ip;
        
        // Log to console
        console.log('Client IP:', data.ip);
    } catch (error) {
        document.getElementById('ip-result').innerHTML = 'Error: ' + error;
    }
}

// Function to extract IP from iframe
function extractIpFromIframe() {
    const iframe = document.getElementById('ip-iframe');
    
    // Wait for iframe to load
    iframe.onload = function() {
        try {
            // Try to get the content
            const iframeContent = iframe.contentDocument || iframe.contentWindow.document;
            const ipText = iframeContent.body.innerText.trim();
            
            // Display the extracted IP
            document.getElementById('iframe-ip').innerText = ipText;
            
            // Store in a JavaScript variable for later use
            window.iframeIpAddress = ipText;
            
            // Log to console
            console.log('Iframe IP:', ipText);
        } catch (error) {
            document.getElementById('iframe-ip').innerText = 'Error accessing iframe content';
            console.error('Error:', error);
        }
    };
}

// Run both functions
getIP();
extractIpFromIframe();
</script>
"""

# Show the combined component
st.subheader("Client-side Detection (including iframe extraction)")
st.components.v1.html(html_code, height=150)

# For demonstration, show how to get the same data server-side
st.subheader("Server-side Method (same as iframe content)")
iframe_content = requests.get("https://api.ipify.org").text.strip()
st.write(f"Content from api.ipify.org: {iframe_content}")
st.write("Note: This is the same content that's loaded in the iframe above.")

# Add a refresh button
if st.button("Refresh"):
    st.experimental_rerun()

# Print to console log (server-side)
print(f"Page loaded at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Stored IP: {ip_address}")
print(f"Iframe content: {iframe_content}")
