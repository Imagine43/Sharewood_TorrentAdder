# Script de Téléchargement de Torrents Sharewood

## Description

Ce script Python permet de télécharger des fichiers torrent depuis Sharewood.tv en utilisant l'API de Sharewood et un mécanisme d'authentification par cookie. Il extrait des données basées sur des mots-clés définis dans un fichier JSON, vérifie les torrents disponibles, et télécharge les fichiers pertinents. De plus, il envoie des notifications via Telegram lorsqu'un téléchargement est trouvé.

## Fonctionnalités

1. **Récupération de données depuis l'API Sharewood**
   - **Fonction**: `fetch_data_from_api`
   - **Description**: Récupère les données de torrents depuis l'API de Sharewood en utilisant l'URL de base, la clé API, et l'endpoint spécifiés.

2. **Extraction des torrents pertinents**
   - **Fonction**: `extract_id_slug`
   - **Description**: Extrait les torrents correspondant aux mots-clés spécifiés depuis les données API.

3. **Gestion des cookies de connexion**
   - **Fonction**: `get_login_cookie`
   - **Description**: Gère le processus de connexion en récupérant un cookie d'authentification à l'aide des informations de connexion et du token CSRF.

4. **Téléchargement des fichiers torrents**
   - **Fonction**: `download_link`
   - **Description**: Télécharge les fichiers torrents et les enregistre dans le répertoire spécifié. Vérifie également la validité des fichiers téléchargés.

5. **Chargement des mots-clés et informations de connexion**
   - **Fonctions**: `load_keywords`, `load_login_info`
   - **Description**: Charge les mots-clés pour filtrer les torrents et les informations de connexion depuis des fichiers JSON.

6. **Envoi de notifications via Telegram**
   - **Fonction**: `send_telegram_message`
   - **Description**: Envoie un message de notification via Telegram lorsque des torrents pertinents sont trouvés et téléchargés.

7. **Traitement des téléchargements en parallèle**
   - **Fonction**: `process_download`
   - **Description**: Gère le téléchargement des torrents et l'envoi de notifications en utilisant un pool de threads pour paralléliser les tâches.

## Utilisation

1. **Configurer les fichiers JSON**
   - `filtres.json`: Contient les mots-clés pour filtrer les torrents. Exemple de format :
     ```json
     {
       "filtres": [
         {
           "titres": ["Titre exemple"],
           "qualite": ["Qualité exemple"],
           "dossier": "NomDossier",
           "filter_name": "NomFiltre"
         }
       ]
     }
     ```
   - `login.json`: Contient les informations de connexion pour obtenir les cookies. Exemple de format :
     ```json
     {
       "login_url": "https://www.sharewood.tv/login",
       "username": "votre_nom_utilisateur",
       "password": "votre_mot_de_passe"
     }
     ```

2. **Modifier les paramètres du script**
   - Remplacez `YOURDOWNLOAD_DIR` par le répertoire où vous souhaitez enregistrer les fichiers téléchargés.
   - Remplacez `YOURTELEGRAMAPI` et `YOURCHAT_ID` par les informations de votre bot Telegram.

3. **Exécuter le script**
   - Exécutez le script depuis la ligne de commande avec Python :
     ```bash
     python script.py
     ```

## Dépendances

- `requests`: Pour les requêtes HTTP.
- `beautifulsoup4`: Pour l'extraction du token CSRF.
- `concurrent.futures`: Pour la gestion des téléchargements en parallèle.

Installez les dépendances via pip :
```bash
pip install requests beautifulsoup4
