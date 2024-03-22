import streamlit as st

# Initial page configurations
st.set_page_config(page_title="Sign Up/Login", initial_sidebar_state="collapsed")
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


st.page_link("pages/1_Login.py", label="Login to your existing account!")
st.page_link("pages/2_Signup.py", label="Sign up for a new account!")