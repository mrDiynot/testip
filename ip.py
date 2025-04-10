import streamlit as st
from streamlit.components.v1 import html

# Initialize session state for the IP address if it doesn't exist
if 'ip_address' not in st.session_state:
    st.session_state.ip_address = None

# Create a callback that Streamlit will use to update the session state
def update_ip(ip):
    st.session_state.ip_address = ip

# JavaScript code to fetch the IP and display it
js_code = """
<div id="ip-container">Loading IP address...</div>

<script>
async function getIP() {
    try {
        const response = await fetch('https://api.ipify.org?format=json');
        const data = await response.json();
        const ip = data.ip;
        
        // Display the IP address
        document.getElementById('ip-container').innerText = 'Fetched IP address: ' + ip;
        
        // Pass the value back to Python - using sendBackData which is available in Streamlit components
        window.parent.Streamlit.setComponentValue(ip);
    } catch (error) {
        document.getElementById('ip-container').innerText = 'Error fetching IP: ' + error.message;
    }
}

// Call the function when the component loads
getIP();
</script>
"""

# Display the component and get the return value
ip_address = html(js_code, height=100, key="ip_getter")

# Update session state if we got a new IP
if ip_address:
    st.session_state.ip_address = ip_address

# Display the IP from session state
st.header("IP Address Information")
if st.session_state.ip_address:
    st.write(f"Your IP address is: {st.session_state.ip_address}")
    
    # You can now use this IP in your Python code
    st.write("Now we can use this IP address in Python code!")
else:
    st.write("Waiting for IP address...")
