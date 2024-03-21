import boto3
import streamlit as st
from streamlit_javascript import st_javascript

url = str(st_javascript("await fetch('').then(r => window.parent.location.href)"))

st.write(f"Current URL : {url}")

accessToken = url.split('access_token=')[1].split('&')[0]

# print(f"\n\n\n\n\n\{accessToken}\n\n\n\n\n")

st.write(accessToken)
# accessTokenObj = paramsList[-3]
# accessToken = accessTokenObj.split('=')[1]

region = 'us-east-1'
client = boto3.client('cognito-idp', region_name = region)
response = client.get_user(
    AccessToken = accessToken
)

userName = response['Username']


accessToken = st.query_params.get_all('access_token')
st.write(accessToken)