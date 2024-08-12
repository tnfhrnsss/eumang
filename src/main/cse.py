import requests
import os
import json

with open('env.json') as f:
    config = json.load(f)


def google_search(query, num_results=10):
    api_key = config['api_key']
    cse_id = config['cse_id']
    query = config['model.en.search_text']
    url = f"https://customsearch.googleapis.com/customsearch/v1?q={query}&key={api_key}&cx={cse_id}&searchType=image&num={num_results}&cr=countryUS" # countryKR
    response = requests.get(url, verify=False)
    results = response.json()
    return results.get('items', [])


def download_image(url, save_dir, image_name):
    try:
        response = requests.get(url, stream=True, verify=False)
        if response.status_code == 200:
            with open(os.path.join(save_dir, image_name), 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
    except Exception as e:
        print(f"예상치 못한 오류 발생: {e}")



def fetch_phishing_images(query):
    save_dir = config['save_dir']
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    images = google_search(query)
    for i, image in enumerate(images):
        image_url = image['link']
        image_name = f"phishing_{i}.jpg"
        download_image(image_url, save_dir, image_name)


# 예시 사용법
query = '보이스 피싱 문자'

fetch_phishing_images(query)
