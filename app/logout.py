import streamlit as st

def main():
    st.title("Logout Page")
    st.write("You have been successfully logged out!")

    if st.button("Login/Sign-up again"):
        signup_again_url = "https://learn-smart-gvpce.auth.us-east-1.amazoncognito.com/login?client_id=72011ciu7lf2an6ftbd6ori7ns&response_type=token&scope=email+openid+phone&redirect_uri=https%3A%2F%2Fgvpcegenai-learnsmart-z0dpk9nof0a.ws-us110.gitpod.io%2F"
        st.markdown(f"<a[Signup/Login]({signup_login_url})", unsafe_allow_html = True)
        # st.experimental_rerun()


if __init__ == "__main__":
    main()