import streamlit as st
from streamlit.components.v1 import html
import requests

st.title("User IP Address Finder")

# Initialize session state to store IP address
if 'ip_address' not in st.session_state:
    st.session_state.ip_address = None

# Define the JavaScript component
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

# Add a method to get IP address server-side
def get_server_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        data = response.json()
        return data['ip']
    except Exception as e:
        return f"Error: {str(e)}"

# Button to store IP server-side
if st.button("Store My IP Address (Server Method)"):
    server_ip = get_server_ip()
    st.session_state.ip_address = server_ip
    st.success(f"IP Address stored: {server_ip}")
    st.info("Note: This is the server's IP address, not necessarily yours.")

# Alternative manual entry option
st.markdown("---")
st.write("### Or enter your IP manually:")
manual_ip = st.text_input("Enter the IP address shown above:")
if st.button("Store This IP"):
    if manual_ip:
        st.session_state.ip_address = manual_ip
        st.success(f"IP Address stored: {manual_ip}")
    else:
        st.warning("Please enter an IP address")

# Display the stored IP
if st.session_state.ip_address:
    st.write("### Stored IP Address:")
    st.write(st.session_state.ip_address)
    
    # Example of using the stored IP in your Python code
    st.write("### Example Python operations with the IP:")
    st.code(f"""
# Now you can use this IP in Python code:
ip = "{st.session_state.ip_address}"
ip_parts = ip.split('.')
print(f"First octet: {ip_parts[0]}")
    """)

st.markdown("---")
st.write("""
### How this works:
1. The JavaScript code displays your IP from ipify.org in the browser
2. You have two options to store the IP:
   - Server Method: Gets the server's IP (may not be your actual IP)
   - Manual Entry: Copy the displayed IP and enter it manually
3. The IP is stored in Streamlit's session_state
4. Now you can use this IP in your Python code!
""")

# Notes about the implementation
st.info("""
Due to how Streamlit works, we can't directly pass values from JavaScript to Python.
The "Server Method" button will get the IP of the server running Streamlit, which 
might be different from your actual IP (especially in cloud deployments).

For most accurate results, use the manual entry method.
""")
