import requests
from random import choice
from time import sleep
from bs4 import BeautifulSoup
import json

# List of user-agent strings
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
    # Add more user-agent strings as needed
]

# Session object to handle cookies
session = requests.Session()

# Function to make a GET request with random user agent
def make_request(url):
    user_agent = choice(user_agents)
    headers = {
        'User-Agent': user_agent,
        'Referer': 'https://www.rudaw.net/',
        # Add more headers if needed
    }
    response = session.get(url, headers=headers)
    return response

# Function to parse the HTML and extract desired information
def parse_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    result = []

    # Extracting a tags from class main__thumb-title
    thumb_titles = soup.find_all('h4', class_='main__thumb-title')
    if thumb_titles:
        for thumb_title in thumb_titles:
            links = thumb_title.find_all('a')
            for link in links:
                title = link.get_text(strip=True)
                href = link.get('href')
                result.append({'title': title, 'href': href})

    # Extracting a tags from class main__atf-title
    atf_titles = soup.find_all('h2', class_='main__atf-title')
    if atf_titles:
        for atf_title in atf_titles:
            links = atf_title.find_all('a')
            for link in links:
                title = link.get_text(strip=True)
                href = link.get('href')
                result.append({'title': title, 'href': href})

    return result

# Example usage
url = 'https://www.rudaw.net/sorani/kurdistan'
response = make_request(url)

if response.status_code == 200:
    result = parse_html(response.text)
    json_result = json.dumps(result, ensure_ascii=False, indent=4)
    print(json_result)
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")

# Add random delay between requests
sleep(choice(range(1, 5)))
