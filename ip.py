import streamlit as st
from streamlit.components.v1 import html
import json

# Initialize session state for the IP address if it doesn't exist
if 'ip_address' not in st.session_state:
    st.session_state.ip_address = None

# JavaScript function to get IP and pass it back to Python
js_code = """
<script>
async function getIP() {
    try {
        const response = await fetch('https://api.ipify.org?format=json');
        const data = await response.json();
        
        // Send the IP back to Python through Streamlit's component communication
        const ip = data.ip;
        window.parent.postMessage({
            type: 'streamlit:setComponentValue',
            value: ip
        }, '*');
        
        document.getElementById('ip-container').innerText = 'Fetched IP address: ' + ip;
    } catch (error) {
        document.getElementById('ip-container').innerText = 'Error fetching IP: ' + error.message;
    }
}

// Call the function when the component loads
getIP();
</script>
<div id="ip-container">Loading IP address...</div>
"""

# Custom component that can return values to Python
def ip_component():
    component_value = html(js_code, height=100, key="ip_getter")
    return component_value

# Get the IP from the component
ip = ip_component()

# Update session state if we got a new IP
if ip is not None and ip != "":
    st.session_state.ip_address = ip

# Display the IP from session state
if st.session_state.ip_address:
    st.header("IP Address Information")
    st.write(f"Your IP address is: {st.session_state.ip_address}")
    
    # You can now use this IP address in your Python code
    st.write("Now we can use this IP address in Python code!")
    
    # Example of how you might use the IP (just for demonstration)
    st.code(f"""
    # Example Python code using the IP address
    ip = "{st.session_state.ip_address}"
    
    # You could now use this IP for geolocation, logging, etc.
    location_info = get_location_from_ip(ip)  # This is just a placeholder function
    log_user_visit(ip)                        # This is just a placeholder function
    """)
else:
    st.warning("Waiting for IP address to be retrieved...")
