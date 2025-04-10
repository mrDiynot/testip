import streamlit as st
import requests
import time

# Initialize session state for tracking progress
if 'ip_fetched' not in st.session_state:
    st.session_state.ip_fetched = False

st.title("IP Address Information")

# Function to get ASN info once we have the IP
def get_asn_info(ip):
    try:
        asn_response = requests.get(f"https://ipapi.co/{ip}/json/")
        asn_data = asn_response.json()
        
        st.write(f"Your IP: {ip}")
        st.write(f"ASN: {asn_data.get('asn', 'Not available')}")
        st.write(f"Organization: {asn_data.get('org', 'Not available')}")
        st.write(f"Country: {asn_data.get('country_name', 'Not available')}")
        st.write(f"City: {asn_data.get('city', 'Not available')}")
    except Exception as e:
        st.error(f"Error getting ASN info: {e}")

# Check if IP is in query params
if "ip" in st.query_params:
    user_ip = st.query_params["ip"]
    st.session_state.ip_fetched = True
    st.session_state.user_ip = user_ip
    get_asn_info(user_ip)
    
# If no IP in parameters but we have it in session state
elif "user_ip" in st.session_state and st.session_state.ip_fetched:
    get_asn_info(st.session_state.user_ip)
    
# No IP yet, use JavaScript to get it
else:
    st.write("Fetching your IP address...")
    
    # Create component with JavaScript that gets IP and sets it as a query parameter
    js_code = """
    <div id="ip-status">Loading your IP address...</div>
    
    <script>
    async function getUserIP() {
        try {
            const ipDisplay = document.getElementById('ip-status');
            ipDisplay.innerText = "Connecting to IP service...";
            
            const response = await fetch('https://api.ipify.org?format=json');
            const data = await response.json();
            const userIP = data.ip;
            
            ipDisplay.innerText = "Found IP: " + userIP + " - Loading ASN data...";
            
            // Add a slight delay to ensure the message is visible
            setTimeout(() => {
                // Redirect with IP as query parameter
                window.location.href = window.location.pathname + '?ip=' + userIP;
            }, 1000);
        } catch (error) {
            document.getElementById('ip-status').innerText = 'Error getting IP: ' + error.message;
        }
    }
    
    // Run when the component is loaded
    getUserIP();
    </script>
    """
    st.subheader("Client-side Detection{user_ip}")
    # Display the JavaScript component
    st.components.v1.html(js_code, height=100)
    
    
