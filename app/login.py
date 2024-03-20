# # import streamlit as st

# # def main():
# #     st.title("Login Page")
# #     st.write("Welcome to the login page!")

# #     signup_login_url = "https://learn-smart-gvpce.auth.us-east-1.amazoncognito.com/login?client_id=72011ciu7lf2an6ftbd6ori7ns&response_type=token&scope=email+openid+phone&redirect_uri=https%3A%2F%2F8501-gvpcegenai-learnsmart-z0dpk9nof0a.ws-us110.gitpod.io%2F"
# #     st.link_button(label = "Go to Login/Signup page", url = signup_login_url, help = "Redirect to Login/Signup page")
    

# # if __name__ == "__main__":
# #     main()


# import streamlit as st
# import boto3

# COGNITO_CLIENT_ID = "72011ciu7lf2an6ftbd6ori7ns"
# # REDIRECT_URI = "https://8501-gvpcegenai-learnsmart-z0dpk9nof0a.ws-us110.gitpod.io/callback"

# def main():
#     st.title("Login Page")
#     st.write("Login or Signup for a new account!")

#     email = None
#     authentication_code = None

#     def handle_login_click():

#         REDIRECT_URI = st.session_state.get("redirect_uri", "https://8501-gvpcegenai-learnsmart-z0dpk9nof0a.ws-us110.gitpod.io/callback")
#         COGNITO_URL = "https://learn-smart-gvpce.auth.us-east-1.amazoncognito.com/login?client_id=72011ciu7lf2an6ftbd6ori7ns&response_type=token&scope=email+openid+phone&redirect_uri=https%3A%2F%2F8501-gvpcegenai-learnsmart-z0dpk9nof0a.ws-us110.gitpod.io%2F"
#         st.link_button(label = "Login/Signup", url = COGNITO_URL, help = "Go to Login/Signup page")



#     if 'code' in st.query_params.keys():
#         print("HI")

#         auth_code = st.query_params['code'][0]

#         cognito_client = boto3.client('cognito-identityprovider')
#         token_response = cognito_client.authorization_code_grant(
#             ClientId=COGNITO_CLIENT_ID,
#             AuthorizationCode=auth_code,
#             RedirectUri=st.session_state.get('redirect_uri')
#         )

#         id_token = taken_response['AccessToken']
#         try:
#             response = cognito_client.decode_id_token(idToken = id_token)
#             email = response.get('email')
#             st.write(f"Welcome, {email}!")
#         except Exception as e:
#             print(f"Error validating ID token: {e}")
#             st.error("An error occurred during login. Please try again.")
#     else:
#         handle_login_click()
    

# if __name__ == "__main__":
#     main()
#     # def handle_login_click():

# import boto3
# client = boto3.client("cognito-idp")
# client.get_user{

# }
        

# import streamlit as st
# import boto3

# COGNITO_CLIENT_ID = "72011ciu7lf2an6ftbd6ori7ns"
# REDIRECT_URI = "https://8501-gvpcegenai-learnsmart-z0dpk9nof0a.ws-us110.gitpod.io/callback"
# COGNITO_URL = "https://learn-smart-gvpce.auth.us-east-1.amazoncognito.com/login?client_id=72011ciu7lf2an6ftbd6ori7ns&response_type=token&scope=email+openid+phone&redirect_uri=https%3A%2F%2F8501-gvpcegenai-learnsmart-z0dpk9nof0a.ws-us110.gitpod.io%2F"

# def main():
#     st.title("Login Page")
#     st.write("Login or Signup for a new account!")
#     # st.link_button(label = "Go to Login/Signup page", url = COGNITO_URL, help = "Redirect to Login/Signup page")
#     # st.write(st.experimental_get_query_params)

#     if 'code' in st.query_params.keys():
#         auth_code = st.experimental_get_query_params['code'][0]

#         try:
#             cognito_client = boto3.client('cognito-idp', region_name='us-east-1')
#             token_response = cognito_client.initiate_auth(
#                 ClientId=COGNITO_CLIENT_ID,
#                 AuthFlow='AUTHORIZATION_CODE',
#                 AuthParameters={
#                     'AUTHORIZATION_CODE': auth_code,
#                     'redirect_uri': REDIRECT_URI
#                 }
#             )

#             id_token = token_response['AuthenticationResult']['IdToken']
#             decoded_id_token = cognito_client.decode_id_token(IdToken=id_token)
#             email = decoded_id_token['email']

#             st.write(f"Welcome, {email}!")
#         except Exception as e:
#             st.error(f"An error occurred during login: {e}")
#     else:
#         # COGNITO_URL = f"https://learn-smart-gvpce.auth.us-east-1.amazoncognito.com/login?client_id={COGNITO_CLIENT_ID}&response_type=code&scope=email+openid+phone&redirect_uri={REDIRECT_URI}"
#         # st.markdown(f"<a href='{COGNITO_URL}'>Login/Signup</a>", unsafe_allow_html=True)
#         st.link_button(label = "Go to Login/Signup page", url = COGNITO_URL, help = "Redirect to Login/Signup page")

