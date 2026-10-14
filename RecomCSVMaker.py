from time import sleep
from urllib import response

from bs4 import BeautifulSoup
import requests
import sys

import requests


def print_response_info(response):
    print("--- URL Sent ---")
    print(response.request.url)

    print("\n--- Headers Sent ---")
    for key, value in response.request.headers.items():
        print(f"{key}: {value}")

    print("\n--- Payload Sent ---")
    print(response.request.body)

    print("\n--- Response Status & Final URL ---")
    print(f"Status Code: {response.status_code}")
    print(f"Final URL after redirects: {response.url}")

def fetch_authenticated_html_requests(url: str, username: str, password: str) -> str:
    """
    Logs into simplecell.recomapp.com using a requests Session and returns
    the page HTML.
    """
    # Create a session to automatically handle cookies/headers across requests
    session = requests.Session()
    
    # Custom User-Agent to prevent basic request blocking
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    })

    # Standard endpoint structure for login forms
    login_url = "https://simplecell.recomapp.com/login"
    
    # Payload matching typical form field names

    # Optional: Fetch initial page first if a CSRF token is required
    response_initial = session.get(login_url)
    payload = {
        'email': username,
        'password': password,
        'remember' : '1'
    }
    
    # Send login credentials via POST request
    response_post = session.post(login_url, data=payload)
    sleep(2)  # Optional: Wait for a moment to ensure the session is established
    response_post.raise_for_status()
    print_response_info(response_post)
    # Request the target URL with the authenticated session cookies
    target_response = session.get(url)
    sleep(2)  # Optional: Wait for a moment to ensure the page is fully loaded
    target_response.raise_for_status()

    with open('newhtml.html', 'w', encoding='utf-8') as f:
        f.write(target_response.text)
    return target_response.text

class RecomItemData:
    gtin: str
    sid: str
    sku: str
    def __init__(self, gtin: str, sid: str, sku: str):
        self.gtin = gtin
        self.sid = sid
        self.sku = sku
    def __str__(self):
        return f"GTIN: {self.gtin}, SID: {self.sid}, SKU: {self.sku}"


def get_recom_item_data(soup) -> RecomItemData:
    data : RecomItemData = RecomItemData(gtin='', sid='', sku='')
    gtin = soup.find('input', attrs={'name': 'product[gtin]'})
    if gtin and 'value' in gtin.attrs:
        data.gtin = gtin['value']

    sid = soup.find_all('div', class_='card-title')
    for title in sid:
        if title.find('h2'):
            sid_value = title.find('h2').text.strip()
            if sid_value.startswith('APP'):
                data.sid = sid_value

    sku = soup.find('a', class_='text-dark fw-bolder text-hover-primary fs-6')
    sku_pieces = sku.text.split('-')
    data.sku = sku_pieces[0] + '-' + sku_pieces[1]
    print(data)
    return data

debug = True
if debug:
    url = "https://simplecell.recomapp.com/products/96788"
    username = ""
    password = ""
    html = fetch_authenticated_html_requests(url, username, password)
    soup = BeautifulSoup(html, 'html.parser')
    data = get_recom_item_data(soup)
else:
    if sys.argv.__len__() == 4:
        url = sys.argv[1]
        print(url)
        username = sys.argv[2]
        password = sys.argv[3]
        html = fetch_authenticated_html_requests(url, username, password)
        soup = BeautifulSoup(html, 'html.parser')
        data = get_recom_item_data(soup)
    else:
        sys.exit(1)
