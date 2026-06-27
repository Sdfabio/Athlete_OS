
from __future__ import annotations

from datetime import date

import numpy as np
import pandas as pd

from Athlete_OS.athlete_os.config import DIMENSION_IDS, DIMENSION_NAMES, EFFECT_COLUMNS


def clamp(x, lo, hi):
    return max(lo, min(hi, x))


def level_label(x: float) -> str:
    if x < 0:
        return "Blessé / ne pas charger"
    if x < 1:
        return "Rééducation"
    if x < 2:
        return "Fondations"
    if x < 3:
        return "Intermédiaire"
    if x < 4:
        return "Avancé"
    if x < 5:
        return "Élite"
    return "Pro"


def knee_status_from_latest(wellness: pd.DataFrame):
    latest = latest_wellness(wellness)
    if latest is None:
        return "UNKNOWN", "Pas encore de log douleur aujourd'hui."

    pain_stairs = float(latest.get("pain_stairs", 0) or 0)
    pain_squat = float(latest.get("pain_squat", 0) or 0)
    pain_morning = float(latest.get("pain_morning", 0) or 0)
    pain_after = float(latest.get("pain_after", 0) or 0)
    avg = np.mean([pain_stairs, pain_squat, pain_morning, pain_after])

    if pain_stairs >= 5 or pain_squat >= 5 or pain_after >= 6:
        return "RED", "Genou très irrité : pas de mouvements explosifs, pas de parkour, pas de front flips."
    if avg >= 3 or pain_stairs >= 4 or pain_squat >= 4:
        return "ORANGE", "Charge modérée : physio + haut du corps + mobilité active. Évite les impacts répétés."
    return "GREEN", "Charge contrôlée possible : progression lente, pas de saut maximal non planifié."


