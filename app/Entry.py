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

def main():

    st.title(":open_book: Welcome to Learn Smart!!")

    st.header("Your best companion to efficient learning!!")
    
    st.markdown(
        """
        <style>
        .button {
        display: inline-block;
        padding: 10px 20px;
        background-color: #4CAF50;
        color: white;
        text-align: center;
        text-decoration: none;
        font-size: 16px;
        border-radius: 4px;
        }

        .button:hover {
            background-color: #45a049;
        }
        </style>
        """, unsafe_allow_html=True)

    st.page_link("pages/1_Login.py", label=":point_up_2: Login", help="For your existing account!")
    st.page_link("pages/2_Signup.py", label=":male-technologist: Sign up", help="To create a new account!")

if __name__ == "__main__":
    main()
