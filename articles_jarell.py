import requests
from bs4 import BeautifulSoup
import re

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

def scrape_article(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        main_content = soup.find('section', id='block-mc-cna-theme-mainpagecontent')
        if main_content:
            first_child = main_content.findChild()
            if first_child:
                content_child = first_child.find('div', class_='content')
                if content_child:
                    last_child = content_child.find_all(recursive=False)[3]
                    first_child = last_child.findChild()
                    first_child = first_child.findChild()
                    if first_child:
                        child_div = first_child.find('div')
                        if child_div:
                            contents = ''
                            contents = contents.join([re.sub(r'[\xa0/\'"]', '', paragraph.get_text(separator=' ', strip=True)) for paragraph in child_div.find_all('p')])
                            
                            return contents

        return {"first_child_texts": "No content found", "last_child_texts": "No content found"}
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return {"first_child_texts": "Error fetching the article", "last_child_texts": "Error fetching the article"}


def cna_articles():
    base_url = 'https://www.channelnewsasia.com'
    articles = []
    for i in range(7):
        url = f'https://www.channelnewsasia.com/topic/terrorism?sort_by=field_release_date_value&sort_order=DESC&page={i}'  # Replace with the target URL
        links = scrape_links(url)
        #get individual article links
        filtered_links = [link for link in links if link.startswith('/singapore')]

        for link in filtered_links:
            full_url = base_url + link  # Construct full URL
            article = scrape_article(full_url)
            articles.append(article)
    return articles

if __name__ == '__main__':
    print(cna_articles()[:3])
    print(len(cna_articles()))