def latest_wellness(wellness: pd.DataFrame):
    if wellness is None or wellness.empty:
        return None
    df = wellness.copy()
    df["_date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["_date"]).sort_values("_date")
    if df.empty:
        return None
    return df.iloc[-1].to_dict()


def recovery_score(wellness: pd.DataFrame) -> float:
    latest = latest_wellness(wellness)
    if latest is None:
        return 50.0

    pain_morning = float(latest.get("pain_morning", 0) or 0)
    pain_stairs = float(latest.get("pain_stairs", 0) or 0)
    pain_squat = float(latest.get("pain_squat", 0) or 0)
    pain_after = float(latest.get("pain_after", 0) or 0)
    sleep_hours = float(latest.get("sleep_hours", 7) or 7)
    energy = float(latest.get("energy", 5) or 5)
    stress = float(latest.get("stress", 5) or 5)

    score = (
        100
        - pain_morning * 5
        - pain_stairs * 7
        - pain_squat * 6
        - pain_after * 3
        + (sleep_hours - 7) * 8
        + energy * 3
        - stress * 3
    )
    return round(clamp(score, 0, 100), 1)


def readiness_emoji(score: float) -> str:
    if score >= 75:
        return "🟢"
    if score >= 50:
        return "🟡"
    return "🔴"


def training_stimulus(training: pd.DataFrame, today=None) -> pd.Series:
    if today is None:
        today = pd.Timestamp(date.today())

    stim = pd.Series(0.0, index=DIMENSION_IDS)

    if training is None or training.empty:
        return stim

    df = training.copy()
    df["_date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["_date"])

    for _, row in df.iterrows():
        age_days = max(0, (today - row["_date"]).days)
        # 28-day half-ish life: recent training matters more, old training still has small effect
        weight = np.exp(-age_days / 28)
        duration = float(row.get("duration_min", 0) or 0)
        intensity = float(row.get("intensity", 0) or 0)
        base = (duration / 30.0) * (intensity / 10.0) * weight

        for dim in DIMENSION_IDS:
            effect = float(row.get(f"effect_{dim}", 0) or 0)
            stim[dim] += base * effect

    return stim


def fatigue_penalties(training: pd.DataFrame, wellness: pd.DataFrame, today=None) -> pd.Series:
    if today is None:
        today = pd.Timestamp(date.today())

    penalty = pd.Series(0.0, index=DIMENSION_IDS)

    if training is not None and not training.empty:
        df = training.copy()
        df["_date"] = pd.to_datetime(df["date"], errors="coerce")
        df = df.dropna(subset=["_date"])
        recent = df[(today - df["_date"]).dt.days.between(0, 6)]
        if not recent.empty:
            knee_load = ((recent["duration_min"].astype(float) / 30) * (recent["knee_load"].astype(float) / 10)).sum()
            wrist_load = ((recent["duration_min"].astype(float) / 30) * (recent["wrist_load"].astype(float) / 10)).sum()
            ankle_load = ((recent["duration_min"].astype(float) / 30) * (recent["ankle_load"].astype(float) / 10)).sum()
            penalty["knee_health"] += min(0.7, max(0, knee_load - 2.5) * 0.12)
            penalty["tendon_capacity"] += min(0.5, max(0, knee_load - 2.5) * 0.08)
            penalty["power"] += min(0.8, max(0, knee_load - 2.0) * 0.15)
            penalty["wrists"] += min(0.6, max(0, wrist_load - 3.0) * 0.10)
            penalty["rings_strength"] += min(0.4, max(0, wrist_load - 3.5) * 0.06)
            penalty["ankles"] += min(0.5, max(0, ankle_load - 3.0) * 0.10)

    latest = latest_wellness(wellness)
    if latest:
        pain_morning = float(latest.get("pain_morning", 0) or 0)
        pain_stairs = float(latest.get("pain_stairs", 0) or 0)
        pain_squat = float(latest.get("pain_squat", 0) or 0)
        pain_after = float(latest.get("pain_after", 0) or 0)
        avg_knee_pain = np.mean([pain_morning, pain_stairs, pain_squat, pain_after])
        knee_pain_penalty = min(1.5, max(0, avg_knee_pain - 2) * 0.35)
        penalty["knee_health"] += knee_pain_penalty
        penalty["tendon_capacity"] += knee_pain_penalty * 0.6
        penalty["power"] += knee_pain_penalty * 0.8

    return penalty


def dimension_scores(baselines: pd.DataFrame, training: pd.DataFrame, wellness: pd.DataFrame) -> pd.DataFrame:
    stim = training_stimulus(training)
    penalties = fatigue_penalties(training, wellness)

    rows = []
    for dim in DIMENSION_IDS:
        base_row = baselines[baselines["dimension_id"] == dim]
        if base_row.empty:
            baseline = 0.0
            manual_adjust = 0.0
            notes = ""
        else:
            baseline = float(base_row.iloc[0].get("baseline_level", 0) or 0)
            manual_adjust = float(base_row.iloc[0].get("manual_adjust", 0) or 0)
            notes = base_row.iloc[0].get("notes", "")

        # 1 level ~= 12 weighted stimulus points; cap adaptation so sliders remain meaningful
        adaptation = min(1.25, stim[dim] / 12.0)
        penalty = penalties[dim]
        current = clamp(baseline + manual_adjust + adaptation - penalty, -1, 5)

        rows.append({
            "dimension_id": dim,
            "dimension": DIMENSION_NAMES[dim],
            "baseline": round(baseline, 2),
            "manual_adjust": round(manual_adjust, 2),
            "adaptation": round(adaptation, 2),
            "penalty": round(penalty, 2),
            "current_level": round(current, 2),
            "status": level_label(current),
            "progress_pct": round((current + 1) / 6 * 100, 1),
            "notes": notes,
        })
    return pd.DataFrame(rows)


def daily_recommendations(status: str):
    if status == "RED":
        return {
            "do": [
                "Physio genou complète",
                "Leg extension iso / Spanish squat sans flare-up",
                "Self-massage + respiration",
                "Mobilité hanches/dos",
                "Rings très basiques si poignets OK",
                "Core au sol sans douleur",
            ],
            "avoid": [
                "Bootcamp",
                "Obstacles / parkour",
                "Front flips",
                "Sauts / réceptions",
                "Squats profonds douloureux",
            ],
        }
    if status == "ORANGE":
        return {
            "do": [
                "Physio genou",
                "Équilibre / aérien si poignets OK",
                "Rings force contrôlée",
                "Flexibilité active",
                "Core",
            ],
            "avoid": [
                "Impacts répétés",
                "Course intense",
                "Réceptions lourdes",
                "Volume jambes non planifié",
            ],
        }
    return {
        "do": [
            "Physio",
            "Force contrôlée jambes",
            "Cours technique adapté",
            "Mobilité active",
            "Core / Rings",
        ],
        "avoid": [
            "Max effort non planifié",
            "Ajouter trop de volume",
            "Ignorer une douleur qui augmente le lendemain",
        ],
    }


def recovery_series(wellness: pd.DataFrame) -> pd.DataFrame:
    if wellness is None or wellness.empty:
        return pd.DataFrame(columns=["date", "recovery_score"])
    rows = []
    for _, row in wellness.iterrows():
        one = pd.DataFrame([row])
        rows.append({"date": row["date"], "recovery_score": recovery_score(one)})
    return pd.DataFrame(rows)
