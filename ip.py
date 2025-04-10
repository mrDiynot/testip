import streamlit as st
from streamlit.components.v1 import html

# JavaScript code to fetch the IP address
js_code = """
<script>
  async function getIP() {
    try {
      const response = await fetch('https://api.ipify.org?format=json');
      const data = await response.json();
      document.getElementById('ip-container').innerText = 'Your IP address is: ' + data.ip;
    } catch (error) {
      document.getElementById('ip-container').innerText = 'Error fetching IP: ' + error.message;
    }
  }
  
  // Call the function when the component loads
  getIP();
</script>
<div id="ip-container">Loading IP address...</div>
"""

# Display the component
st.header("IP Address Finder")
html(js_code, height=100)
