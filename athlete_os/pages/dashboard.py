
import plotly.graph_objects as go
import streamlit as st

from athlete_os.config import DIMENSION_IDS, DIMENSION_NAMES
from athlete_os.scoring import (
    daily_recommendations,
    dimension_scores,
    knee_status_from_latest,
    readiness_emoji,
    recovery_score,
)
from athlete_os.storage import load_baselines, load_training, load_wellness, save_baselines


def radar_chart(scores_df):
    labels = scores_df["dimension"].tolist()
    vals = scores_df["current_level"].tolist()

    # close polygon
    labels_closed = labels + [labels[0]]
    vals_closed = vals + [vals[0]]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=vals_closed,
        theta=labels_closed,
        fill="toself",
        name="Niveau actuel",
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[-1, 5], tickvals=[-1, 0, 1, 2, 3, 4, 5])
        ),
        showlegend=False,
        margin=dict(l=20, r=20, t=40, b=20),
        height=520,
    )
    return fig


def render():
    st.title("🏋️ Athlete OS v2")
    st.caption("Dashboard de récupération, niveaux physiques et décision du jour.")

    wellness = load_wellness()
    training = load_training()
    baselines = load_baselines()

    score = recovery_score(wellness)
    status, msg = knee_status_from_latest(wellness)
    scores_df = dimension_scores(baselines, training, wellness)

    knee_level = scores_df.loc[scores_df["dimension_id"] == "knee_health", "current_level"].iloc[0]
    power_level = scores_df.loc[scores_df["dimension_id"] == "power", "current_level"].iloc[0]
    flex_level = scores_df.loc[scores_df["dimension_id"] == "flexibility", "current_level"].iloc[0]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Recovery score", f"{readiness_emoji(score)} {score:.0f}%")
    c2.metric("Statut genou", status)
    c3.metric("Genou", f"{knee_level:.1f}/5")
    c4.metric("Flexibilité", f"{flex_level:.1f}/5")

    if status == "RED":
        st.error(msg)
    elif status == "ORANGE":
        st.warning(msg)
    elif status == "GREEN":
        st.success(msg)
    else:
        st.info(msg)

    left, right = st.columns([1.15, 1])
    with left:
        st.subheader("Radar des dimensions")
        st.plotly_chart(radar_chart(scores_df), use_container_width=True)

    with right:
        st.subheader("Décision du jour")
        recs = daily_recommendations(status)
        st.write("✅ **À faire**")
        for item in recs["do"]:
            st.write(f"- {item}")
        st.write("⛔ **À éviter**")
        for item in recs["avoid"]:
            st.write(f"- {item}")

    st.subheader("Niveaux actuels")
    st.dataframe(
        scores_df[[
            "dimension",
            "current_level",
            "status",
            "baseline",
            "adaptation",
            "penalty",
            "manual_adjust",
            "progress_pct",
        ]],
        use_container_width=True,
        hide_index=True,
    )

    with st.expander("Modifier les niveaux de base"):
        st.write("Utilise cette section pour corriger ton niveau de départ. L'entraînement et la douleur ajustent ensuite le niveau actuel.")
        edited = baselines.copy()
        for i, row in edited.iterrows():
            st.markdown(f"**{row['dimension_name']}**")
            col1, col2 = st.columns(2)
            with col1:
                edited.loc[i, "baseline_level"] = st.slider(
                    f"Baseline {row['dimension_name']}",
                    -1.0,
                    5.0,
                    float(row["baseline_level"]),
                    0.1,
                    key=f"base_{row['dimension_id']}",
                )
            with col2:
                edited.loc[i, "manual_adjust"] = st.slider(
                    f"Ajustement manuel {row['dimension_name']}",
                    -1.0,
                    1.0,
                    float(row["manual_adjust"]),
                    0.1,
                    key=f"adjust_{row['dimension_id']}",
                )
            edited.loc[i, "notes"] = st.text_input(
                f"Notes {row['dimension_name']}",
                value=str(row.get("notes", "")),
                key=f"notes_{row['dimension_id']}",
            )
        if st.button("Sauvegarder les niveaux"):
            save_baselines(edited)
            st.success("Niveaux sauvegardés. Recharge la page si nécessaire.")
