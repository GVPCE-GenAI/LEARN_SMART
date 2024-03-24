import os
import time
import boto3
import dotenv
import streamlit as st
from validate import Validate


# Initial page configurations
st.set_page_config(page_title="Sign Up", initial_sidebar_state="collapsed")
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


# Function to Sign_Up the user
def sign_up_user(clientID, region_name, username, password, email) -> bool:
    try:
        client = boto3.client('cognito-idp', region_name = region_name)
        response = client.sign_up(
            ClientId = clientID,
            Username = username,
            Password = password,
            UserAttributes = [
                {
                    'Name' : 'email',
                    'Value': email
                },
            ],
        )
        return True
    except Exception as e:
        if "UsernameExistsException" in str(e):
            st.warning("User already exists!!")
        st.warning("Couldn't complete process, Do it again...")
        time.sleep(5)
        st.switch_page("pages/2_Signup.py")
        return False
        


def main():
    # Loading the environment variables.
    dotenv.load_dotenv("/workspace/LEARN_SMART/Secrets/.env")
    
    APP_CLIENT_ID = os.getenv("APP_CLIENT_ID")
    USER_POOL_ID = os.getenv("USER_POOL_ID")
    USER_POOL_REGION = os.getenv("USER_POOL_REGION")

    client = boto3.client('cognito-idp', region_name='us-east-1')
    # Login Form
    with st.form("Sign-Up Form"):
        # Input for username
        st.write("Username: (must only be a valid email-address)")
        username = st.text_input(label="Username", placeholder="abc@example.com", label_visibility="collapsed")
        st.session_state['username'] = username

        # Input for password
        st.write("Password, must be:\n1. Minimum of 8 characters.\n2. Must have atleast 1 Uppercase Letter.\n3. Must have atleast 1 lowercase letter.\n4. Must have atleast 1 digit.\n5. Must have atleast 1 special character")
        password = st.text_input(label="Password", placeholder="Abcde@#$123", label_visibility="collapsed", type="password")

        # Submit button
        submitted = st.form_submit_button("Submit")
        if submitted:
            validate_obj = Validate(username, password)
            if validate_obj.validate_details():
                if sign_up_user(APP_CLIENT_ID, USER_POOL_REGION, username, password, username):
                    st.switch_page("pages/3_Verify.py")
                    


if __name__ == "__main__":
    main()