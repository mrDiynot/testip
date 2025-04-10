import streamlit as st
from streamlit.components.v1 import html
import json

# Initialize session state for IP if not already set
if 'user_ip' not in st.session_state:
    st.session_state.user_ip = None

st.title("User IP Address Demo")

# JavaScript to get user IP and store in session state
ip_html = """
<div id="ip-display">Loading your IP address...</div>

<script>
async function getUserIP() {
    try {
        const response = await fetch('https://api.ipify.org?format=json');
        const data = await response.json();
        const userIP = data.ip;
        
        // Display IP in the component
        document.getElementById('ip-display').innerText = 'Your IP: ' + userIP;
        
        // Send IP to Streamlit backend using streamlit-component-lib
        const stringifiedData = JSON.stringify({ip: userIP});
        
        // Use window.parent.postMessage to send data back to Streamlit
        window.parent.postMessage({
            type: "streamlit:setComponentValue",
            value: stringifiedData
        }, "*");
    } catch (error) {
        document.getElementById('ip-display').innerText = 'Error getting IP';
        console.error(error);
    }
}

getUserIP();
</script>
"""

# Render the component and capture its return value
component_value = html(ip_html, height=50)

# If component returns a value, update session state
if component_value:
    try:
        # Parse the JSON string returned from the component
        data = json.loads(component_value)
        st.session_state.user_ip = data.get('ip')
    except:
        st.error("Could not parse IP data from component")

# Display and use the IP stored in session state
if st.session_state.user_ip:
    st.write(f"Your IP address is: {st.session_state.user_ip}")
    # Now you can use st.session_state.user_ip in your Python code
