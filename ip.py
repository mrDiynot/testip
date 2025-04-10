import streamlit as st
from datetime import datetime
import requests

st.set_page_config(page_title="IP Address Detector", page_icon="🔍")

st.title("IP Address Detector")

# Initialize a session state variable to store the IP
if 'iframe_ip' not in st.session_state:
    st.session_state.iframe_ip = "Not detected yet"

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

# Create a function to get client IP and store it in session state
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
            
            // Store IP in sessionStorage for Streamlit to access
            sessionStorage.setItem('detected_ip', data.ip);
            
            // Log to console
            console.log('Client IP:', data.ip);
            
            // Send to Streamlit via streamlit:component:message
            const message = {ip: data.ip};
            window.parent.postMessage({
                type: "streamlit:setComponentValue",
                value: message
            }, "*");
        } catch (error) {
            document.getElementById('ip-result').innerHTML = 'Error: ' + error;
        }
    }
    
    // Run when loaded
    getIP();
    </script>
    """
    
    # Use the component with a callback to capture the IP
    component_value = st.components.v1.html(html_code, height=100, key="ip_component")
    
    # If we got a value back, store it
    if component_value:
        if 'ip' in component_value:
            st.session_state.iframe_ip = component_value['ip']
            print(f"IP from component stored: {st.session_state.iframe_ip}")

# Show the IP component (client-side detection)
st.subheader("Client-side Detection")
get_client_ip_component()

# Display the stored IP from iframe/component
st.subheader("Stored IP Address (from client-side)")
st.write(st.session_state.iframe_ip)

# Add a section to show we can use the variable
st.subheader("Using the stored IP variable")
if st.session_state.iframe_ip != "Not detected yet":
    st.success(f"Successfully captured IP: {st.session_state.iframe_ip}")
    
    # Example of using the IP
    st.write(f"You can now use this IP address ({st.session_state.iframe_ip}) in your application logic!")
else:
    st.warning("Waiting for IP detection to complete... Try refreshing the page.")

# Add a refresh button
if st.button("Refresh"):
    st.experimental_rerun()

# Print to console log (server-side)
print(f"Page loaded at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Stored IP: {ip_address}")
print(f"Iframe IP: {st.session_state.iframe_ip}")
