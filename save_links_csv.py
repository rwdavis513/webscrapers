import pandas as pd
import json

import requests
from bs4 import BeautifulSoup

def get_links_from_url(url):
    """
    Extract all links and their text from a webpage
    
    Args:
        url (str): URL of the webpage to scrape
        
    Returns:
        list: List of dictionaries containing url and title for each link
    """
    # Check if URL is a local file
    if url.startswith('file:///'):
        # Remove file:// prefix and handle URL encoding
        file_path = url.replace('file:///', '').replace('%20', ' ')
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
        except Exception as e:
            print(f"Error reading local file: {e}")
            return []
    else: 
        # Send GET request to URL
        try:
            response = requests.get(url)
            response.raise_for_status()
            html_content = response.text
        except requests.RequestException as e:
            print(f"Error fetching URL: {e}")
            return []

    # Parse HTML content
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find all <a> tags
    links = []
    for a_tag in soup.find_all('a'):
        link = {
            'url': a_tag.get('href', ''),
            'title': a_tag.get_text(strip=True)
        }
        # Only include links that have a URL
        if link['url']:
            links.append(link)
            
    return links

# Xpath for links 
# response = fetch(url)
# response.xpath("//a").xpath("concat(@href, '|', text())").getall() 

def load_json_file(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def save_links_to_csv(data, file_path):
    
    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Save as CSV
    df.to_csv(file_path.replace('.json', '.csv'), index=False)

if __name__ == "__main__":
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    url = "file:///C:/Users/rwdav/OneDrive/Documents/Wellness%20Acquisitions/FB%20Weight%20Loss%20Groups%203.4.25.html"
    links = get_links_from_url(url)
    
    save_links_to_csv(links, f'links_{timestamp}.json')
