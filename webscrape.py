import requests
from bs4 import BeautifulSoup
import cssutils

import urllib.parse

def extract_css_properties(base_url, css_url):
    if not css_url.startswith('http'):
        css_url = urllib.parse.urljoin(base_url, css_url)

    response = requests.get(css_url)
    css_content = response.text

    # Parse CSS content
    sheet = cssutils.parseString(css_content)

    # Extract properties
    properties = {}
    for rule in sheet:
        if isinstance(rule, cssutils.css.CSSStyleRule):
            selector = rule.selectorText
            for property in rule.style:
                property_name = property.name
                property_value = property.value
                properties.setdefault(selector, {}).update({property_name: property_value})

    return properties
def scrape_background_images(url):
    response = requests.get(url)
    html_content = response.text

    # Parse HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find CSS files linked in the HTML
    css_files = []
    for link in soup.find_all('link', rel='stylesheet'):
        css_files.append(link['href'])

    # Extract background images and their properties
    background_images = {}
    for css_file in css_files:
        css_properties = extract_css_properties(url, css_file)
        for selector, properties in css_properties.items():
            if 'background-image' in properties and 'opacity' in properties:
                background_images.setdefault(css_file, []).append({
                    'background-image': properties['background-image'],
                    'opacity': properties['opacity']
                })

    return background_images


def save_to_file(background_images, file_path):
    with open(file_path, 'w') as file:
        for css_file, images in background_images.items():
            file.write(f'CSS File: {css_file}\n')
            for image in images:
                file.write(f'Image URL: {image["background-image"]}, Opacity: {image["opacity"]}\n')
            file.write('\n')

url = 'https://www.webtoons.com/en/'  # Replace with the URL you want to scrape
background_images = scrape_background_images(url)
file_path = 'background_images.txt'  # File path to save the data
save_to_file(background_images, file_path)
