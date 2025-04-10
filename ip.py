import streamlit as st
from streamlit.components.v1 import html

st.title("User IP Address")

# Create a simple component with JavaScript that will fetch the IP
ip_component = html("""
<div id="ip-display">Loading IP...</div>
<div id="ip-value" style="display:none;"></div>

<script>
async function getUserIP() {
    try {
        const response = await fetch('https://api.ipify.org?format=json');
        const data = await response.json();
        const userIP = data.ip;
        
        // Display IP
        document.getElementById('ip-display').innerText = 'Your IP: ' + userIP;
        
        // Store IP in a hidden div for extraction
        document.getElementById('ip-value').innerText = userIP;
        
        // Force rerun of Streamlit app
        if (window.parent && window.parent.document) {
            const buttons = window.parent.document.querySelectorAll('button');
            for (const button of buttons) {
                if (button.innerText === 'Rerun') {
                    button.click();
                    break;
                }
            }
        }
    } catch (error) {
        document.getElementById('ip-display').innerText = 'Error: ' + error.message;
    }
}

getUserIP();
</script>
""", height=80)

# Add a button to manually trigger getting IP value
if st.button("Get IP to Python"):
    st.rerun()

# Create a text input for manual entry
manual_ip = st.text_input("Or copy your IP here manually from the display above:")

if manual_ip:
    st.write(f"Using IP: {manual_ip}")
    # Now you can use manual_ip as a Python variable
    # For example, to get ASN info:
    import requests
    try:
        asn_response = requests.get(f"https://ipapi.co/{manual_ip}/json/")
        asn_data = asn_response.json()
        st.write(f"ASN: {asn_data.get('asn', 'Not available')}")
        st.write(f"Organization: {asn_data.get('org', 'Not available')}")
        st.write(f"Country: {asn_data.get('country_name', 'Not available')}")
    except Exception as e:
        st.error(f"Error getting ASN info: {e}")
