import streamlit as st
import requests

API="http://127.0.0.1:8000"

if "token" not in st.session_state:
    st.session_state.token=None

if "challenge" not in st.session_state:
    st.session_state.challenge=None

def get_challenge():
    response=requests.get(f"{API}/auth/challenge")
    st.session_state.challenge=response.json()

if not st.session_state.token:
    st.title("📚 Book Store")
    st.header("Login")

    try:
        if st.session_state.challenge is None:
            get_challenge()

        challenge=st.session_state.challenge

        st.write("رتب الأرقام من الأصغر إلى الأكبر:")
        st.write(challenge["numbers"])

        username=st.text_input("Username")
        password=st.text_input("Password",type="password")
        answer=st.text_input("Answer",placeholder="Example: 1,2,3,4,5")

        if st.button("Login"):
            data={
                "username":username,
                "password":password
            }

            params={
                "challenge_token":challenge["challenge_token"],
                "challenge_answer":answer
            }

            response=requests.post(
                f"{API}/auth/login",
                data=data,
                params=params
            )

            if response.status_code==200:
                st.session_state.token=response.json()["access_token"]
                st.session_state.challenge=None
                st.rerun()
            else:
                st.error(response.json().get("detail","Login failed"))

    except requests.RequestException:
        st.warning("Backend is not running")

else:
    st.title("📚 Book Store")
    st.success("Login successful")

    headers={
        "Authorization":f"Bearer {st.session_state.token}"
    }

    st.header("Available Books")

    try:
        response=requests.get(
            f"{API}/books",
            headers=headers
        )

        if response.status_code==200:
            books=response.json()

            if not books:
                st.info("No books available")

            for book in books:
                st.subheader(book.get("title","Book"))

                if "price" in book:
                    st.write("Price:",book["price"])

                if "stock" in book:
                    st.write("Stock:",book["stock"])

                st.divider()

    except requests.RequestException:
        st.warning("Backend is not running")

    if st.button("Logout"):
        st.session_state.token=None
        st.session_state.challenge=None
        st.rerun()