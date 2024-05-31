import requests
from bs4 import BeautifulSoup

def scrape_links(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all divs with the class 'media-object__figure'
        divs = soup.find_all('div', class_='media-object__figure')

        # Extract all href links within these divs
        links = []
        for div in divs:
            # Find all 'a' tags inside each div
            a_tags = div.find_all('a', href=True)
            for a in a_tags:
                links.append(a['href'])

        return links

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return []

url = 'https://www.channelnewsasia.com/topic/terrorism?sort_by=field_release_date_value&sort_order=DESC&page=1'  # Replace with the target URL
links = scrape_links(url)
#get individual article links
links = [link for link in links if link.startswith('/singapore')]


print("Found links:", links)
