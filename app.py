import streamlit as st
import pandas as pd

from code import (
    init_user,
    save_profile,
    get_profile,
    get_all,
    leaderboard
)

from study import (
    log_entry,
    remove_entry,
    ENGINEERING_SUBJECTS,
    CODING_LANGUAGES
)

from dash import dashboard
from upload import upload_file


# ==================================
# PAGE CONFIG
# ==================================
st.set_page_config(
    page_title="SkillTrack Pro",
    page_icon="📚",
    layout="wide"
)


# ==================================
# SESSION STATE
# ==================================
if "user" not in st.session_state:
    st.session_state.user = None

if "logged" not in st.session_state:
    st.session_state.logged = False


# ==================================
# LOGIN
# ==================================
def login():

    st.title("🔐 SkillTrack Pro")

    username = st.text_input(
        "Enter Username"
    )

    if st.button("Login"):

        if username.strip():

            init_user(username)

            st.session_state.user = username
            st.session_state.logged = True

            st.rerun()


# ==================================
# PROFILE CREATION
# ==================================
def profile_form():

    st.title("👤 Create Profile")

    name = st.text_input("Full Name")

    year = st.selectbox(
        "Year",
        [
            "1st Year",
            "2nd Year",
            "3rd Year",
            "4th Year"
        ]
    )

    branch = st.text_input("Branch")

    if st.button("Save Profile"):

        save_profile(
            st.session_state.user,
            name,
            year,
            branch
        )

        st.success(
            "Profile Created Successfully 🚀"
        )

        st.rerun()


# ==================================
# DASHBOARD
# ==================================
def dashboard_page():

    dashboard(
        st.session_state.user
    )


# ==================================
# STUDY PAGE
# ==================================
def study_page():

    st.title("📚 Study Tracker")

    subjects = st.multiselect(
        "📚 Select Subjects",
        ENGINEERING_SUBJECTS
    )

    languages = st.multiselect(
        "💻 Coding Languages",
        CODING_LANGUAGES
    )

    problems = st.number_input(
        "🧠 Problems Solved",
        min_value=1,
        value=1
    )

    if st.button("🚀 Add Entry"):

        if not subjects:

            st.warning(
                "Select at least one subject"
            )

            return

        for subject in subjects:

            log_entry(
                st.session_state.user,
                subject,
                problems,
                languages
            )

        st.success(
            f"Added {len(subjects)} entries"
        )

        st.rerun()


# ==================================
# ENTRIES PAGE
# ==================================
def entries_page():

    st.title("📋 Entries")

    data = get_all(
        st.session_state.user
    )

    if not data:

        st.info(
            "No entries available"
        )

        return

    for entry in reversed(data):

        with st.container():

            col1, col2, col3, col4 = st.columns(
                [4, 2, 2, 1]
            )

            with col1:

                st.write(
                    f"📘 {entry['topic']}"
                )

                if entry.get("languages"):

                    st.caption(
                        "💻 " +
                        ", ".join(
                            entry["languages"]
                        )
                    )

            with col2:

                st.write(
                    f"🧠 {entry['problems']}"
                )

            with col3:

                st.write(
                    f"⭐ {entry.get('stars', 0)}"
                )

            with col4:

                if st.button(
                    "❌",
                    key=f"del_{entry['id']}"
                ):

                    remove_entry(
                        st.session_state.user,
                        entry["id"]
                    )

                    st.rerun()

            st.divider()


# ==================================
# LEADERBOARD
# ==================================
def leaderboard_page():

    st.title("🏆 Leaderboard")

    board = leaderboard()

    if not board:

        st.info(
            "No users yet"
        )

        return

    df = pd.DataFrame(board)

    st.dataframe(
        df,
        use_container_width=True
    )


# ==================================
# PROFILE PAGE
# ==================================
def profile_page():

    st.title("👤 Profile")

    profile = get_profile(
        st.session_state.user
    )

    st.write(
        f"**Name:** {profile.get('name', '')}"
    )

    st.write(
        f"**Year:** {profile.get('year', '')}"
    )

    st.write(
        f"**Branch:** {profile.get('branch', '')}"
    )

    st.divider()

    st.subheader("Update Profile")

    new_name = st.text_input(
        "Name",
        value=profile.get("name", "")
    )

    new_year = st.selectbox(
        "Year",
        [
            "1st Year",
            "2nd Year",
            "3rd Year",
            "4th Year"
        ]
    )

    new_branch = st.text_input(
        "Branch",
        value=profile.get("branch", "")
    )

    if st.button("Update Profile"):

        save_profile(
            st.session_state.user,
            new_name,
            new_year,
            new_branch
        )

        st.success(
            "Profile Updated Successfully"
        )

        st.rerun()


# ==================================
# UPLOAD PAGE
# ==================================
def upload_page():

    st.title("📤 Upload CSV")

    file = st.file_uploader(
        "Upload CSV",
        type=["csv"]
    )

    category = st.selectbox(
        "Category",
        [
            "study",
            "coding"
        ]
    )

    if file:

        result = upload_file(
            st.session_state.user,
            file,
            category
        )

        if result.startswith("✅"):

            st.success(result)

        else:

            st.error(result)


# ==================================
# MAIN APP
# ==================================
def main():

    if not st.session_state.logged:

        login()

        return

    profile = get_profile(
        st.session_state.user
    )

    if not profile.get("created"):

        profile_form()

        return

    st.sidebar.title("📌 Menu")

    st.sidebar.write(
        f"👤 {profile.get('name', 'User')}"
    )

    menu = st.sidebar.radio(
        "Navigation",
        [
            "📊 Dashboard",
            "📚 Study",
            "📋 Entries",
            "🏆 Leaderboard",
            "👤 Profile",
            "📤 Upload"
        ]
    )

    if menu == "📊 Dashboard":

        dashboard_page()

    elif menu == "📚 Study":

        study_page()

    elif menu == "📋 Entries":

        entries_page()

    elif menu == "🏆 Leaderboard":

        leaderboard_page()

    elif menu == "👤 Profile":

        profile_page()

    elif menu == "📤 Upload":

        upload_page()


# ==================================
# RUN APP
# ==================================
main()
