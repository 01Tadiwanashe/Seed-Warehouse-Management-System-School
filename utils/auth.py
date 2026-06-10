import streamlit as st
import hashlib

USERS = {
    "admin":   hashlib.sha256("admin123".encode()).hexdigest(),
    "manager": hashlib.sha256("manager123".encode()).hexdigest(),
    "staff":   hashlib.sha256("staff123".encode()).hexdigest(),
}

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def login_page():
    st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background: #FFFFFF; }
    [data-testid="stHeader"] { background: #FFFFFF; }
    div.stButton > button {
        background-color: #2E7D32 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        width: 100%;
    }
    div.stButton > button:hover { background-color: #1B5E20 !important; }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        import os
        if os.path.exists("assets/logo.png"):
            st.image("assets/logo.png", use_container_width=True)

        st.markdown("""
        <div style="background:#F1F8E9;border:2px solid #2E7D32;border-radius:12px;
                    padding:32px 36px;margin-top:16px;">
          <h2 style="text-align:center;color:#2E7D32;margin-top:0;">
            Smart Seed Warehouse
          </h2>
          <h4 style="text-align:center;color:#C62828;margin-bottom:24px;">
            Management System
          </h4>
        </div>
        """, unsafe_allow_html=True)

        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")

        if st.button("Login", use_container_width=True):
            if username in USERS and USERS[username] == hash_password(password):
                st.session_state["authenticated"] = True
                st.session_state["username"]      = username
                st.rerun()
            else:
                st.error("Invalid username or password.")

        st.caption("Default: admin / admin123  |  staff / staff123")
    return False

def require_login():
    if not st.session_state.get("authenticated", False):
        login_page()
        st.stop()

def logout_button():
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        f"Logged in as **{st.session_state.get('username', 'user')}**"
    )
    if st.sidebar.button("Logout"):
        st.session_state["authenticated"] = False
        st.session_state["username"]      = ""
        st.rerun()
