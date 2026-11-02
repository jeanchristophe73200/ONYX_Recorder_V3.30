# ONYX V3.30

Enregistreur acoustique pour macOS. Il enregistre le son en FLAC, relève les niveaux sonores fournis par REW (Room EQ Wizard) et la météo locale, et écrit un journal CSV horodaté.

Ce dépôt publie l'état du logiciel sur la machine d'enregistrement au 2 novembre 2026 (affichage « ONYX V3.30 »). C'est un outil artisanal, pas un produit fini : voir « Limites connues ».

## Ce que fait ONYX

- Audio : FLAC mono, 48 kHz, un fichier par heure (rotation aux heures pleines, nom du type `2026-03-02_07h57_Audio.flac`). Le code ne précise pas le format : les fichiers sont en 16 bits. Sur les archives, le premier fichier de chacune des 13 sessions a été vérifié : 12 sont en 16 bits, la session du 17 décembre 2025 est en 24 bits.
- Journal CSV : une ligne environ toutes les 3 secondes (séparateur « ; », virgule décimale) : `ts;h;dBA;dBC;20Hz;…`, puis température, humidité, vent, pression, pluie, une note d'événement et `Audio_Ref` (nom du fichier audio en cours).
- Niveaux : dBA, dBC et spectre lus via l'API locale de REW (port 4735). REW doit être lancé. L'étalonnage du microphone se fait dans REW ; ONYX ne le vérifie pas. Le spectre est repris des points RTA de REW par correspondance de fréquence à ±10 % près.
- Météo : Open-Meteo (coordonnées saisies à l'écran de configuration).
- Telegram : notifications (arrêt de mission, événements) et saisie d'événements à distance.
- Horodatage : horloge du Mac, sans vérification de sa synchronisation.

## Installation (macOS, Python 3.11)

1. `bash install_onyx.sh` : crée l'environnement virtuel et installe les dépendances de `requirements.txt`. Les versions exactes de la machine d'enregistrement sont dans `requirements_freeze.txt` (`pip install -r requirements_freeze.txt` pour les reproduire).
2. Copier `onyx_settings.example.py` en `onyx_settings.py`, puis remplacer les valeurs fictives (token et identifiant de chat Telegram, disque, micro). Ne jamais publier `onyx_settings.py` : il est dans `.gitignore`.
3. Activer le serveur API de REW, puis lancer `LANCER_ONYX.command` (créé par l'installateur) ou `source venv/bin/activate && python onyx_main.py`.

## Règle d'exploitation

En mode continu : 30 jours maximum par lancement, puis arrêt et relance. Cette règle de prudence vient de la lecture du code : la fonction d'enregistrement se rappelle elle-même à chaque heure, et Python limite normalement ce type d'appels à environ 1 000, soit environ 41 jours. Le code n'impose pas cette limite et elle n'a pas été mesurée.

## Limites connues

- Aucune signature ni aucun hash des fichiers produits : le logiciel ne scelle rien.
- La file audio n'est pas bornée ; l'arrêt du thread d'enregistrement n'est pas signalé à l'écran.
- Nombreux `except: pass` : des erreurs peuvent passer sans trace.
- Si REW est indisponible, la mesure est enregistrée comme 0,0 dBA, sans indicateur.
- Les alertes de saturation du micro sont seulement affichées dans le Terminal.
- 5 Go d'espace disque minimum sur le disque d'enregistrement (vérifié au démarrage uniquement).
- Aucun test automatique ; l'installateur n'a pas été retesté pour cette publication.

## Autres documents

- `README_TECH.md` : notes techniques.
- `VISION.md` : vision du projet.

## Note de publication

`onyx_main.py`, `onyx_audio.py`, `onyx_rew.py`, `onyx_telegram.py` et `onyx_log.py` sont identiques à l'original (empreintes dans `SHA256SUMS_V3.30_ORIGINAL.txt`). Différences :

- `onyx_weather.py` (lignes 7-8) : coordonnées par défaut remplacées par 0.0.
- `onyx_gui.py` (ligne 198) : coordonnées préremplies remplacées par une valeur d'exemple.
- `install_onyx.sh` : numéro de version affiché corrigé (V3.30).
- `onyx_settings.py` (réglages réels, avec secrets) n'est pas publié ; remplacé par `onyx_settings.example.py`.
- `VISION.md` : une phrase promettant de « garantir l'intégrité des données » a été reformulée.
- `SHA256SUMS.txt` : empreintes des fichiers de cette publication.

`build_release.sh`, `install.sh`, `requirements.txt` et `test_api_rew.py` viennent de l'ancien dépôt et n'ont pas été revus en détail. Les CSV des sessions archivées portent l'en-tête « ONYX V3.2 », texte écrit en dur dans le code : ils ne permettent pas de dater le passage à la V3.30. Dates de dernière modification des fichiers de code sur la machine d'enregistrement : 16 au 19 décembre 2025 (onyx_audio.py le 18 décembre à 13h29, onyx_main.py le 19 décembre à 21h46). Les 12 sessions archivées en 16 bits ont démarré après (la plus ancienne le 19 décembre à 22h00). Ces dates de fichiers sont un indice, pas une preuve.
