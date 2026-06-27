
import pandas as pd
import plotly.express as px
import streamlit as st

from athlete_os.scoring import dimension_scores, recovery_series
from athlete_os.storage import load_baselines, load_training, load_wellness


def render():
    st.title("📈 Historique & analytics")

    wellness = load_wellness()
    training = load_training()
    baselines = load_baselines()

    if wellness.empty and training.empty:
        st.info("Pas encore de données. Commence par logger douleurs/sommeil et entraînements.")
        return

    if not wellness.empty:
        st.subheader("Douleurs")
        w = wellness.copy()
        w["date"] = pd.to_datetime(w["date"], errors="coerce")
        pain_cols = ["pain_morning", "pain_stairs", "pain_squat", "pain_after"]
        for c in pain_cols:
            w[c] = pd.to_numeric(w[c], errors="coerce")
        fig = px.line(w, x="date", y=pain_cols, markers=True, title="Douleurs dans le temps")
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Recovery score")
        rs = recovery_series(wellness)
        if not rs.empty:
            rs["date"] = pd.to_datetime(rs["date"], errors="coerce")
            fig2 = px.line(rs, x="date", y="recovery_score", markers=True, title="Recovery score")
            fig2.update_yaxes(range=[0, 100])
            st.plotly_chart(fig2, use_container_width=True)

    if not training.empty:
        st.subheader("Volume d'entraînement")
        t = training.copy()
        t["date"] = pd.to_datetime(t["date"], errors="coerce")
        t["duration_min"] = pd.to_numeric(t["duration_min"], errors="coerce").fillna(0)
        by_cat = t.groupby("category", as_index=False)["duration_min"].sum().sort_values("duration_min", ascending=False)
        fig3 = px.bar(by_cat, x="category", y="duration_min", title="Minutes par catégorie")
        st.plotly_chart(fig3, use_container_width=True)

        st.subheader("Charge genou / poignets / chevilles")
        for c in ["knee_load", "wrist_load", "ankle_load"]:
            t[c] = pd.to_numeric(t[c], errors="coerce").fillna(0)
        t["knee_load_score"] = t["duration_min"] / 30 * t["knee_load"] / 10
        t["wrist_load_score"] = t["duration_min"] / 30 * t["wrist_load"] / 10
        t["ankle_load_score"] = t["duration_min"] / 30 * t["ankle_load"] / 10
        load_daily = t.groupby("date", as_index=False)[["knee_load_score", "wrist_load_score", "ankle_load_score"]].sum()
        fig4 = px.line(load_daily, x="date", y=["knee_load_score", "wrist_load_score", "ankle_load_score"], markers=True, title="Charges articulaires")
        st.plotly_chart(fig4, use_container_width=True)

    st.subheader("Niveaux actuels calculés")
    scores = dimension_scores(baselines, training, wellness)
    st.dataframe(scores, use_container_width=True, hide_index=True)
