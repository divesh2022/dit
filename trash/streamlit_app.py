import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(page_title="DIT Admin UI", layout="wide")

if "token" not in st.session_state:
    st.session_state.token = None
if "user" not in st.session_state:
    st.session_state.user = {}

st.title("DIT - Minimal Admin UI")

if not st.session_state.token:
    st.header("Login (dev)")
    with st.form("login"):
        username = st.text_input("Username", value="student1")
        role = st.selectbox("Role", options=["student", "faculty", "admin"], index=0)
        user_id = st.number_input("User ID", min_value=1, value=1)
        minutes = st.number_input("Token TTL (minutes)", min_value=1, value=60)
        submitted = st.form_submit_button("Get token")
        if submitted:
            payload = {"username": username, "role": role, "user_id": user_id, "expires_minutes": minutes}
            try:
                r = requests.post(f"{API_URL}/auth/token", json=payload, timeout=5)
                r.raise_for_status()
                data = r.json()
                st.session_state.token = data["access_token"]
                st.session_state.user = {"username": username, "role": role, "id": user_id}
                st.success("Logged in (dev token issued)")
            except Exception as e:
                st.error(f"Login failed: {e}")
else:
    st.sidebar.markdown(f"**User:** {st.session_state.user.get('username')}  ")
    st.sidebar.markdown(f"**Role:** {st.session_state.user.get('role')}  ")
    if st.sidebar.button("Logout"):
        st.session_state.token = None
        st.session_state.user = {}
        st.experimental_rerun()

    st.header("Dashboard")

    # Student-specific view
    if st.session_state.user.get("role") == "student":
        st.subheader("My Reports")
        subject_filter = st.text_input("Subject code (optional)")
        semester_filter = st.text_input("Semester (optional)")
        params = {}
        if subject_filter:
            params["subject_code"] = subject_filter
        if semester_filter:
            params["semester"] = semester_filter

        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        try:
            resp = requests.get(f"{API_URL}/student/reports", params=params, headers=headers, timeout=5)
            if resp.status_code == 200:
                rows = resp.json()
                if rows:
                    for r in rows:
                        st.markdown(f"**{r.get('subject_code')} - {r.get('subject_name')}**")
                        st.write({"marks": r.get("marks"), "grade": r.get("grade"), "semester": r.get("semester")})
                        st.divider()
                else:
                    st.info("No reports found")
            else:
                st.error(f"Failed to fetch reports: {resp.status_code} {resp.text}")
        except Exception as e:
            st.error(f"Request error: {e}")

    else:
        st.subheader("Faculty / Admin")
        st.info("Use API endpoints directly or extend this UI. Example: view students, create assignments.")

    st.markdown("---")
    st.caption("This is a minimal development UI. Secure token issuance and user authentication are required for production.")