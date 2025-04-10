import streamlit as st
from streamlit.components.v1 import html

st.title("User IP Address Finder")

# Initialize session state to store IP address
if 'ip_address' not in st.session_state:
    st.session_state.ip_address = None
    
if 'clicked' not in st.session_state:
    st.session_state.clicked = False

# Function to handle click
def on_button_click():
    st.session_state.clicked = True

# Define the JavaScript component
ip_component = """
<div>
    <p id="ip-display">Detecting your IP address...</p>
    <input type="hidden" id="ip-value">
    <script>
        // Function to get IP address
        async function getUserIP() {
            try {
                const response = await fetch('https://api.ipify.org?format=json');
                const data = await response.json();
                document.getElementById('ip-display').innerHTML = 
                    '<strong>Your IP address is:</strong> ' + data.ip;
                
                // Store IP in a hidden input field
                document.getElementById('ip-value').value = data.ip;
            } catch (error) {
                document.getElementById('ip-display').innerHTML = 
                    'Error detecting IP: ' + error.message;
            }
        }
        
        // Initialize
        getUserIP();
    </script>
</div>
"""

# Display the HTML/JavaScript component
html(ip_component, height=100)

# Create a simple form to submit the IP
with st.form("ip_form"):
    # You can't directly access the JS variables, so ask user to confirm
    submit_button = st.form_submit_button("Store IP Address", on_click=on_button_click)
    
# Handle the form submission
if st.session_state.clicked:

# After form submission, prompt user to enter IP manually
if st.session_state.clicked:
    user_ip = st.text_input("Please enter the IP address shown above:",
                          help="Copy the IP address that was detected and paste it here")
    
    if st.button("Confirm IP Address"):
        if user_ip:
            st.session_state.ip_address = user_ip
            st.success(f"IP Address stored: {user_ip}")
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
1. The JavaScript code gets your IP from ipify.org and displays it in the browser
2. When you click "Store IP Address", you'll be prompted to enter the IP address manually
3. The IP is stored in Streamlit's session_state
4. Now you can use this IP in your Python code!
""")

# Notes about the implementation
st.info("""
Due to the way Streamlit works with JavaScript, we can't directly pass variables from
JavaScript to Python. This is why you need to manually copy the displayed IP.

For a more advanced solution, you would need to create a custom Streamlit component
or use an alternative approach like setting up a small API endpoint.
""")
