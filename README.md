
# Athlete OS v2

Application Streamlit modulaire pour suivre :

- douleurs du tendon patellaire / genou
- sommeil, énergie, stress, récupération
- entraînements, cours, physio, massages, mobilité, force
- progression par dimension de -1 à 5
- radar chart des qualités physiques
- programme hebdomadaire selon ton horaire Paragym

## Lancer dans VS Code

```bash
cd athlete_os_v2
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Où sont les données ?

Les fichiers CSV sont créés automatiquement dans `data/` :

- `wellness_log.csv` : douleur, sommeil, énergie, stress
- `training_log.csv` : exercices / cours faits
- `exercise_library.csv` : bibliothèque d'exercices modifiable
- `dimension_baselines.csv` : niveaux de base par dimension

## Échelle des dimensions

- `-1` : blessé / ne pas charger
- `0` : rééducation
- `1` : fondations
- `2` : intermédiaire
- `3` : avancé
- `4` : élite
- `5` : pro
