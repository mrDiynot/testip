import streamlit as st
from datetime import datetime

st.set_page_config(page_title="IP Address Detector", page_icon="🔍")

st.title("IP Address Detector")

# Create HTML/JS component to get client IP without the key parameter
def get_client_ip_component():
    html_code = """
    <div style="padding: 10px; background-color: #f0f2f6; border-radius: 5px;">
        <p style="font-weight: bold;">Your IP Address: <span id="ip-result">Detecting...</span></p>
    </div>
    
    <script>
    async function getIP() {
        try {
            const response = await fetch('https://api.ipify.org?format=json');
            const data = await response.json();
            
            // Display the IP
            document.getElementById('ip-result').innerHTML = data.ip;
            
            // Log to console
            console.log('Client IP:', data.ip);
        } catch (error) {
            document.getElementById('ip-result').innerHTML = 'Error: ' + error;
        }
    }
    
    // Run when loaded
    getIP();
    </script>
    """
    # Removed the key parameter that was causing the error
    st.components.v1.html(html_code, height=100)

# Main content
st.write("This app uses JavaScript to detect your real IP address directly from your browser.")
st.write("This works even when deployed to services like PythonAnywhere.")

# Show the IP component
get_client_ip_component()

# Alternative method using iframe to ipify.org
st.subheader("Alternative Method")
st.markdown('<iframe src="https://api.ipify.org" width="100%" height="50"></iframe>', unsafe_allow_html=True)

# Add a refresh button
if st.button("Refresh"):
    st.experimental_rerun()

# Information section
st.markdown("---")
st.subheader("How This Works")
st.markdown("""
This app uses JavaScript running in your browser to contact ipify.org directly.
This means:

1. The IP shown is your actual public IP address
2. This works even when deployed to hosting services
3. The result is more reliable than server-side detection

When deployed, server-side IP detection often shows the server's IP address or an internal proxy IP,
not your actual public IP. This client-side approach solves that problem.
""")

# Log timestamp
st.caption(f"Last refresh: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Print to console log (server-side)
print(f"Page loaded at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("Note: The user's IP is visible in the app but not captured on the server.")