import streamlit as st
from datetime import datetime
import requests

st.set_page_config(page_title="IP Address Detector", page_icon="🔍")

st.title("IP Address Detector")

# Get IP address server-side and store in variable
try:
    response = requests.get('https://api.ipify.org?format=json')
    ip_data = response.json()
    ip_address = ip_data['ip']
   
    print(f"IP 1: {ip_address}")
except Exception as e:
    ip_address = "Failed to detect"
    print(f"Error detecting IP: {e}")

# Display the server-detected IP
st.subheader("Your IP Address (detected server-side)")
st.write(ip_address)

# Method 1: Client-side extraction from iframe using JavaScript
st.subheader("IP from iframe (JavaScript method)")
iframe_extraction_code = """
<div style="padding: 10px; background-color: #f0f2f6; border-radius: 5px;">
    <p style="font-weight: bold;">IP from iframe: <span id="iframe-ip">Loading...</span></p>
    <iframe id="ip-iframe" src="https://api.ipify.org" width="100%" height="30" style="border:none;"></iframe>
</div>

<script>
// Function to extract IP from iframe
function extractIpFromIframe() {
    const iframe = document.getElementById('ip-iframe');
    
    // Wait for iframe to load
    iframe.onload = function() {
        try {
            // Try to get the content directly (this will work because api.ipify.org sets CORS headers)
            const iframeContent = iframe.contentDocument || iframe.contentWindow.document;
            const ipText = iframeContent.body.innerText.trim();
            
            // Display the extracted IP
            document.getElementById('iframe-ip').innerText = ipText;
            
            // Store in a JavaScript variable
            window.iframeIpAddress = ipText;
            
            // Log to console
            console.log('Iframe IP:', ipText);
        } catch (error) {
            document.getElementById('iframe-ip').innerText = 'Error accessing iframe content';
            console.error('Error:', error);
        }
    };
}

// Run the extraction function
extractIpFromIframe();
</script>
"""
st.components.v1.html(iframe_extraction_code, height=100)

# Method 2: Create a custom component that sends data back to Streamlit
st.subheader("IP from iframe with callback to Python")
callback_component = """
<div style="padding: 10px; background-color: #f0f2f6; border-radius: 5px;">
    <p style="font-weight: bold;">IP from iframe (with Python callback): <span id="callback-result">Preparing...</span></p>
    <iframe id="ip-iframe-callback" src="https://api.ipify.org" width="100%" height="30" style="display:none;"></iframe>
</div>

<script>
// Function to extract IP and save it to session state through Streamlit's component API
function extractAndCallback() {
    const iframe = document.getElementById('ip-iframe-callback');
    
    iframe.onload = function() {
        try {
            // Extract the IP from iframe
            const iframeContent = iframe.contentDocument || iframe.contentWindow.document;
            const ipText = iframeContent.body.innerText.trim();
            
            // Display the result
            document.getElementById('callback-result').innerText = ipText + " (saved to session state)";
            
            // Send the IP to Streamlit's session_state
            // This requires the streamlit-component-lib which is automatically available
            if (window.Streamlit) {
                window.Streamlit.setComponentValue(ipText);
            }
            
            console.log('Iframe IP for callback:', ipText);
        } catch (error) {
            document.getElementById('callback-result').innerText = 'Error accessing iframe';
            console.error('Error in callback method:', error);
        }
    };
}

// Run callback extraction
extractAndCallback();
</script>
"""

# Create a custom component and get the return value
iframe_ip = st.components.v1.html(callback_component, height=100, key="iframe_extractor")

# Store the iframe IP in session state if it's returned
if iframe_ip:
    st.session_state.iframe_ip = iframe_ip
    st.write(f"✅ Successfully stored iframe IP in session_state: {iframe_ip}")
    
    # Now you can use this IP variable in your Python code
    # For example, let's uppercase it to show we can manipulate it
    st.write(f"Uppercase version: {iframe_ip.upper()}")
elif 'iframe_ip' in st.session_state:
    st.write(f"Using previously stored iframe IP: {st.session_state.iframe_ip}")
else:
    st.write("Waiting for iframe IP to be extracted...")

# Add a refresh button
if st.button("Refresh"):
    st.experimental_rerun()

# Print to console log (server-side)
print(f"Page loaded at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Stored IP: {ip_address}")
if 'iframe_ip' in st.session_state:
    print(f"Iframe IP in session state: {st.session_state.iframe_ip}")
