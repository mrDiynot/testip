import streamlit as st

# Create a custom component using HTML and JavaScript
html_code = """
<div id="ipDisplay">Loading IP address...</div>

<script>
    async function getUserIP() {
        try {
            const response = await fetch('https://api.ipify.org?format=json');
            const data = await response.json();
            document.getElementById('ipDisplay').innerHTML = 'Your IP: ' + data.ip;
            
            // Optional: Send the IP to Streamlit using session state
            if (window.parent.window.streamlit) {
                window.parent.window.streamlit.setComponentValue(data.ip);
            }
        } catch (error) {
            document.getElementById('ipDisplay').innerHTML = 'Error getting IP';
            console.error(error);
        }
    }
    
    getUserIP();
</script>
"""

# Display the component
from streamlit.components.v1 import html
ip_component = html(html_code, height=50)

# If you're using callback to get the IP in Python
if ip_component:
    st.write(f"Captured IP in Python: {ip_component}")
