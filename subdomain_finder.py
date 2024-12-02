
import requests
from bs4 import BeautifulSoup

def find_subdomains(domain):
    # List of potential subdomains to check
    subdomains = ['www', 'mail', 'blog', 'shop', 'dev', 'test']

    discovered_subdomains = []

    for subdomain in subdomains:
        url = f"http://{subdomain}.{domain}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                discovered_subdomains.append(url)
        except requests.ConnectionError:
            pass

    return discovered_subdomains

def find_subdomains_from_html(domain):
    search_url = f"https://www.google.com/search?q=site:{domain}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    discovered_subdomains = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and domain in href:
            parts = href.split('/')
            if len(parts) > 2:
                subdomain = parts[2]
                if subdomain not in discovered_subdomains and domain in subdomain:
                    discovered_subdomains.append(subdomain)

    return discovered_subdomains

if __name__ == "__main__":
    domain = 'bing.com'
    subdomains = find_subdomains(domain)
    print(f"Discovered subdomains for {domain}:")
    for subdomain in subdomains:
        print(subdomain)

    print("\nDiscovered subdomains from Google search:")
    google_subdomains = find_subdomains_from_html(domain)
    for subdomain in google_subdomains:
        print(subdomain)
        
