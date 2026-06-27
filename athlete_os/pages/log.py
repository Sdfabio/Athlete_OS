
from datetime import date

import pandas as pd
import streamlit as st

from Athlete_OS.athlete_os.config import EFFECT_COLUMNS
from Athlete_OS.athlete_os.storage import (
    append_training_entry,
    load_exercises,
    load_training,
    load_wellness,
    save_wellness_entry,
)


def render():
    st.title("📝 Log douleurs & entraînement")
    st.caption("C'est ici que tu enregistres la douleur, le sommeil et les exercices/cours faits.")

    tab1, tab2, tab3 = st.tabs(["Douleur / sommeil", "Entraînement", "Tables"])

    with tab1:
        st.subheader("Journal quotidien douleur + récupération")

        with st.form("wellness_form"):
            d = st.date_input("Date", value=date.today())
            col1, col2, col3, col4 = st.columns(4)
            pain_morning = col1.slider("Douleur matin", 0, 10, 2)
            pain_stairs = col2.slider("Douleur escaliers", 0, 10, 3)
            pain_squat = col3.slider("Douleur squat/flexion", 0, 10, 4)
            pain_after = col4.slider("Douleur après séance", 0, 10, 3)

            col5, col6, col7 = st.columns(3)
            sleep_hours = col5.slider("Sommeil (heures)", 4.0, 10.0, 8.0, 0.25)
            energy = col6.slider("Énergie", 0, 10, 6)
            stress = col7.slider("Stress", 0, 10, 4)

            notes = st.text_area("Notes", placeholder="Ex: escaliers douloureux au boulot, tendon sensible sous la rotule...")
            submitted = st.form_submit_button("Sauvegarder douleur/sommeil")

        if submitted:
            save_wellness_entry({
                "date": str(d),
                "pain_morning": pain_morning,
                "pain_stairs": pain_stairs,
                "pain_squat": pain_squat,
                "pain_after": pain_after,
                "sleep_hours": sleep_hours,
                "energy": energy,
                "stress": stress,
                "notes": notes,
            })
            st.success("Journal quotidien sauvegardé.")

    with tab2:
        st.subheader("Log d'un exercice ou cours")

        exercises = load_exercises()
        if exercises.empty:
            st.warning("Aucun exercice dans la bibliothèque.")
            return

        names = exercises["exercise_name"].tolist()
        selected_name = st.selectbox("Exercice / cours", names)
        ex = exercises[exercises["exercise_name"] == selected_name].iloc[0].to_dict()

        st.info(f"Catégorie : {ex['category']} | Région : {ex['body_region']} | Dose par défaut : {ex['default_dose']}")

        with st.expander("Voir les effets de cet exercice sur les dimensions"):
            effect_cols = [c for c in EFFECT_COLUMNS if float(ex.get(c, 0) or 0) != 0]
            if effect_cols:
                effect_df = pd.DataFrame([
                    {"Dimension": c.replace("effect_", ""), "Effet": ex[c]} for c in effect_cols
                ])
                st.dataframe(effect_df, use_container_width=True, hide_index=True)
            else:
                st.write("Aucun effet dimensionnel défini.")

        with st.form("training_form"):
            d = st.date_input("Date séance", value=date.today(), key="training_date")
            col1, col2, col3 = st.columns(3)
            duration_min = col1.number_input("Durée (min)", min_value=1, max_value=240, value=30)
            intensity = col2.slider("Intensité", 1, 10, int(float(ex.get("default_intensity", 5) or 5)))
            sets = col3.number_input("Sets", min_value=0, max_value=20, value=0)

            col4, col5, col6 = st.columns(3)
            reps = col4.number_input("Reps total ou reps/set", min_value=0, max_value=200, value=0)
            pain_before = col5.slider("Douleur avant", 0, 10, 0)
            pain_after = col6.slider("Douleur après", 0, 10, 0)

            st.write("Charges articulaires ressenties")
            col7, col8, col9 = st.columns(3)
            knee_load = col7.slider("Charge genou", 0, 10, int(float(ex.get("knee_load", 0) or 0)))
            wrist_load = col8.slider("Charge poignets", 0, 10, int(float(ex.get("wrist_load", 0) or 0)))
            ankle_load = col9.slider("Charge chevilles", 0, 10, int(float(ex.get("ankle_load", 0) or 0)))

            notes = st.text_area("Notes séance", placeholder="Ex: leg extension iso OK, douleur 2/10, pas pire après.")
            submitted = st.form_submit_button("Sauvegarder entraînement")

        if submitted:
            entry = {
                "date": str(d),
                "exercise_name": ex["exercise_name"],
                "category": ex["category"],
                "body_region": ex["body_region"],
                "duration_min": duration_min,
                "intensity": intensity,
                "knee_load": knee_load,
                "wrist_load": wrist_load,
                "ankle_load": ankle_load,
                "sets": sets,
                "reps": reps,
                "pain_before": pain_before,
                "pain_after": pain_after,
                "notes": notes,
            }
            for c in EFFECT_COLUMNS:
                entry[c] = ex.get(c, 0.0)
            append_training_entry(entry)
            st.success("Séance sauvegardée.")

    with tab3:
        st.subheader("Données persistantes")
        st.write("Wellness log")
        st.dataframe(load_wellness(), use_container_width=True)
        st.write("Training log")
        st.dataframe(load_training(), use_container_width=True)
