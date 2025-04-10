import streamlit as st
from streamlit.components.v1 import html
import json

st.title("User IP Address Finder")

# Initialize session state to store IP address
if 'ip_address' not in st.session_state:
    st.session_state.ip_address = None

# Define the JavaScript component with callback functionality
ip_component = """
<div>
    <p id="ip-display">Detecting your IP address...</p>
    <script>
        // Function to get IP address
        async function getUserIP() {
            try {
                const response = await fetch('https://api.ipify.org?format=json');
                const data = await response.json();
                document.getElementById('ip-display').innerHTML = 
                    '<strong>Your IP address is:</strong> ' + data.ip;
                
                // Store IP in a hidden field for easy access
                window.userIPAddress = data.ip;
            } catch (error) {
                document.getElementById('ip-display').innerHTML = 
                    'Error detecting IP: ' + error.message;
            }
        }
        
        // Function to send IP back to Streamlit
        function sendToStreamlit() {
            if (window.userIPAddress) {
                // Use Streamlit's setComponentValue to communicate back to Python
                window.parent.postMessage({
                    type: "streamlit:setComponentValue",
                    value: window.userIPAddress
                }, "*");
            }
        }
        
        // Initialize
        getUserIP();
        
        // Add event listener for messages from Streamlit
        window.addEventListener("message", function(event) {
            // Check if Streamlit is asking for the value
            if (event.data.type === "streamlit:render") {
                // Wait a bit to make sure IP is fetched
                setTimeout(sendToStreamlit, 1000);
            }
        });
    </script>
</div>
"""

# Create a custom component that can return values
def get_ip_component():
    component_value = html(ip_component, height=100, key="ip_component")
    return component_value

# Display the component and get its value
user_ip = get_ip_component()

# Button to store IP
if st.button("Store IP Address"):
    if user_ip:
        st.session_state.ip_address = user_ip
        st.success(f"IP Address stored: {user_ip}")
    else:
        st.warning("No IP address detected yet. Please wait a moment.")

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
1. The JavaScript code gets your IP from ipify.org
2. When you click "Store IP Address", it sends the IP back to Python
3. The IP is stored in Streamlit's session_state
4. Now you can use this IP in your Python code!
""")

# Notes about the implementation
st.info("""
This solution uses Streamlit's component communication system to pass 
the client-side IP address back to the server-side Python code.
""")
