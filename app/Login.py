import streamlit as st

cognito_url = "https://learn-smart-gvpce.auth.us-east-1.amazoncognito.com/oauth2/authorize?client_id=72011ciu7lf2an6ftbd6ori7ns&response_type=token&scope=email+openid+phone&redirect_uri=https%3A%2F%2F8501-gvpcegenai-learnsmart-z0dpk9nof0a.ws-us110.gitpod.io%2FHomepage"

link_text = 'Login/Sign-Up'

st.markdown(f'<a href="{cognito_url}" target="_self">{link_text}</a>', unsafe_allow_html=True)