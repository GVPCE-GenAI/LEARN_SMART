import re
import streamlit as st

class Validate():

    def __init__(self, username : str = None, password : str = None):
        self.username = username
        self.password = password
        return None
    
    # Function to validate email
    def validate_email(self) -> bool:
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, self.username)


    # Function to validate password
    def validate_password(self) -> bool:
        if len(self.password) < 8:
            return False
        if not any(char.isupper() for char in self.password):
            return False
        if not any(char.islower() for char in self.password):
            return False
        if not any(char in "!'@#$%^&*()-_=+\\|{}[\\]:;\"\'<>,.?/" for char in self.password):
            return False
        if not any(char.isdigit() for char in self.password):
            return False
        return True


    # Function to call both email and password validation functions
    def validate_details(self) -> bool:
        if not self.validate_email():
            st.warning('Username must be an email address only!!', icon="⚠️")
            return False
        if not self.validate_password():
            st.warning("Password is invalid!!", icon="⚠️")
            return False
        return True