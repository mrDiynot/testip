import streamlit as st
from streamlit_javascript import st_javascript

st.title("Get Client IP in Streamlit")

ip = st_javascript(
    """
    async () => {
        const res = await fetch("https://api.ipify.org?format=json");
        const data = await res.json();
        return data.ip;
    }
    """
)

if ip:
    st.success(f"Your IP is: {ip}")
else:
    st.info("Fetching your IP...")
