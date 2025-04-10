import streamlit as st
from datetime import datetime
import requests
import json

st.set_page_config(page_title="IP Address Detector", page_icon="🔍")

st.title("IP Address Detector")

# Initialize session state variables
if 'client_ip' not in st.session_state:
    st.session_state.client_ip = "Not detected yet"
if 'form_submitted' not in st.session_state:
    st.session_state.form_submitted = False

# Get IP address server-side and store in variable
try:
    response = requests.get('https://api.ipify.org?format=json')
    ip_data = response.json()
    ip_address = ip_data['ip']
    print(f"Server IP: {ip_address}")
except Exception as e:
    ip_address = "Failed to detect"
    print(f"Error detecting IP: {e}")

# Display the server-detected IP
st.subheader("Your IP Address (detected server-side)")
st.write(ip_address)

# Create HTML component to get client IP and display it
def get_client_ip_component():
    html_code = """
    <div style="padding: 10px; background-color: #f0f2f6; border-radius: 5px; margin-bottom: 15px;">
        <p style="font-weight: bold;">Your IP Address (client-side): <span id="ip-result">Detecting...</span></p>
        <form id="ip-form" style="display:none;">
            <input type="hidden" id="ip-input" name="ip">
            <button type="submit" id="submit-btn" style="display:none;">Submit</button>
        </form>
    </div>
    
    <script>
    async function getIP() {
        try {
            const response = await fetch('https://api.ipify.org?format=json');
            const data = await response.json();
            
            // Display the IP
            document.getElementById('ip-result').innerHTML = data.ip;
            
            // Set the form input value
            document.getElementById('ip-input').value = data.ip;
            
            // Auto-submit the form
            setTimeout(() => {
                document.getElementById('ip-form').submit();
            }, 500);
            
            // Log to console
            console.log('Client IP detected:', data.ip);
        } catch (error) {
            document.getElementById('ip-result').innerHTML = 'Error: ' + error;
            console.error(error);
        }
    }
    
    // Run when loaded
    getIP();
    </script>
    """
    
    # Display the HTML component
    st.components.v1.html(html_code, height=80)

# Add a hidden form to capture the IP from the client-side component
with st.form(key='hidden_form', clear_on_submit=False):
    client_ip = st.text_input("IP Address", key="ip_input", label_visibility="collapsed")
    submit_button = st.form_submit_button("Update IP", type="primary")
    
    if submit_button or st.session_state.form_submitted:
        st.session_state.form_submitted = True
        if client_ip and client_ip != "":
            st.session_state.client_ip = client_ip
            print(f"Client IP captured: {client_ip}")

# Show the IP component for client-side detection
st.subheader("Client-side Detection")
get_client_ip_component()

# Show iframe method as an alternative
st.subheader("Alternative Method (iframe)")
col1, col2 = st.columns([3, 1])
with col1:
    st.write("Raw iframe response:")
    st.markdown('<iframe src="https://api.ipify.org" width="100%" height="50"></iframe>', unsafe_allow_html=True)
with col2:
    if st.button("Capture from iframe"):
        st.info("Note: Direct capture from iframe not possible due to security restrictions")

# Display the stored IP information
st.subheader("Stored IP Address Variable")
st.info(f"Current stored client IP: **{st.session_state.client_ip}**")

# Demonstrate using the variable
st.subheader("Using the Stored IP Variable")
if st.session_state.client_ip != "Not detected yet":
    st.success(f"IP address successfully captured and stored in session state")
    
    # Example of using the IP
    st.code(f"""
# Example usage in your Streamlit code:
client_ip = st.session_state.client_ip  # This equals: {st.session_state.client_ip}

# Now you can use this variable in your application
if client_ip.startswith("192.168"):
    st.write("You are on a local network")
else:
    st.write("You are connecting from the internet")
    """)
else:
    st.warning("Waiting for IP detection... Try manually submitting the form above or refreshing the page.")

# Add a refresh button
if st.button("Refresh Page"):
    st.session_state.form_submitted = False
    st.experimental_rerun()

# Print to console log (server-side)
print(f"Page loaded at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Server IP: {ip_address}")
print(f"Client IP: {st.session_state.client_ip}")
