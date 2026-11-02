# ONYX V3.30 – notes techniques

## Prérequis
- macOS, Python 3, REW (Room EQ Wizard) lancé avec son API locale activée (port 4735).
- Microphone USB calibré ou micro interne.

## Fichiers
- `onyx_main.py` : programme principal.
- `onyx_audio.py` : capture et écriture FLAC.
- `onyx_rew.py` : lecture des niveaux et du spectre via l'API REW.
- `onyx_weather.py` : météo Open-Meteo.
- `onyx_telegram.py` : alertes Telegram.
- `onyx_gui.py` : interface.
- `onyx_log.py` : journal.
- `onyx_settings.example.py` : modèle de réglages (à copier en `onyx_settings.py`).

## Sorties
- Fichiers FLAC (mono, 48 kHz, 16 bits), un par heure.
- Fichier CSV toutes les 3 s, avec la colonne `Audio_Ref`.

## Limites
Voir la section « Limites connues » de `README.md`.
