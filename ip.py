import streamlit as st

# Create a session state variable to store the IP
if 'user_ip' not in st.session_state:
    st.session_state.user_ip = None

st.title("User IP Address Finder")

# Modified JavaScript component with callback
ip_component = """
<div>
    <p id="ip-display">Detecting your IP address...</p>
    <script>
        async function getUserIP() {
            try {
                const response = await fetch('https://api.ipify.org?format=json');
                const data = await response.json();
                
                // Display the IP
                document.getElementById('ip-display').innerHTML = 
                    '<strong>Your IP address is:</strong> ' + data.ip;
                
                // Send the IP to Python via Streamlit's communication API
                const ip = data.ip;
                if (window.parent && window.parent.Streamlit) {
                    window.parent.Streamlit.setComponentValue(ip);
                }
            } catch (error) {
                document.getElementById('ip-display').innerHTML = 
                    'Error detecting IP: ' + error.message;
            }
        }
        getUserIP();
    </script>
</div>
"""

# Display the component and get the return value
result = st.components.v1.html(ip_component, height=100, key="ip_component")

# If we got an IP back from the component, store it in session state
if result:
    st.session_state.user_ip = result

# Display the IP in Python if available
if st.session_state.user_ip:
    st.write(f"Python has received the IP: {st.session_state.user_ip}")
else:
    st.write("Waiting to receive IP in Python...")
