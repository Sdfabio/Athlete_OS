
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"

DIMENSIONS = [
    {"id": "knee_health", "name": "Genou / Patella", "default": -0.5},
    {"id": "tendon_capacity", "name": "Tendons", "default": 0.0},
    {"id": "wrists", "name": "Poignets", "default": 1.5},
    {"id": "ankles", "name": "Chevilles", "default": 0.5},
    {"id": "hips_mobility", "name": "Hanches", "default": 1.0},
    {"id": "shoulder_flex", "name": "Épaules flex", "default": 0.8},
    {"id": "bridge_spine", "name": "Dos / Pont", "default": 0.8},
    {"id": "core", "name": "Core / Abdos", "default": 1.2},
    {"id": "rings_strength", "name": "Rings", "default": 0.5},
    {"id": "balance", "name": "Équilibre", "default": 1.8},
    {"id": "global_strength", "name": "Force générale", "default": 1.2},
    {"id": "power", "name": "Puissance jambes", "default": -1.0},
    {"id": "flexibility", "name": "Flexibilité globale", "default": 1.0},
]

DIMENSION_IDS = [d["id"] for d in DIMENSIONS]
DIMENSION_NAMES = {d["id"]: d["name"] for d in DIMENSIONS}
EFFECT_COLUMNS = [f"effect_{d}" for d in DIMENSION_IDS]

LEVEL_LABELS = [
    (-1, "Blessé / ne pas charger"),
    (0, "Rééducation"),
    (1, "Fondations"),
    (2, "Intermédiaire"),
    (3, "Avancé"),
    (4, "Élite"),
    (5, "Pro"),
]

CATEGORIES = [
    "Physio tendon",
    "Self-massage",
    "Mobilité active",
    "Flexibilité",
    "Rings",
    "Core",
    "Force haut",
    "Force bas",
    "Poignets",
    "Chevilles",
    "Cours Paragym",
    "Technique",
    "Récupération",
]
