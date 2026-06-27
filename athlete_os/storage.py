
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import pandas as pd

from athlete_os.config import DATA_DIR, DIMENSIONS, EFFECT_COLUMNS
from athlete_os.seed import DEFAULT_EXERCISES

WELLNESS_COLUMNS = [
    "date",
    "pain_morning",
    "pain_stairs",
    "pain_squat",
    "pain_after",
    "sleep_hours",
    "energy",
    "stress",
    "notes",
]

TRAINING_COLUMNS = [
    "timestamp",
    "date",
    "exercise_name",
    "category",
    "body_region",
    "duration_min",
    "intensity",
    "knee_load",
    "wrist_load",
    "ankle_load",
    "sets",
    "reps",
    "pain_before",
    "pain_after",
    "notes",
] + EFFECT_COLUMNS

EXERCISE_COLUMNS = [
    "exercise_name",
    "category",
    "body_region",
    "default_dose",
    "goal",
    "default_intensity",
    "knee_load",
    "wrist_load",
    "ankle_load",
    "phase_min",
    "equipment",
    "notes",
] + EFFECT_COLUMNS

BASELINE_COLUMNS = ["dimension_id", "dimension_name", "baseline_level", "manual_adjust", "notes"]


def data_path(filename: str) -> Path:
    return DATA_DIR / filename


def ensure_data_files() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if not data_path("wellness_log.csv").exists():
        pd.DataFrame(columns=WELLNESS_COLUMNS).to_csv(data_path("wellness_log.csv"), index=False)

    if not data_path("training_log.csv").exists():
        pd.DataFrame(columns=TRAINING_COLUMNS).to_csv(data_path("training_log.csv"), index=False)

    if not data_path("exercise_library.csv").exists():
        df = pd.DataFrame(DEFAULT_EXERCISES)
        for col in EXERCISE_COLUMNS:
            if col not in df.columns:
                df[col] = 0.0 if col.startswith("effect_") else ""
        df[EXERCISE_COLUMNS].to_csv(data_path("exercise_library.csv"), index=False)

    if not data_path("dimension_baselines.csv").exists():
        rows = []
        for d in DIMENSIONS:
            rows.append({
                "dimension_id": d["id"],
                "dimension_name": d["name"],
                "baseline_level": d["default"],
                "manual_adjust": 0.0,
                "notes": "",
            })
        pd.DataFrame(rows, columns=BASELINE_COLUMNS).to_csv(data_path("dimension_baselines.csv"), index=False)


def read_csv_safe(filename: str, columns: list[str]) -> pd.DataFrame:
    path = data_path(filename)
    if not path.exists():
        return pd.DataFrame(columns=columns)
    df = pd.read_csv(path)
    for col in columns:
        if col not in df.columns:
            df[col] = None
    return df[columns]


def load_wellness() -> pd.DataFrame:
    df = read_csv_safe("wellness_log.csv", WELLNESS_COLUMNS)
    if not df.empty:
        df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date.astype("string")
    return df


def load_training() -> pd.DataFrame:
    df = read_csv_safe("training_log.csv", TRAINING_COLUMNS)
    if not df.empty:
        df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date.astype("string")
    return df


def load_exercises() -> pd.DataFrame:
    return read_csv_safe("exercise_library.csv", EXERCISE_COLUMNS)


def load_baselines() -> pd.DataFrame:
    return read_csv_safe("dimension_baselines.csv", BASELINE_COLUMNS)


def save_wellness_entry(entry: dict) -> None:
    df = load_wellness()
    entry = {col: entry.get(col, "") for col in WELLNESS_COLUMNS}

    # one wellness record per date: update existing date or append
    if not df.empty and str(entry["date"]) in set(df["date"].astype(str)):
        idx = df.index[df["date"].astype(str) == str(entry["date"])][0]
        for col, val in entry.items():
            df.loc[idx, col] = val
    else:
        df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)

    df.to_csv(data_path("wellness_log.csv"), index=False)


def append_training_entry(entry: dict) -> None:
    df = load_training()
    entry = {col: entry.get(col, 0.0 if col.startswith("effect_") else "") for col in TRAINING_COLUMNS}
    if not entry["timestamp"]:
        entry["timestamp"] = datetime.now().isoformat(timespec="seconds")
    df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
    df.to_csv(data_path("training_log.csv"), index=False)


def save_exercise_library(df: pd.DataFrame) -> None:
    for col in EXERCISE_COLUMNS:
        if col not in df.columns:
            df[col] = 0.0 if col.startswith("effect_") else ""
    df[EXERCISE_COLUMNS].to_csv(data_path("exercise_library.csv"), index=False)


def add_exercise(row: dict) -> None:
    df = load_exercises()
    row = {col: row.get(col, 0.0 if col.startswith("effect_") else "") for col in EXERCISE_COLUMNS}
    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    save_exercise_library(df)


def save_baselines(df: pd.DataFrame) -> None:
    for col in BASELINE_COLUMNS:
        if col not in df.columns:
            df[col] = ""
    df[BASELINE_COLUMNS].to_csv(data_path("dimension_baselines.csv"), index=False)
