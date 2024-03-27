import os
import time
import boto3
import dotenv
import streamlit as st

# Initial page configurations
st.set_page_config(page_title="Verify Code", initial_sidebar_state="collapsed")
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

# Function to verify the code
def verify_code(client_id, region_name, username, code) -> bool:
    try:
        client = boto3.client('cognito-idp', region_name = region_name)
        response = client.confirm_sign_up(
            ClientId = client_id,
            Username = username,
            ConfirmationCode = code
        )
        st.write(response)
        return True
    except Exception as e:
        if e == "CodeMismatchException":
            st.warning("Error code is wrong!!")
        if e == "ExpiredCodeException":
            st.warning("Error code is expired!")
        if e == "LimitExceededException":
            st.warning("Too many wrong codes entered, wait for some time!")
        else:
            st.warning(f"Wrong code entered, try again in 5 seconds")
            time.sleep(5)
            st.switch_page("pages/3_Verify.py")

def main():
    # Loading the environment variables.
    dotenv.load_dotenv("/workspace/LEARN_SMART/Secrets/.env")

    APP_CLIENT_ID = os.getenv("APP_CLIENT_ID")
    USER_POOL_REGION = os.getenv("USER_POOL_REGION")

    st.markdown("""
    <h4>
        Enter the verification code sent to your given email
    </h4>
    """, 
    unsafe_allow_html=True)

    # Verify the code
    with st.form("Verify-code-form"):
        st.write("Verification Code:")
        code = st.text_input(label="Verification-code", placeholder="XXXXXX", label_visibility="collapsed", type="password")
        if st.form_submit_button("Verify"):
            username = st.session_state['username']
            val = verify_code(APP_CLIENT_ID, USER_POOL_REGION, username, code)
            if val:
                st.success("Successfully signed up!!")
                st.switch_page("pages/4_Homepage.py")


if __name__ == "__main__":
    main()