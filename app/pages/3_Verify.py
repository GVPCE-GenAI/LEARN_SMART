import streamlit as st
import dotenv
import os
import boto3

def verify_code(client_id, region_name, username, code) -> bool:
    try:
        st.write("I am here")
        client = boto3.client('cognito-idp', region_name = region_name)
        response = client.confirm_sign_up(
            ClientId = client_id,
            Username = username,
            ConfirmationCode = confirmation_code,
        )
        st.write(response)
        return True
    except Exception as e:
        if e == "CodeMismatchException":
            st.warning("Error code is wrong!!")
        if e == "ExpiredCodeException":
            st.warning("Error code is expired!")
        return False


# Loading the environment variables.
dotenv.load_dotenv("/workspace/LEARN_SMART/Secrets/.env")

APP_CLIENT_ID = os.getenv("APP_CLIENT_ID")
USER_POOL_ID = os.getenv("USER_POOL_ID")
USER_POOL_REGION = os.getenv("USER_POOL_REGION")
st.write(APP_CLIENT_ID)
# Verify the code
with st.form("Verify-code-form"):
    st.write("Verification Code:")
    code = st.text_input(label="Verification-code", placeholder="XXXXXX", label_visibility="collapsed")
    if st.form_submit_button("Verify"):
        # username = st.session_state['username']
        username = "mkpentapalli2k2@gmail.com"
        val = verify_code(APP_CLIENT_ID, USER_POOL_REGION, username, code)
        if val:
            st.success("Successfully signed up!!")
            st.page_link("pages/4_Homepage.py")