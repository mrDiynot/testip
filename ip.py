import streamlit as st
from streamlit.components.v1 import html

st.title("IP Address Getter")

# Create a container to display the result
result_container = st.empty()

# Initialize session state
if 'ip_address' not in st.session_state:
    st.session_state.ip_address = None

# Function to update the display when IP is found
def display_ip():
    if st.session_state.ip_address:
        result_container.success(f"Your IP address is: {st.session_state.ip_address}")
    else:
        result_container.info("Waiting for IP address...")

# Display initial state
display_ip()

# Create a button to trigger the IP fetch
if st.button("Get My IP Address"):
    # JavaScript with a direct Streamlit API call
    component = html("""
        <script>
        // Immediately invoke this function to fetch the IP
        (async () => {
            try {
                const response = await fetch('https://api.ipify.org?format=json');
                const data = await response.json();
                
                // Use Streamlit's event mechanism to rerun with the new data
                const ip = data.ip;
                
                // Store the IP in sessionStorage for persistence
                sessionStorage.setItem('userIpAddress', ip);
                
                // Force a rerun of the Streamlit app
                window.parent.document.querySelector('button[kind="primaryFormSubmit"]').click();
            } catch (error) {
                console.error('Error fetching IP:', error);
            }
        })();
        </script>
        <div id="ip-fetch-status">Fetching your IP address...</div>
    """, height=0)
    
    # This will run after the rerun is triggered by the JavaScript
    st.session_state.ip_address = "fetching..."

# Check for IP in sessionStorage on each load
get_ip_from_storage = html("""
    <script>
    // Check if we have the IP in sessionStorage
    const storedIp = sessionStorage.getItem('userIpAddress');
    if (storedIp) {
        // Create a custom event to send data to Python
        const event = new CustomEvent('streamlit:ip-found', { 
            detail: { ip: storedIp }
        });
        window.parent.document.dispatchEvent(event);
        
        // Also update any Streamlit forms to include this data
        const hiddenInput = document.createElement('input');
        hiddenInput.type = 'hidden';
        hiddenInput.name = 'ip_address';
        hiddenInput.value = storedIp;
        
        // Add to any forms that might be in the Streamlit app
        Array.from(window.parent.document.forms).forEach(form => {
            form.appendChild(hiddenInput.cloneNode(true));
        });
    }
    </script>
""", height=0)

# Detect IP from query parameters (will be present after the form submit)
query_params = st.experimental_get_query_params()
if 'ip_address' in query_params:
    st.session_state.ip_address = query_params['ip_address'][0]
    display_ip()

# Instructions for alternative method
st.markdown("---")
st.markdown("""
### Alternative Method:
If the button doesn't work properly, you can try a direct Python approach using a different service:
""")

if st.button("Get IP with Python"):
    import requests
    try:
        response = requests.get('https://api.ipify.org?format=json')
        data = response.json()
        st.session_state.ip_address = data['ip']
        display_ip()
    except Exception as e:
        st.error(f"Error fetching IP: {e}")
