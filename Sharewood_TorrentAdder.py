import requests
import json
import os
from bs4 import BeautifulSoup
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor


date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
log_buffer = []

def fetch_data_from_api(base_url, api_key, endpoint, params=None):
    url = f"{base_url}{api_key}{endpoint}"
    headers = {
        'Authorization': f'Bearer {api_key}'
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()  
        return response.json()  
    except requests.exceptions.RequestException as e:
        log_buffer.append(f'{date} - ERROR - An error occured : {e}.\n')
        return None

def extract_id_slug(data, keywords):
    extracted_data = []
    for item in data:
        slug = item.get('slug', '').lower()
        name = item.get('name', '').lower()
        
        for filter_item in keywords:
            titres = filter_item.get('titres', [])
            if isinstance(titres, str):
                titres = [titres]  
            titres = [titre.lower() for titre in titres]
            
            qualites = filter_item.get('qualite', [])
            if isinstance(qualites, str):
                qualites = [qualites]  
            qualites = [qualite.lower() for qualite in qualites]
            
            dossier = filter_item.get('dossier', 'default')
            filter_name = filter_item.get('filter_name', 'default')
            
            # Criteria verification
            if (any(titre in slug or titre in name for titre in titres) and
                all(qualite in slug or qualite in name for qualite in qualites)):
                extracted_data.append({
                    'id': item.get('id'),
                    'slug': slug,
                    'name': name,
                    'dossier': dossier,
                    'filter_name': filter_name
                })
                break
    return extracted_data

def get_login_cookie(login_url, username, password):
    session = requests.Session()
    try:
        # Étape 1 : Récupérer la page de connexion pour obtenir le token CSRF
        response = session.get(login_url)
        response.raise_for_status()
        
        # Extraire le token CSRF
        soup = BeautifulSoup(response.text, 'html.parser')
        csrf_token = soup.find('input', {'name': '_token'})['value']

        # Étape 2 : Utiliser le token CSRF dans la requête de connexion
        payload = {
            'username': username,
            'password': password,
            '_token': csrf_token
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = session.post(login_url, data=payload, headers=headers)
        response.raise_for_status()  # Vérifie si la requête a réussi
        return session.cookies.get_dict()
    except requests.exceptions.RequestException as e:
        log_buffer.append(f'{date} - ERROR - An error occured when trying to log in Sharewood : {e}.\n')
        return None

def download_link(slug, id, download_dir, cookies, subfolder):
    url = f"https://www.sharewood.tv/download/{slug}.{id}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'fr,fr-FR;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'
    }
    try:
        response = requests.get(url, headers=headers, cookies=cookies, allow_redirects=True)
        response.raise_for_status()  # Vérifie si la requête a réussi

        # Vérifier si le log est un log torrent en utilisant le type de contenu
        content_type = response.headers.get('Content-Type')
        if content_type != 'application/x-bittorrent':
            log_buffer.append(f'{date} - ERROR - New file constructed is not a valid torrent file.\n')
            return None

        # Obtenir le nom du log à partir de l'en-tête Content-Disposition
        content_disposition = response.headers.get('Content-Disposition')
        if content_disposition:
            filename = content_disposition.split('filename=')[1].strip('"')
        else:
            filename = f"{slug}.torrent"

        # Créer le dossier si nécessaire
        folder_path = os.path.join(download_dir, subfolder)
        os.makedirs(folder_path, exist_ok=True)

        filepath = os.path.join(folder_path, filename)

        if os.path.exists(filepath):
            log_buffer.append(f'{date} - INFO - File {filepath} already exists. Download skipped.\n')
            return None
        
        filepath = os.path.join(folder_path, filename)
        with open(filepath, 'wb') as file:
            file.write(response.content)
        return filepath
    except requests.exceptions.RequestException as e:
        log_buffer.append(f'{date} - ERROR - An error occured : {e}.\n')
        return None

def load_keywords(json_file):
    try:
        with open(json_file, 'r') as file:
            data = json.load(file)
            return data.get('filtres', [])
    except FileNotFoundError:
        log_buffer.append(f'{date} - ERROR - Login Json file not found : {json_file}\n')
        return []
    except json.JSONDecodeError:
        log_buffer.append(f'{date} - ERROR - Failed to decode json file : {json_file}.\n')
        return []

def load_login_info(json_file):
    try:
        with open(json_file, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        log_buffer.append(f'{date} - ERROR - Login Json file not found : {json_file}\n')
        return None
    except json.JSONDecodeError:
        log_buffer.append(f'{date} - ERROR - Failed to decode json file : {json_file}\n')
    
def send_telegram_message(bot_token, chat_id, message):

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()  # Verify if request is successful
        log_buffer.append(f'{date} - INFO - Telegram message sent successfully.\n')
    except requests.exceptions.RequestException as e:
        log_buffer.append(f'{date} - ERROR - Telegram message not sent : {e} \n')

def process_download(item, download_dir, cookies, bot_token, chat_id):
    slug = item['slug']
    id = item['id']
    subfolder = item['dossier']
    filter_name = item['filter_name']
    filepath = download_link(slug, id, download_dir, cookies, subfolder)
    if filepath:
        message = f"{date} - INFO - Download found! Downloading: {filter_name} (Filename: {slug}) now."
        send_telegram_message(bot_token, chat_id, message)
        log_buffer.append(f'{date} - INFO - Download found! Downloading {filter_name} (Filename: {slug})...\n')
    else:
        log_buffer.append(f'{date} - ERROR - No further actions needed for file : {slug}\n')

if __name__ == "__main__":
    base_url = "https://sharewood.tv/api"  
    endpoint = "/last-torrents"
    api_key = "/XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" # Sharewood API Key (don't forget the / before the api key)
    data = fetch_data_from_api(base_url, api_key, endpoint)


keywords_file = "filtres.json"
keywords = load_keywords(keywords_file)

download_dir = r"\\YOURDOWNLOAD_DIR"  # Download directory
os.makedirs(download_dir, exist_ok=True)

login_info_file = "login.json"
login_info = load_login_info(login_info_file)
if not login_info:
    with open(r'YOURINSTALL_DIR\Sharewood_TorrentAdder_log.txt', 'a') as log:
        log.write(f"{date} - ERROR - Failed to retrieve login informations.\n")
        exit(1)

login_url = login_info['login_url']
username = login_info['username']
password = login_info['password']


# Telegram informations
bot_token = "YOURTELEGRAMAPI"  # Telegram bot API ID here
chat_id = "YOURCHAT_ID"  # Telegram chat ID Here

cookies = get_login_cookie(login_url, username, password)
if not cookies:
    with open(r'YOURINSTALL_DIR\Sharewood_TorrentAdder_log.txt', 'a') as log:
        log.write(f"{date} - ERROR - Failed to produce new cookie.\n")
else:
    data = fetch_data_from_api(base_url, api_key, endpoint)
    if data:
        id_slug_data = extract_id_slug(data, keywords)
        if not id_slug_data:
            log_buffer.append(f"{date} - INFO - No new download found.\n")
        else:
            with ThreadPoolExecutor(max_workers=5) as executor:  # ThreadPoolExecutor to handle multiple downloads
                for item in id_slug_data:
                    executor.submit(process_download, item, download_dir, cookies, bot_token, chat_id)
    
# Writing logs
with open(r'YOURINSTALL_DIR\Sharewood_TorrentAdder_log.txt', 'a') as log:
        log.writelines(log_buffer)