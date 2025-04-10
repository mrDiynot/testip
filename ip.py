import streamlit as st
from streamlit.components.v1 import html
import time

st.title("User IP Address Finder")

# Create a place to store the IP
if 'user_ip' not in st.session_state:
    st.session_state.user_ip = None

# Modified JavaScript to redirect with query parameter
ip_component = """
<div>
    <p id="ip-display">Detecting your IP address...</p>
    <script>
        async function getUserIP() {
            try {
                const response = await fetch('https://api.ipify.org?format=json');
                const data = await response.json();
                document.getElementById('ip-display').innerHTML = 
                    '<strong>Your IP address is:</strong> ' + data.ip;
                
                // Add IP to URL as query parameter and reload
                const url = new URL(window.location.href);
                url.searchParams.set('ip', data.ip);
                window.history.replaceState(null, '', url);
                
                // Force a Streamlit rerun
                setTimeout(() => {
                    window.parent.postMessage({
                        type: "streamlit:forceRerun"
                    }, "*");
                }, 500);
            } catch (error) {
                document.getElementById('ip-display').innerHTML = 
                    'Error detecting IP: ' + error.message;
            }
        }
        getUserIP();
    </script>
</div>
"""

# Display the HTML/JavaScript component
html(ip_component, height=100)

# Check for IP in query parameters using the current API
if 'ip' in st.query_params:
    st.session_state.user_ip = st.query_params['ip']

# Display the IP if we have it
if st.session_state.user_ip:
    st.success(f"Python has received the IP: {st.session_state.user_ip}")
    # Now you can use st.session_state.user_ip in your Python code
else:
    st.info("Waiting to receive IP in Python...")
