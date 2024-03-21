import streamlit as st

html_code = None

if 'is_form_submitted' not in st.session_state:
    st.session_state.is_form_submitted = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'password' not in st.session_state:
    st.session_state.password = ""

if st.session_state.is_form_submitted == False:
    with open("../app/html_files/login.html", 'r') as file:
        html_code = file.read() 

    st.components.v1.html(html_code, width=600, height=450)

username = st.session_state.username
password = st.session_state.password

st.session_state.username = None
st.session_state.password = None

st.write("Username: ", username)
st.write("Password: ", password)