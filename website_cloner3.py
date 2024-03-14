import requests
from bs4 import BeautifulSoup
import argparse
import os

def clone_website(url):
    # Send a GET request to the website
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the website
        soup = BeautifulSoup(response.text, 'html.parser')

        # Create a folder for storing cloned content
        output_folder = os.path.basename(url)
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Save the entire HTML content
        with open(os.path.join(output_folder, 'index.html'), 'w', encoding='utf-8') as file:
            file.write(str(soup))

        # Download static assets (CSS, JavaScript, images)
        for link in soup.find_all(['link', 'script', 'img']):
            if link.has_attr('href'):
                asset_url = link['href']
            elif link.has_attr('src'):
                asset_url = link['src']
            else:
                continue
            
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

    args = parser.parse_args()

    clone_website(args.url)
