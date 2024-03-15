import requests
from bs4 import BeautifulSoup
import urllib.parse

def get_website_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching website content: {e}")
        return None

def extract_logo_urls(html_content, domain):
    logo_urls = set()
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all <img> tags
    img_tags = soup.find_all('img')

    for img in img_tags:
        src = img.get('src')
        if src:
            # Check if src attribute is a relative URL
            if not src.startswith('http'):
                # If it's a relative URL, join it with the domain to form an absolute URL
                src = urllib.parse.urljoin(domain, src)
            logo_urls.add(src)

    # Find all URLs within the webpage content
    for tag in soup.find_all():
        for attr in ['src', 'href']:
            url = tag.get(attr)
            if url and url.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                if not url.startswith(('http', '#')):
                    url = urllib.parse.urljoin(domain, url)
                logo_urls.add(url)

    return logo_urls

def save_urls_to_file(urls, output_file):
    with open(output_file, 'w') as f:
        for url in urls:
            f.write(url + '\n')

def main():
    domain = input("Enter the domain (e.g., example.com): ")
    url = f"https://{domain}"

    website_content = get_website_content(url)
    if website_content is None:
        return

    logo_urls = extract_logo_urls(website_content, url)

    output_file = 'logo_urls.txt'
    save_urls_to_file(logo_urls, output_file)

    print(f"All logo URLs from {domain} saved to {output_file}")

if __name__ == "__main__":
    main()
