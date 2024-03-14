import requests
from bs4 import BeautifulSoup
import argparse
import os
from urllib.parse import urljoin

def clone_website(url, output_folder):
    # Send a GET request to the website
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the website
        soup = BeautifulSoup(response.text, 'html.parser')

        # Create a folder for storing cloned content
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Update src attributes for external resources
        for tag in soup.find_all(['link', 'script', 'img']):
            if tag.has_attr('src') and tag['src'].startswith(('http://', 'https://')):
                continue  # Skip if src is already an absolute URL

            if tag.has_attr('src') and (tag['src'].startswith('/') or tag['src'].startswith('../')):
                tag['src'] = urljoin(url, tag['src'])

        # Save the entire HTML content
        with open(os.path.join(output_folder, 'index.html'), 'w', encoding='utf-8') as file:
            file.write(str(soup))

        # Download static assets (CSS, JavaScript, images)
        for tag in soup.find_all(['link', 'script', 'img']):
            if tag.has_attr('src'):
                asset_url = tag['src']
                if asset_url.startswith('http'):
                    asset_response = requests.get(asset_url)
                    if asset_response.status_code == 200:
                        with open(os.path.join(output_folder, os.path.basename(asset_url)), 'wb') as asset_file:
                            asset_file.write(asset_response.content)

        print("Website cloned successfully. You can find it in the '{}' folder.".format(output_folder))
    else:
        print("Failed to fetch website content. Status code:", response.status_code)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Clone a website.')
    parser.add_argument('-u', '--url', type=str, required=True, help='URL of the website')
    parser.add_argument('-o', '--output', type=str, default='cloned_website', help='Output folder path')

    args = parser.parse_args()

    clone_website(args.url, args.output)
