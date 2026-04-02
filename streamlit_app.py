import requests
import streamlit as st

API_BASE_URL = "http://127.0.0.1:8000"


def login(username, password):
    response = requests.post(
        f"{API_BASE_URL}/login",
        json={
            "username": username,
            "password": password
        },
        timeout=60
    )
    return response


def ask_question(username, password, question):
    response = requests.post(
        f"{API_BASE_URL}/query",
        json={
            "username": username,
            "password": password,
            "question": question
        },
        timeout=120
    )
    return response


def init_session():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "user" not in st.session_state:
        st.session_state.user = None
    if "username" not in st.session_state:
        st.session_state.username = ""
    if "password" not in st.session_state:
        st.session_state.password = ""


def logout():
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.username = ""
    st.session_state.password = ""


def render_login():
    st.title("Enterprise Knowledge Assistant")
    st.subheader("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if not username or not password:
            st.error("Enter both username and password.")
            return

        try:
            response = login(username, password)
            if response.status_code == 200:
                payload = response.json()
                st.session_state.logged_in = True
                st.session_state.user = payload["user"]
                st.session_state.username = username
                st.session_state.password = password
                st.success("Login successful.")
                st.rerun()
            else:
                try:
                    detail = response.json().get("detail", "Login failed.")
                except Exception:
                    detail = "Login failed."
                st.error(detail)
        except requests.exceptions.RequestException as exc:
            st.error(f"Could not connect to backend: {exc}")


def render_app():
    user = st.session_state.user

    st.title("Enterprise Knowledge Assistant")
    st.caption("Role-based secure querying over organizational documents")

    col1, col2 = st.columns([3, 1])

    with col1:
        st.write(f"Logged in as: `{user['username']}`")
        st.write(f"Role: `{user['role']}`")
        st.write(f"Domain: `{user.get('domain')}`")

    with col2:
        if st.button("Logout"):
            logout()
            st.rerun()

    st.divider()

    question = st.text_area(
        "Ask a question",
        placeholder="Example: What is the code of ethics?"
    )

    if st.button("Get Answer"):
        if not question.strip():
            st.warning("Enter a question first.")
            return

        try:
            with st.spinner("Retrieving answer..."):
                response = ask_question(
                    st.session_state.username,
                    st.session_state.password,
                    question
                )

            if response.status_code == 200:
                payload = response.json()

                st.subheader("Answer")
                st.write(payload["answer"])

                st.subheader("Sources")
                sources = payload.get("sources", [])
                if sources:
                    for source in sources:
                        st.write(f"- {source}")
                else:
                    st.info("No sources found.")
            else:
                try:
                    detail = response.json().get("detail", "Query failed.")
                except Exception:
                    detail = "Query failed."
                st.error(detail)

        except requests.exceptions.RequestException as exc:
            st.error(f"Could not connect to backend: {exc}")


def main():
    st.set_page_config(
        page_title="Enterprise Knowledge Assistant",
        page_icon="📘",
        layout="wide"
    )
    init_session()

    if not st.session_state.logged_in:
        render_login()
    else:
        render_app()


if __name__ == "__main__":
    main()