# if __name__ == "__main__":
#     main()


import boto3
import time
import streamlit as st

# accessToken = None
# emailAddress = None

# st.title("Login/Signup Page")

# cognito_url = "https://learn-smart-gvpce.auth.us-east-1.amazoncognito.com/login?client_id=72011ciu7lf2an6ftbd6ori7ns&response_type=token&scope=email+openid+phone&redirect_uri=https%3A%2F%2F8501-gvpcegenai-learnsmart-z0dpk9nof0a.ws-us110.gitpod.io%2F"
# st.link_button(label = "Login/Signup", url = cognito_url, help = "Go to Login/Signup page")

# # time.sleep(30)

# # accessToken = "eyJraWQiOiIxd3RnZ1NqcnBqTXl5dkM1WlF3WFh6TitrdUtjSjkxZFBJd1lRV3JUc3VrPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiI4Y2E4YjFjMS1kMmIxLTQzMmItOGQ0OS1iYTZhYTAxNjMyZDIiLCJ0b2tlbl91c2UiOiJhY2Nlc3MiLCJzY29wZSI6InBob25lIG9wZW5pZCBlbWFpbCIsImF1dGhfdGltZSI6MTcxMDkzMjQyMiwiaXNzIjoiaHR0cHM6XC9cL2NvZ25pdG8taWRwLnVzLWVhc3QtMS5hbWF6b25hd3MuY29tXC91cy1lYXN0LTFfcG45ZkhMaWYyIiwiZXhwIjoxNzEwOTM2MDIyLCJpYXQiOjE3MTA5MzI0MjIsInZlcnNpb24iOjIsImp0aSI6IjRhNTNmNDFlLTJlNzItNDRmNS1iMjllLTIxZTMyOTFiZWMxZSIsImNsaWVudF9pZCI6IjcyMDExY2l1N2xmMmFuNmZ0YmQ2b3JpN25zIiwidXNlcm5hbWUiOiI4Y2E4YjFjMS1kMmIxLTQzMmItOGQ0OS1iYTZhYTAxNjMyZDIifQ.DYp4gorN7KpZcgE2yWSk03MtwirCQGVADUWFWcs7mN3vqN1n6MbaP9rctxTk6S7ymr72Eq1d3kS5FHwSzcqNUwYc9dR6lDzZbgHkzaKwv5sOX4FFEO90tTWApcvX5_c-YLo74LE6MAcQb67EdFEg3SUReqXpq9EXKy5ePrKVU9srA4gn4dBYY8RJbJrEs7J6Jtl2iUvwSgfk9JukxAGwhSnmRLMzZf7xukk5Ht-OWgZvWs0QQ5epIFLJMHsnRIAbAsBmCD5hhqeN-egHfbhRdYrrRqve4ueHD4pm0MG-cLfXtz4pQIIpSCYOKOlxYCAU74t3C8y3J_mDnedVQRH4iQ"

# client = boto3.client('cognito-idp', region_name='us-east-1')
# response = client.get_user(AccessToken = accessToken)
# st.write(response)
# email = response["Username"]
# print(response)

def get_access_token() -> str:
    url = None
    token_list = []
    token_list = st.query_params.get_all("access_token")
    # print(url)
    print(token_list)

    if len(token_list) > 0:
        print(token_list[0])
        return token_list[0]
    return None
    # url = st.session_state.get('url')
    # if url is not None:
    #     parts = url.split('&')
    #     if len(parts) > 1:
    #         for part in parts:
    #             if part.startswith('access_token'):
    #                 return part.split('=')[1]
    # return None


def get_email_from_cognito_access_token() -> str:
    try:
        response = "Something...."
        client = boto3.client('cognito-idp', region_name='us-east-1')
        # response = client.decode_id_token(IdToken = id_token)
        response = response.join(client.get_user(AccessToken = accessToken))
        # print(response)
        st.write(response)
        email = response["Username"]
        # print(email)
        return email
    except Exception as e:
        print(f"Error decoding ID token: {e}")
        return None

accessToken = get_access_token()
print(accessToken)

if accessToken == None:
    client_id_token = "72011ciu7lf2an6ftbd6ori7ns"
    cognito_url = "https://learnsmart-gvpce-genai.auth.us-east-1.amazoncognito.com/login?client_id=43s8f0sg81oebje23vae0g4pa0&response_type=code&scope=email+openid+phone&redirect_uri=https%3A%2F%2Flearnsmart-gvpce-genai"
    st.link_button(label = "Login/Signup", url = cognito_url, help = "Go to Login/Signup page")
else:
    email = get_email_from_cognito_id_token(accessToken)
    st.write(f"Welcome, {email}!")