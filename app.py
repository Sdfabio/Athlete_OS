
import streamlit as st

from athlete_os.pages import dashboard, exercise_library, history, log
from athlete_os.storage import ensure_data_files
from athlete_os.pages import program

st.set_page_config(page_title="Athlete OS v2", layout="wide")

ensure_data_files()

st.sidebar.title("🏋️ Athlete OS")
page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Log douleurs & entraînement",
        "Bibliothèque exercices",
        "Programme semaine",
        "Historique & analytics",
    ],
)

if page == "Dashboard":
    dashboard.render()
elif page == "Log douleurs & entraînement":
    log.render()
elif page == "Bibliothèque exercices":
    exercise_library.render()
elif page == "Programme semaine":
    program.render()
elif page == "Historique & analytics":
    history.render()
