import os
import time
import boto3
import dotenv
import streamlit as st
from validate import Validate


# Initial page configurations
st.set_page_config(page_title="Login", initial_sidebar_state="collapsed")
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

# Reset Username:
st.session_state['username'] = ''

# Sign in the user:
def sign_in_user(userpool_id, app_client_id, region_name, username, password) -> bool:
    try:
        client = boto3.client('cognito-idp', region_name = region_name)

        response = client.admin_initiate_auth(
            UserPoolId=userpool_id,
            ClientId=app_client_id,
            AuthFlow='ADMIN_USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password
            }
        )

        result = response['AuthenticationResult']
        return True
    except Exception as e:
        st.warning("Username or Password is incorrect!\nTry again")
        time.sleep(5)
        st.switch_page("pages/1_Login.py")

def main():
    # Loading the environment variables.
    dotenv.load_dotenv("/workspace/LEARN_SMART/Secrets/.env")
    
    APP_CLIENT_ID = os.getenv("APP_CLIENT_ID")
    USER_POOL_ID = os.getenv("USER_POOL_ID")
    USER_POOL_REGION = os.getenv("USER_POOL_REGION")

    # Login Form
    with st.form("Login Form"):
        # Input for username
        st.write("Username:")
        username = st.text_input(label="Username", placeholder="abc@example.com", label_visibility="collapsed")
        st.session_state['username'] = username

        # Input for password
        st.write("Password:")
        password = st.text_input(label="Password", placeholder="Abcde@#$123", label_visibility="collapsed", type="password")
        st.session_state['password'] = password

        # Submit button
        submitted = st.form_submit_button("Submit")
        if submitted:
            validate_obj = Validate(username, password)
            if validate_obj.validate_details():                                               # If both username and password are valid:
                val = sign_in_user(USER_POOL_ID, APP_CLIENT_ID, USER_POOL_REGION, username, password)
                if val:
                    st.session_state['password'] = ''
                    st.switch_page("pages/4_Homepage.py")


if __name__ == "__main__":
    main()