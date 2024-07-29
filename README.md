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

## Configuration de qBittorrent

Pour gérer les téléchargements automatiquement via des dossiers surveillés, vous devez configurer qBittorrent comme suit :

1. **Configurer les dossiers surveillés dans qBittorrent**
   - Ouvrez qBittorrent et allez dans `Options` > `Téléchargements`.
   - Sous `Dossiers surveillés`, ajoutez le répertoire où les fichiers torrents seront téléchargés par ce script.

2. **Vérifiez que le téléchargement automatique est activé**
   - Assurez-vous que l'option pour surveiller les dossiers et ajouter automatiquement les torrents est activée.

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
```

## Journalisation

Les logs d'exécution sont enregistrés dans le fichier `Sharewood_TorrentAdder_log.txt` situé dans le répertoire d'installation. Ce fichier contient des informations sur les actions effectuées par le script ainsi que les erreurs rencontrées pendant l'exécution. Les logs incluent :

- Les erreurs liées aux requêtes HTTP et à la connexion.
- Les informations sur les fichiers déjà téléchargés.
- Les messages de succès ou d'échec des opérations de téléchargement.
- Les notifications envoyées via Telegram.

Assurez-vous de vérifier ce fichier pour tout problème ou pour obtenir des détails sur le traitement des torrents.

## Notes

- **Vérification de la clé API et des informations de connexion** : Assurez-vous que votre clé API de Sharewood et les informations de connexion (nom d'utilisateur et mot de passe) sont corrects et valides avant d'exécuter le script.
- **Permissions d'écriture** : Vérifiez que le répertoire spécifié pour les téléchargements (`YOURDOWNLOAD_DIR`) possède les permissions nécessaires pour permettre l'écriture des fichiers.

## Futurs Développements

- **Filtrage par épisode** : Les prochaines versions du script prendront en charge le filtrage des torrents par épisode, permettant une gestion plus précise des téléchargements en fonction des épisodes spécifiques.

## Licence

Ce projet est sous licence [MIT](https://opensource.org/licenses/MIT). Voir le fichier [LICENSE](https://github.com/Imagine43/Sharewood_TorrentAdder/blob/main/LICENSE.txt) pour plus de détails.

**Avertissement :** Toute utilisation de ce logiciel est à vos propres risques. L'auteur ne saurait être tenu responsable des dommages directs ou indirects résultant de l'utilisation de ce logiciel. En utilisant ce logiciel, vous acceptez de dégager l'auteur de toute responsabilité.

## Donations

Si vous trouvez ce projet utile et souhaitez soutenir mon travail, vous pouvez faire un don via [Ko-fi](https://ko-fi.com/imagine43). Toute contribution est grandement appréciée et aide à maintenir le développement de ce projet.

Merci pour votre soutien !

++++++++++++++++++++++
ENGLISH VERSION
+++++++++++++++++++++++

# Sharewood Torrent Downloader Script

## Description

This Python script allows you to download torrent files from Sharewood.tv using the Sharewood API and a cookie-based authentication mechanism. It extracts data based on keywords defined in a JSON file, checks available torrents, and downloads relevant files. Additionally, it sends notifications via Telegram when a download is found.

## Features

1. **Fetching Data from Sharewood API**
   - **Function**: `fetch_data_from_api`
   - **Description**: Retrieves torrent data from the Sharewood API using the specified base URL, API key, and endpoint.

2. **Extracting Relevant Torrents**
   - **Function**: `extract_id_slug`
   - **Description**: Extracts torrents that match the specified keywords from the API data.

3. **Managing Login Cookies**
   - **Function**: `get_login_cookie`
   - **Description**: Manages the login process by retrieving an authentication cookie using the login information and CSRF token.

4. **Downloading Torrent Files**
   - **Function**: `download_link`
   - **Description**: Downloads torrent files and saves them to the specified directory. Also checks the validity of the downloaded files.

5. **Loading Keywords and Login Information**
   - **Functions**: `load_keywords`, `load_login_info`
   - **Description**: Loads keywords for filtering torrents and login information from JSON files.

6. **Sending Notifications via Telegram**
   - **Function**: `send_telegram_message`
   - **Description**: Sends a notification message via Telegram when relevant torrents are found and downloaded.

7. **Parallel Download Processing**
   - **Function**: `process_download`
   - **Description**: Manages the downloading of torrents and sending notifications using a thread pool to parallelize tasks.

## qBittorrent Configuration

To manage automatic downloads via monitored folders, you need to configure qBittorrent as follows:

1. **Configure Monitored Folders in qBittorrent**
   - Open qBittorrent and go to `Options` > `Downloads`.
   - Under `Monitored Folders`, add the directory where torrent files will be downloaded by this script.

2. **Ensure Automatic Downloading is Enabled**
   - Make sure the option to monitor folders and automatically add torrents is enabled.

## Usage

1. **Configure JSON Files**
   - `filtres.json`: Contains keywords to filter torrents. Example format:
     ```json
     {
       "filtres": [
         {
           "titres": ["Example Title"],
           "qualite": ["Example Quality"],
           "dossier": "FolderName",
           "filter_name": "FilterName"
         }
       ]
     }
     ```
   - `login.json`: Contains login information to obtain cookies. Example format:
     ```json
     {
       "login_url": "https://www.sharewood.tv/login",
       "username": "your_username",
       "password": "your_password"
     }
     ```

2. **Modify Script Settings**
   - Replace `YOURDOWNLOAD_DIR` with the directory where you want to save downloaded files.
   - Replace `YOURTELEGRAMAPI` and `YOURCHAT_ID` with your Telegram bot information.

3. **Run the Script**
   - Execute the script from the command line using Python:
     ```bash
     python script.py
     ```

## Dependencies

- `requests`: For HTTP requests.
- `beautifulsoup4`: For extracting the CSRF token.
- `concurrent.futures`: For managing parallel downloads.

Install the dependencies via pip:
```bash
pip install requests beautifulsoup4
```

## Logging

Execution logs are recorded in the `Sharewood_TorrentAdder_log.txt` file located in the installation directory. This file contains information about the actions performed by the script as well as errors encountered during execution. The logs include:

- Errors related to HTTP requests and login.
- Information about files that have already been downloaded.
- Success or failure messages for download operations.
- Notifications sent via Telegram.

Be sure to check this file for any issues or to get details about torrent processing.

## Notes

- **API Key and Login Information Verification**: Ensure that your Sharewood API key and login information (username and password) are correct and valid before running the script.
- **Write Permissions**: Verify that the directory specified for downloads (`YOURDOWNLOAD_DIR`) has the necessary permissions to allow file writing.

## Future Developments

- **Episode Filtering**: Future versions of the script will support filtering torrents by episode, allowing for more precise management of downloads based on specific episodes.

## License

This project is licensed under the [MIT](https://opensource.org/licenses/MIT) License. See the [LICENSE](https://github.com/Imagine43/Sharewood_TorrentAdder/blob/main/LICENSE.txt) file for details.

**Disclaimer:** Use of this software is at your own risk. The author cannot be held liable for any direct or indirect damages resulting from the use of this software. By using this software, you agree to hold the author harmless from any liability.

## Donations

If you find this project useful and would like to support my work, you can make a donation via [Ko-fi](https://ko-fi.com/imagine43). Any contribution is greatly appreciated and helps to support the development of this project.

Thank you for your support!
