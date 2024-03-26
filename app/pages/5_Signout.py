import streamlit as st

# Initial page configurations
st.set_page_config(page_title="Homepage", layout="wide", initial_sidebar_state="collapsed")
st.markdown(
    """
    <style>
        [data-testid="collapsedControl"] {
            display : none
        }
    </style>
    """,
    unsafe_allow_html = True
)

st.title("You've been successfully signed out!!")

if st.button("Login again"):
    st.switch_page("pages/1_Login.py")

if st.button("Sign up for a new account:"):
    st.switch_page("pages/2_Signup.py")