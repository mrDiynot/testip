import streamlit as st
import json
from streamlit.components.v1 import html

st.title("User IP Address Finder")

# Initialize session state to store IP address
if 'ip_address' not in st.session_state:
    st.session_state.ip_address = None

# Create a key for callback when DOM elements are ready
callback_key = "get_ip_callback"

# Define the JavaScript component with auto-save functionality
auto_ip_component = f"""
<div>
    <p id="ip-display">Detecting your IP address...</p>
    <p id="status">Waiting...</p>
    
    <script>
        // Function to get the IP address
        async function getUserIP() {{
            try {{
                const response = await fetch('https://api.ipify.org?format=json');
                const data = await response.json();
                document.getElementById('ip-display').innerHTML = 
                    '<strong>Your IP address is:</strong> ' + data.ip;
                
                // Send the IP to Streamlit via the URL query parameter trick
                document.getElementById('status').innerHTML = 'Sending to Python...';
                
                // Create a form and submit it to update the Streamlit session state
                const form = document.createElement('form');
                form.method = 'POST';
                form.action = '';
                
                const input = document.createElement('input');
                input.type = 'hidden';
                input.name = '{callback_key}';
                input.value = data.ip;
                
                form.appendChild(input);
                document.body.appendChild(form);
                form.submit();
                
                return data.ip;
            }} catch (error) {{
                document.getElementById('ip-display').innerHTML = 
                    'Error detecting IP: ' + error.message;
                return null;
            }}
        }}
        
        // Execute on page load
        getUserIP().then(ip => {{
            if (ip) {{
                document.getElementById('status').innerHTML = 
                    'IP detected and submitted to Python automatically.';
            }}
        }});
    </script>
</div>
"""

# Display the HTML/JavaScript component
html(auto_ip_component, height=150)

# Check if we received an IP from the JavaScript
if callback_key in st.experimental_get_query_params():
    ip_from_js = st.experimental_get_query_params()[callback_key][0]
    st.session_state.ip_address = ip_from_js

# Button to manually trigger storing IP (as fallback)
col1, col2 = st.columns([3, 1])
with col1:
    manual_ip = st.text_input("If auto-detection doesn't work, enter IP manually:", 
                             help="Copy the IP address shown above")
with col2:
    st.write("")
    st.write("")
    if st.button("Store IP"):
        if manual_ip:
            st.session_state.ip_address = manual_ip
            st.success(f"IP Address stored: {manual_ip}")
        else:
            st.warning("Please enter an IP address")

# Display the stored IP
if st.session_state.ip_address:
    st.write("### IP Address Stored in Python:")
    st.success(st.session_state.ip_address)
    
    # Example of using the stored IP in your Python code
    st.write("### Example Python operations with the IP:")
    st.code(f"""
# Now you can use this IP in Python code:
ip = "{st.session_state.ip_address}"
ip_parts = ip.split('.')
print(f"First octet: {ip_parts[0]}")
    """)
    
    # Add a button to demonstrate using the IP in actual Python code
    if st.button("Run Python Example"):
        ip = st.session_state.ip_address
        ip_parts = ip.split('.')
        st.write(f"First octet: {ip_parts[0]}")
        st.write(f"Second octet: {ip_parts[1]}")
        st.write(f"IP type: {'Private' if ip_parts[0] in ['10', '192', '172'] else 'Public'}")

st.markdown("---")
st.write("""
### How this works:
1. The JavaScript code gets your IP from ipify.org
2. It automatically submits the IP to Python using a form submission trick
3. The IP is stored in Streamlit's session_state
4. Now you can use this IP in your Python code!
""")

# Notes about the implementation
st.info("""
This solution uses a form submission technique to pass data from JavaScript to Python.
If auto-detection doesn't work, you can still use the manual entry option.
""")
