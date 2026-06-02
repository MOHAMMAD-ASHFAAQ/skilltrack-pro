import streamlit as st
import pandas as pd
import plotly.express as px

from study import (
    fetch_entries,
    subject_stats,
    language_stats,
    total_stars,
    total_problems,
    total_entries
)

from code import (
    load_raw,
    get_profile,
    leaderboard
)


# ==================================
# DASHBOARD
# ==================================
def dashboard(user):

    st.title("📊 SkillTrack Dashboard")

    data = fetch_entries(user)

    profile = get_profile(user)

    # --------------------------
    # PROFILE CARD
    # --------------------------
    with st.container():

        st.subheader("👤 Profile")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.info(f"Name\n\n{profile.get('name', '')}")

        with col2:
            st.info(f"Year\n\n{profile.get('year', '')}")

        with col3:
            st.info(f"Branch\n\n{profile.get('branch', '')}")

    st.divider()

    # --------------------------
    # TOP METRICS
    # --------------------------
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "🔥 Streak",
            load_raw().get(user, {}).get("streak", 0)
        )

    with col2:
        st.metric(
            "⭐ Stars",
            total_stars(user)
        )

    with col3:
        st.metric(
            "🧠 Problems",
            total_problems(user)
        )

    with col4:
        st.metric(
            "📚 Entries",
            total_entries(user)
        )

    st.divider()

    # --------------------------
    # EMPTY STATE
    # --------------------------
    if not data:
        st.warning("No study data available.")
        return

    # --------------------------
    # DATAFRAME
    # --------------------------
    df = pd.DataFrame(data)

    # --------------------------
    # SUBJECT GRAPH
    # --------------------------
    st.subheader("📚 Subject Analytics")

    subject_data = subject_stats(user)

    if subject_data:

        subject_df = pd.DataFrame(
            list(subject_data.items()),
            columns=["Subject", "Problems"]
        )

        fig = px.bar(
            subject_df,
            x="Subject",
            y="Problems",
            text="Problems",
            title="Problems by Subject"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.divider()

    # --------------------------
    # LANGUAGE GRAPH
    # --------------------------
    st.subheader("💻 Language Analytics")

    lang_data = language_stats(user)

    if lang_data:

        lang_df = pd.DataFrame(
            list(lang_data.items()),
            columns=["Language", "Problems"]
        )

        fig2 = px.pie(
            lang_df,
            names="Language",
            values="Problems",
            hole=0.4,
            title="Coding Language Usage"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    st.divider()

    # --------------------------
    # DAILY PROGRESS
    # --------------------------
    st.subheader("📈 Daily Progress")

    if "date" in df.columns:

        df["date"] = pd.to_datetime(df["date"])

        daily = (
            df.groupby("date")["problems"]
            .sum()
            .reset_index()
        )

        fig3 = px.line(
            daily,
            x="date",
            y="problems",
            markers=True,
            title="Daily Problems Solved"
        )

        st.plotly_chart(
            fig3,
            use_container_width=True
        )

    st.divider()

    # --------------------------
    # RECENT ENTRIES
    # --------------------------
    st.subheader("📝 Recent Entries")

    recent = df.sort_values(
        "id",
        ascending=False
    ).head(10)

    st.dataframe(
        recent,
        use_container_width=True
    )

    st.divider()

    # --------------------------
    # LEADERBOARD
    # --------------------------
    st.subheader("🏆 Leaderboard")

    board = leaderboard()

    if board:

        board_df = pd.DataFrame(board)

        st.dataframe(
            board_df,
            use_container_width=True
        )
