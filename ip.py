import streamlit as st
from streamlit.components.v1 import html

st.title("User IP Address Finder")

# Define the JavaScript component to get the user's IP
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

st.markdown("---")
st.write("""
### How this works:
1. The JavaScript code runs in your browser (client-side)
2. It makes a direct request to ipify.org from your browser
3. This returns YOUR IP address, not the server's IP

### Note:
The IP address is not sent to the Streamlit backend, so you can't 
use it in Python code without additional steps.
""")

# Show a note about server IP vs client IP
st.info("""
If you were to fetch the IP using Python's requests library like this:
```python
import requests
response = requests.get('https://api.ipify.org?format=json')
