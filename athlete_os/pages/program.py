
import pandas as pd
import streamlit as st

from athlete_os.scoring import knee_status_from_latest
from athlete_os.storage import load_wellness

WEEKLY_SCHEDULE = pd.DataFrame([
    ["Lundi", "Bureau 8h30-16h30", "17h-18h Équilibre", "19h-20h option : Rings / Flexibilité / Physio longue", "Meilleur jour haut du corps + poignets."],
    ["Mardi", "Bureau 8h30-16h30", "17h30-19h Bootcamp OU 19h-20h Acro basics", "Choisir selon genou", "Bootcamp = plus risqué pour tendon. Acro selon contenu."],
    ["Mercredi", "Maison 8h30-16h30", "19h-21h Mouvements / Hammock / Aérien", "Avant : physio + hanches", "Si mouvements = genou, adapter."],
    ["Jeudi", "Maison 8h30-16h30", "19h-21h Obstacles / Équilibre / Foundations", "Obstacles seulement si genou vert", "Parkour = prudence."],
    ["Vendredi", "Variable", "Aerial / Acro / Backflip selon horaire", "Core + rings si pas de cours", "Ne pas forcer jambes si semaine lourde."],
    ["Samedi", "Libre", "Champignon / Rings / Mobilité profonde", "Long stretch + massage", "Jour idéal skills sans impacts."],
    ["Dimanche", "Repos actif", "Soft acro jam seulement si genou vert", "Marche + récupération", "Pas de surcharge."],
], columns=["Jour", "Travail", "Cours possible", "Bloc ajouté", "Note"])

PHASES = pd.DataFrame([
    ["-1", "Tendon très irrité", "Escaliers douloureux", "Physio quotidienne, massage, haut du corps, mobilité active", "Sauts, bootcamp, front flips, parkour"],
    ["0", "Rééducation active", "Escaliers ≤2/10", "Isométriques + heavy slow + rings/core", "Volume explosif"],
    ["1", "Fondation force", "Squat contrôlé ≤3/10, pas pire le lendemain", "Leg extension lourd, split squat, mollets, core", "Depth jumps"],
    ["2", "Réintroduction dynamique", "Jog/sauts bas tolérés", "Pogos légers, technique acro douce", "Max effort"],
    ["3", "Puissance contrôlée", "Sauts/réceptions sans flare-up 24h", "Box jumps, bounds, acro plus complète", "Volume excessif"],
    ["4", "Performance", "Entraînement régulier sans douleur persistante", "Tumbling, parkour modéré, force lourde", "Tests béton/impacts inutiles"],
    ["5", "Peak mode", "Tolérance haute + récupération rapide", "Puissance + flexibilité + skills avancés", "Ego lifting / douleur ignorée"],
], columns=["Phase", "Nom", "Critère d'entrée", "Focus", "À éviter"])

MIN_ROUTINE = pd.DataFrame([
    ["Genou", "Spanish squat iso", "5 x 45-60s"],
    ["Genou", "Leg extension iso", "5 x 30-45s"],
    ["Chevilles", "Tibialis + mollets", "3 x 20 + 3 x 15"],
    ["Hanches", "Active Hip IR + 90/90", "2 x 8/side + 2-3 min"],
    ["Poignets", "CARs + extensions/flexions", "5 min"],
    ["Massage", "Foam rolling quad/TFL/adducteurs/mollets", "8-10 min"],
    ["Flexibilité", "Hanches + dos/pont", "15-20 min"],
], columns=["Zone", "Exercice", "Dose"])


def render():
    st.title("📅 Programme semaine")
    wellness = load_wellness()
    status, msg = knee_status_from_latest(wellness)

    if status == "RED":
        st.error(msg)
    elif status == "ORANGE":
        st.warning(msg)
    elif status == "GREEN":
        st.success(msg)
    else:
        st.info(msg)

    st.subheader("Horaire hebdomadaire")
    st.dataframe(WEEKLY_SCHEDULE, use_container_width=True, hide_index=True)

    st.subheader("Routine minimale quotidienne")
    st.dataframe(MIN_ROUTINE, use_container_width=True, hide_index=True)

    st.subheader("Phases du genou / retour puissance")
    st.dataframe(PHASES, use_container_width=True, hide_index=True)

    st.markdown("""
    ### Règle de progression
    Tu ne passes pas à la phase suivante parce que tu es motivé.  
    Tu passes quand le genou ne réagit pas mal dans les **24-48h** après la charge.

    ### Règle rouge
    Si les escaliers ou le squat montent à **5/10 ou plus**, la priorité redevient :
    physio, massage, mobilité active, haut du corps, rings basiques, core sans douleur.
    """)
