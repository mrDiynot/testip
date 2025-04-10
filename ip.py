import streamlit as st
from datetime import datetime
import requests
import json

st.set_page_config(page_title="IP Address Detector", page_icon="🔍")

st.title("IP Address Detector")

# Initialize session state
if 'iframe_ip' not in st.session_state:
    st.session_state.iframe_ip = "Not detected yet"

# Get IP address server-side and store in variable
try:
    response = requests.get('https://api.ipify.org?format=json')
    ip_data = response.json()
    ip_address = ip_data['ip']
    print(f"Server IP: {ip_address}")
except Exception as e:
    ip_address = "Failed to detect"
    print(f"Error detecting IP: {e}")

# Display the server-detected IP
st.subheader("Your IP Address (detected server-side)")
st.write(ip_address)

# Create HTML/JS component to get client IP without the key parameter
def get_client_ip_component():
    html_code = """
    <div style="padding: 10px; background-color: #f0f2f6; border-radius: 5px;">
        <p style="font-weight: bold;">Your IP Address (client-side): <span id="ip-result">Detecting...</span></p>
    </div>
    
    <script>
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
    
    // Run when loaded
    getIP();
    </script>
    """
    
    st.components.v1.html(html_code, height=100)

# Show the IP component (client-side detection)
st.subheader("Client-side Detection")
get_client_ip_component()

# Create a form to manually capture iframe IP
st.subheader("Iframe IP Capture")

# Show the iframe directly
st.markdown('<iframe src="https://api.ipify.org" width="100%" height="50" id="ip-frame"></iframe>', unsafe_allow_html=True)

# Create a form for manual entry
with st.form("iframe_ip_form"):
    iframe_ip_input = st.text_input("Enter the IP address shown in the iframe above:", 
                                   value=st.session_state.get('iframe_ip', ''))
    
    submitted = st.form_submit_button("Save IP to variable")
    
    if submitted:
        st.session_state.iframe_ip = iframe_ip_input
        st.success(f"Successfully saved IP: {iframe_ip_input} to variable")

# Display the stored iframe IP
st.subheader("Stored IP Variables")
st.write(f"Server-side IP variable: {ip_address}")
st.write(f"Iframe IP variable: {st.session_state.get('iframe_ip', 'Not set yet')}")

# Add a refresh button outside the form
if st.button("Refresh Page"):
    st.experimental_rerun()

# Print to console log (server-side)
print(f"Page loaded at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Server IP: {ip_address}")
print(f"Iframe IP (from session state): {st.session_state.get('iframe_ip', 'Not detected yet')}")
