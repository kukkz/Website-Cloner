import os
import argparse
from selenium import webdriver
from bs4 import BeautifulSoup

def clone_website(url, output_folder):
    # Configure Chrome WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)

    try:
        # Load the website
        driver.get(url)

        # Get the page source after JavaScript execution
        page_source = driver.page_source

        # Parse the HTML content of the website
        soup = BeautifulSoup(page_source, 'html.parser')

        # Create a folder for storing cloned content
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Save the entire HTML content
        with open(os.path.join(output_folder, 'index.html'), 'w', encoding='utf-8') as file:
            file.write(str(soup))

        # Download static assets (CSS, JavaScript, images)
        for tag in soup.find_all(['link', 'script', 'img']):
            if tag.has_attr('src'):
                asset_url = tag['src']
                if asset_url.startswith(('http://', 'https://')):
                    driver.get(asset_url)
                    with open(os.path.join(output_folder, os.path.basename(asset_url)), 'wb') as asset_file:
                        asset_file.write(driver.page_source.encode('utf-8'))

        print("Website cloned successfully. You can find it in the '{}' folder.".format(output_folder))
    finally:
        # Quit the WebDriver session
        driver.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Clone a website.')
    parser.add_argument('-u', '--url', type=str, required=True, help='URL of the website')
    parser.add_argument('-o', '--output', type=str, default='cloned_website', help='Output folder path')

    args = parser.parse_args()

    clone_website(args.url, args.output)
