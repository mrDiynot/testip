import streamlit as st
from streamlit.components.v1 import components

# Create a custom component to get the user's IP
def get_user_ip():
    # Define the component
    component_code = """
    <div>
      <p id="ip-display">Loading IP address...</p>
      <script>
        async function getUserIP() {
          try {
            const response = await fetch('https://api.ipify.org?format=json');
            const data = await response.json();
            document.getElementById('ip-display').innerHTML = 'Your IP: ' + data.ip;
            
            // Send data back to Streamlit
            window.parent.Streamlit.setComponentValue(data.ip);
          } catch (error) {
            document.getElementById('ip-display').innerHTML = 'Error fetching IP';
            console.error('Error:', error);
          }
        }
        
        // Run immediately
        getUserIP();
      </script>
    </div>
    """
    
    # Create the component
    component_func = components.declare_component(
        "get_ip_component",
        render_func=lambda: components.html(component_code, height=50)
    )
    
    # Call the component function and return the result
    return component_func()

# Use the component in your app
st.title("User IP Address Demo")

# Get user IP
user_ip = get_user_ip()

# Display the returned IP (will be None initially, then update when data is received)
if user_ip:
    st.write(f"Your IP address is: {user_ip}")
    # Now you can use user_ip variable in your Python code
    st.write(f"First octet of your IP: {user_ip.split('.')[0]}")
