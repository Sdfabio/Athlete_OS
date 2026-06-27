
import pandas as pd
import streamlit as st

from Athlete_OS.athlete_os.config import CATEGORIES, DIMENSIONS, EFFECT_COLUMNS
from Athlete_OS.athlete_os.storage import add_exercise, load_exercises


def render():
    st.title("📚 Bibliothèque exercices")
    st.caption("Ajoute tes exercices. Chaque exercice peut influencer plusieurs dimensions.")

    exercises = load_exercises()

    st.subheader("Exercices existants")
    filters = st.multiselect("Filtrer par catégorie", sorted(exercises["category"].dropna().unique().tolist()))
    view = exercises.copy()
    if filters:
        view = view[view["category"].isin(filters)]
    st.dataframe(view, use_container_width=True, hide_index=True)

    st.subheader("Ajouter un exercice")

    with st.form("add_exercise_form"):
        col1, col2 = st.columns(2)
        name = col1.text_input("Nom de l'exercice", placeholder="Ex: Shoulder bridge pulses")
        category = col2.selectbox("Catégorie", CATEGORIES)

        col3, col4 = st.columns(2)
        body_region = col3.text_input("Partie du corps", placeholder="Épaules / dos / hanches...")
        default_dose = col4.text_input("Dose par défaut", placeholder="3 x 10 ou 5 min")

        goal = st.text_input("But", placeholder="Ex: améliorer flexibilité haut du corps")
        notes = st.text_area("Notes")

        col5, col6, col7, col8 = st.columns(4)
        default_intensity = col5.slider("Intensité par défaut", 1, 10, 5)
        knee_load = col6.slider("Charge genou", 0, 10, 0)
        wrist_load = col7.slider("Charge poignets", 0, 10, 0)
        ankle_load = col8.slider("Charge chevilles", 0, 10, 0)

        phase_min = st.slider("Phase genou minimale recommandée", -1, 5, -1)
        equipment = st.text_input("Équipement", placeholder="Rings, foam roller, machine leg extension...")

        st.markdown("### Effets sur les dimensions")
        st.caption("0 = aucun effet, 5 = effet très fort. Ces valeurs servent à estimer tes niveaux avec tes logs.")
        effects = {}
        cols = st.columns(3)
        for i, d in enumerate(DIMENSIONS):
            with cols[i % 3]:
                effects[f"effect_{d['id']}"] = st.slider(d["name"], 0.0, 5.0, 0.0, 0.5, key=f"effect_new_{d['id']}")

        submitted = st.form_submit_button("Ajouter l'exercice")

    if submitted:
        if not name.strip():
            st.error("Ajoute au moins un nom d'exercice.")
            return

        row = {
            "exercise_name": name.strip(),
            "category": category,
            "body_region": body_region,
            "default_dose": default_dose,
            "goal": goal,
            "default_intensity": default_intensity,
            "knee_load": knee_load,
            "wrist_load": wrist_load,
            "ankle_load": ankle_load,
            "phase_min": phase_min,
            "equipment": equipment,
            "notes": notes,
        }
        row.update(effects)
        add_exercise(row)
        st.success(f"Exercice ajouté : {name}")
