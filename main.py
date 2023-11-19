from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin, urlparse
import html2text
import time 

def extract_links(url, html_content):
    """ Extract links from the HTML content of a page, excluding links within the same document """
    soup = BeautifulSoup(html_content, 'html.parser')
    links = set()
    for link in soup.find_all('a', href=True):
        href = link['href']
        # Parse the URL and check if it has a fragment (part after '#')
        parsed_href = urlparse(href)
        if parsed_href.fragment:
            continue  # Skip links that point to the same document
        # Convert relative URL to absolute URL
        absolute_url = urljoin(url, href)
        links.add(absolute_url)
    return links

def extract_markdown_from_url(visited_links, element_id=None, element_class=None):
    """
    Downloads webpage content from the given URL, extracts a specific part of it,
    and converts it to Markdown format.

    Args:
    url (str): URL of the webpage to download.
    element_id (str, optional): ID of the HTML element to extract. Defaults to None.
    element_class (str, optional): Class of the HTML element to extract. Defaults to None.

    Returns:
    str: Markdown content of the extracted part of the webpage.
    """
    for url, html_content in visited_links.items():
        
        # Parse HTML using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract relevant part of the webpage
        if element_id:
            main_content = soup.find(id=element_id)
        elif element_class:
            main_content = soup.find(class_=element_class)
        else:
            main_content = soup

        # Convert HTML to Markdown
        converter = html2text.HTML2Text()
        converter.ignore_links = False
        markdown_content = converter.handle(str(main_content))

        # Add Markdown content to the list
        extracted_contents.append(markdown_content)

def is_same_domain(url1, url2):
    """ Check if two URLs belong to the same domain """
    return urlparse(url1).netloc == urlparse(url2).netloc

def crawl(url, visited={}):
    """ Crawl a URL and follow links within the same domain """
    if url in visited:
        return
    try:
        time.sleep(2)
        response = requests.get(url)
        html_content = response.text
        visited[url] = html_content  # Store the HTML content in the dictionary

        links = extract_links(url, html_content)

        for link in links:
            if is_same_domain(url, link):
                crawl(link, visited)
    except requests.RequestException:
        pass

    return visited

# a function save each item in the list to a file
def save_to_file(extracted_contents):
    for item in extracted_contents:
        with open('output.txt', 'a', encoding='utf-8') as f:
            f.write(item)


# Start crawling from a given URL
start_url = 'https://viktoranchutin.github.io'
visited_links = crawl(start_url)
print(visited_links)

extracted_contents = []

extract_markdown_from_url(visited_links)

save_to_file(extracted_contents)        
        
print(extracted_contents)