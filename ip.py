import streamlit as st
import requests
from urllib.parse import parse_qs

# Check for IP in query params or session state
query_params = st.experimental_get_query_params()
user_ip = None

if "ip" in query_params:
    user_ip = query_params["ip"][0]
    # Store in session state
    st.session_state.user_ip = user_ip
elif "user_ip" in st.session_state:
    user_ip = st.session_state.user_ip

# If we don't have the IP yet, show the JavaScript to get it
if not user_ip:
    st.title("Fetching your IP address...")
    
    html_code = """
    <script>
    async function getUserIP() {
        try {
            const response = await fetch('https://api.ipify.org?format=json');
            const data = await response.json();
            const userIP = data.ip;
            
            // Redirect to same page with IP as query param
            window.location.href = window.location.pathname + '?ip=' + userIP;
        } catch (error) {
            console.error('Error getting IP:', error);
        }
    }
    
    // Run immediately
    getUserIP();
    </script>
    """
    st.components.v1.html(html_code, height=0)
    st.stop()

# If we have the IP, show it and do something with it
st.title("User IP Information")
st.write(f"Your IP: {user_ip}")

# Use the IP to get ASN info
try:
    asn_response = requests.get(f"https://ipapi.co/{user_ip}/json/")
    asn_data = asn_response.json()
    
    st.write(f"ASN: {asn_data.get('asn', 'Not available')}")
    st.write(f"Organization: {asn_data.get('org', 'Not available')}")
    st.write(f"Country: {asn_data.get('country_name', 'Not available')}")
    st.write(f"City: {asn_data.get('city', 'Not available')}")
except Exception as e:
    st.error(f"Error getting ASN info: {e}")
