import streamlit as st
import requests

st.title("IP Address Finder")

# Initialize session state
if 'ip_address' not in st.session_state:
    st.session_state.ip_address = None

# Display current IP if we have it
if st.session_state.ip_address:
    st.success(f"Your IP address is: {st.session_state.ip_address}")
else:
    st.info("Click the button below to fetch your IP address")

# Button to fetch IP
if st.button("Get My IP Address"):
    try:
        # Make a request to the IP API service
        response = requests.get('https://api.ipify.org?format=json')
        data = response.json()
        
        # Store the IP in session state
        st.session_state.ip_address = data['ip']
        
        # Display the result
        st.success(f"Your IP address is: {st.session_state.ip_address}")
        
        # Show how to use this in Python code
        st.subheader("Using the IP in Python code:")
        st.code(f"""
# Now you can use this IP address in your Python code
ip_address = "{st.session_state.ip_address}"

# Example of how you might use it
print(f"User IP: {ip_address}")

# You could save it to a database
# db.save_user_ip(ip_address)

# Or use it for geolocation
# location = get_location(ip_address)
        """)
        
    except Exception as e:
        st.error(f"Error fetching IP: {e}")

# If you need to access query parameters, use st.query_params instead of st.experimental_get_query_params
# For example:
if 'ip' in st.query_params:
    st.write(f"IP from query parameters: {st.query_params['ip']}")
