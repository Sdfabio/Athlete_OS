
from athlete_os.config import DIMENSION_IDS, EFFECT_COLUMNS

def blank_effects():
    return {f"effect_{d}": 0.0 for d in DIMENSION_IDS}

def ex(
    name,
    category,
    body_region,
    dose,
    goal,
    intensity=5,
    knee_load=0,
    wrist_load=0,
    ankle_load=0,
    phase_min=-1,
    effects=None,
    equipment="",
    notes="",
):
    row = {
        "exercise_name": name,
        "category": category,
        "body_region": body_region,
        "default_dose": dose,
        "goal": goal,
        "default_intensity": intensity,
        "knee_load": knee_load,
        "wrist_load": wrist_load,
        "ankle_load": ankle_load,
        "phase_min": phase_min,
        "equipment": equipment,
        "notes": notes,
    }
    row.update(blank_effects())
    if effects:
        for k, v in effects.items():
            row[f"effect_{k}"] = float(v)
    return row

DEFAULT_EXERCISES = [
    # Physio tendon / knee
    ex("Spanish squat isométrique", "Physio tendon", "Genou / quadriceps", "5 x 45-60s", "Analgésie + charge tendon", 5, 2, 0, 0, -1, {"knee_health": 3, "tendon_capacity": 4, "global_strength": 1}),
    ex("Leg extension isométrique", "Physio tendon", "Genou / quadriceps", "5 x 30-45s", "Calmer la douleur + recruter quadriceps", 5, 2, 0, 0, -1, {"knee_health": 4, "tendon_capacity": 4, "global_strength": 1}),
    ex("Leg extension heavy slow", "Physio tendon", "Genou / quadriceps", "3-4 x 8-12, tempo 3-0-3", "Heavy slow resistance du tendon", 7, 4, 0, 0, 0, {"knee_health": 4, "tendon_capacity": 5, "global_strength": 2}),
    ex("Step-down bas contrôlé", "Physio tendon", "Genou", "3 x 8-10 lent", "Contrôle excentrique sans impact", 5, 3, 0, 1, 0, {"knee_health": 3, "tendon_capacity": 3, "balance": 1}),
    ex("Reverse step-up", "Physio tendon", "Genou / quad", "3 x 10", "Quad + contrôle genou", 5, 3, 0, 1, 0, {"knee_health": 3, "tendon_capacity": 3}),
    ex("Hip thrust / glute bridge", "Force bas", "Fessiers", "3 x 12-15", "Fessiers puissants, décharger genou", 6, 1, 0, 0, -1, {"global_strength": 3, "power": 1, "knee_health": 1}),
    ex("Soleus raise genou plié", "Chevilles", "Mollets / tendon Achille", "3 x 15-20", "Soleus + tendon Achille", 5, 1, 0, 3, -1, {"ankles": 4, "tendon_capacity": 3}),
    ex("Standing calf raise", "Chevilles", "Mollets", "3 x 12-20", "Chevilles fortes", 5, 1, 0, 3, -1, {"ankles": 4, "tendon_capacity": 2, "power": 1}),
    ex("Tibialis raise", "Chevilles", "Tibialis", "3 x 20", "Stabilité cheville/genou", 4, 1, 0, 2, -1, {"ankles": 4, "knee_health": 1}),

    # Self massage
    ex("Foam roll quadriceps", "Self-massage", "Quad", "1-2 min/side", "Diminuer tension cuisse", 2, 0, 0, 0, -1, {"knee_health": 1, "flexibility": 1}),
    ex("Foam roll TFL / fessiers", "Self-massage", "Hanche", "1-2 min/side", "Hanche/genou", 2, 0, 0, 0, -1, {"hips_mobility": 1, "knee_health": 1}),
    ex("Foam roll adducteurs", "Self-massage", "Adducteurs", "1-2 min/side", "Middle split + genou", 2, 0, 0, 0, -1, {"hips_mobility": 1, "flexibility": 1}),
    ex("Foam roll mollets / soleus", "Self-massage", "Mollets", "1-2 min/side", "Cheville + genou", 2, 0, 0, 0, -1, {"ankles": 1, "tendon_capacity": 1}),
    ex("Massage balle pied", "Self-massage", "Pied", "1-2 min/side", "Chaîne d'appui", 2, 0, 0, 0, -1, {"ankles": 1}),
    ex("Massage manuel autour rotule", "Self-massage", "Genou", "2-3 min doux", "Soulager sans écraser tendon irrité", 2, 0, 0, 0, -1, {"knee_health": 1}),
    ex("Respiration lente récupération", "Récupération", "Système nerveux", "3-5 min", "Faire descendre le stress", 1, 0, 0, 0, -1, {}),

    # Mobility/flexibility
    ex("Active Hip Internal Rotation Lift-off", "Mobilité active", "Hanches", "2-3 x 8/side", "Rotation interne active", 4, 0, 0, 0, -1, {"hips_mobility": 5, "flexibility": 2}),
    ex("90/90 transitions", "Mobilité active", "Hanches", "2-3 min", "Contrôle rotation hanche", 4, 0, 0, 0, -1, {"hips_mobility": 5, "flexibility": 2}),
    ex("Hip CARs", "Mobilité active", "Hanches", "3 lentes/side", "Contrôle articulaire", 3, 0, 0, 0, -1, {"hips_mobility": 4}),
    ex("Hip Airplane assisté", "Mobilité active", "Hanches", "2 x 5/side", "Stabilité hanche", 5, 1, 0, 1, 0, {"hips_mobility": 4, "balance": 2}),
    ex("Couch stretch", "Flexibilité", "Psoas / quads", "2 x 60s/side", "Front split + extension hanche", 3, 1, 0, 0, -1, {"flexibility": 3, "hips_mobility": 2, "knee_health": 1}),
    ex("Front split isométrique doux", "Flexibilité", "Hanches / ischios", "3 x 30-45s", "Split actif", 4, 1, 0, 0, -1, {"flexibility": 5, "hips_mobility": 3}),
    ex("Frog stretch", "Flexibilité", "Adducteurs", "2 x 60s", "Middle split", 3, 0, 0, 0, -1, {"flexibility": 4, "hips_mobility": 3}),
    ex("Pancake good morning", "Flexibilité", "Adducteurs / ischios", "3 x 8 lent", "Souplesse active + force", 5, 0, 0, 0, -1, {"flexibility": 4, "hips_mobility": 3, "global_strength": 1}),
    ex("Thoracic extension foam roller", "Mobilité active", "Thoracique", "2 min", "Pont/dos haut", 3, 0, 0, 0, -1, {"bridge_spine": 3, "shoulder_flex": 1}),
    ex("Bridge hold / wall bridge", "Flexibilité", "Dos / épaules", "3 x 20-40s", "Pont actif", 5, 0, 2, 0, -1, {"bridge_spine": 5, "shoulder_flex": 3, "flexibility": 2}),
    ex("PVC dislocates", "Mobilité active", "Épaules", "2 x 15", "Amplitude épaules", 3, 0, 1, 0, -1, {"shoulder_flex": 4, "flexibility": 1}),
    ex("German hang progression", "Mobilité active", "Épaules / rings", "3 x 10-30s", "Extension épaules + rings", 5, 0, 3, 0, -1, {"shoulder_flex": 4, "rings_strength": 2, "tendon_capacity": 1}),

    # Rings / core / strength
    ex("Ring support hold", "Rings", "Haut du corps", "4 x 10-30s", "Base rings", 6, 0, 4, 0, -1, {"rings_strength": 5, "wrists": 2, "global_strength": 2}),
    ex("False grip hang", "Rings", "Poignets / tirage", "4 x 10-20s", "False grip", 6, 0, 4, 0, -1, {"rings_strength": 4, "wrists": 4, "global_strength": 1}),
    ex("Ring push-up", "Rings", "Push", "3 x 6-12", "Stabilité épaules", 6, 0, 4, 0, -1, {"rings_strength": 4, "global_strength": 2, "wrists": 2}),
    ex("Ring dip progression", "Rings", "Push", "3 x 3-8", "Force rings", 7, 0, 4, 0, 0, {"rings_strength": 5, "global_strength": 3}),
    ex("Planche lean", "Force haut", "Épaules / poignets", "4 x 10-20s", "Préparation planche", 7, 0, 5, 0, -1, {"wrists": 4, "global_strength": 3, "rings_strength": 2}),
    ex("Pseudo planche push-up", "Force haut", "Push", "3 x 5-10", "Planche force", 7, 0, 5, 0, 0, {"wrists": 4, "global_strength": 4, "rings_strength": 2}),
    ex("Scap pull-up", "Force haut", "Scapulas", "3 x 8-12", "Scapula contrôle", 5, 0, 1, 0, -1, {"global_strength": 2, "rings_strength": 2}),
    ex("Ring row / pull-up", "Force haut", "Dos", "4 x 6-10", "Dos puissant", 7, 0, 2, 0, -1, {"global_strength": 4, "rings_strength": 3}),
    ex("Hollow hold", "Core", "Core", "4 x 30-45s", "Base abdos", 5, 0, 0, 0, -1, {"core": 4}),
    ex("L-sit tuck / parallettes", "Core", "Core / compression", "5 x 10-20s", "Compression", 6, 0, 3, 0, -1, {"core": 5, "wrists": 2, "hips_mobility": 1}),
    ex("Dragon flag negative", "Core", "Core", "3 x 3-5", "Dragon flag", 8, 0, 0, 0, 0, {"core": 5, "global_strength": 2}),
    ex("Human flag prep side plank", "Core", "Obliques / épaules", "3 x 20-30s", "Drapeau", 7, 0, 2, 0, 0, {"core": 4, "global_strength": 2, "rings_strength": 1}),
    ex("Mushroom / bucket circles", "Technique", "Champignon", "10-15 min", "Pommel horse", 5, 0, 4, 0, -1, {"wrists": 3, "balance": 3, "core": 2}),

    # Courses
    ex("Cours Équilibre", "Cours Paragym", "Haut du corps / poignets", "60 min", "Équilibre, contrôle, poignets", 6, 0, 6, 1, -1, {"balance": 4, "wrists": 3, "core": 2}),
    ex("Cours Aérien / Hammock / Silks", "Cours Paragym", "Haut du corps", "60 min", "Grip, épaules, core", 6, 0, 5, 0, -1, {"rings_strength": 2, "global_strength": 2, "core": 2, "shoulder_flex": 1}),
    ex("Kick ass bootcamp", "Cours Paragym", "Full body", "60-90 min", "Force/cardio/endurance", 8, 6, 3, 4, 1, {"global_strength": 3, "tendon_capacity": 1, "power": 1}),
    ex("Obstacles / Parkour", "Cours Paragym", "Full body / genou", "60-120 min", "Parkour, coordination", 7, 7, 4, 5, 2, {"balance": 3, "power": 3, "ankles": 2}),
    ex("Acro basics", "Cours Paragym", "Acro", "60 min", "Back handspring / bases", 6, 4, 4, 3, 1, {"balance": 3, "power": 1, "wrists": 2}),
    ex("Front flips", "Cours Paragym", "Acro / genou", "60 min", "Front flips", 8, 8, 3, 5, 3, {"power": 4, "balance": 2, "ankles": 2}),
]
