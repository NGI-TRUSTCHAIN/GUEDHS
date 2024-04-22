import streamlit as st
import syft as sy
import pandas as pd


def main():
    st.title("GUEHDS Portal")

    if "login_status" not in st.session_state:
        st.session_state['login_status'] = False

    if not st.session_state.login_status:  # Show login UI if not logged in
        show_login_form()
    else:
        show_datasets()


def show_login_form():
    st.subheader("Tenant Login")
    url = st.text_input("URL")
    port = st.text_input("Port")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        try:
            client = sy.login(url=url, port=port, email=email, password=password)
            st.success("Login successful!")
            st.session_state.login_status = True
            st.session_state.client = client
            st.rerun()
        except Exception as e:
            st.error(f"Login failed: {e}")


def show_datasets():
    st.subheader("Datasets")
    datasets = st.session_state.client.datasets
    st.dataframe(
        pd.DataFrame(
            [{k: str(v) for k, v in dataset if k in ["id", "name", "updated_at", "created_at"]} for dataset in datasets]
        )
    )


if __name__ == "__main__":
    main()
