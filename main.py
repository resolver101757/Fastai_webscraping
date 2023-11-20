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

def is_html_url(url):
    """Check if the URL points to an HTML document."""
    parsed_url = urlparse(url)
    if parsed_url.path.endswith(('.gif', '.jpg', '.jpeg', '.png', '.svg', '.webp')):
        return False

    try:
        response = requests.head(url, allow_redirects=True)
        content_type = response.headers.get('Content-Type', '')
        return 'text/html' in content_type
    except requests.RequestException:
        return False

def extract_markdown_from_url(visited_links, element_id=None, element_class=None):
    markdown_contents = {}
    
    for url, html_content in visited_links.items():
        try:
            soup = BeautifulSoup(html_content, 'html.parser')

            # Remove unwanted tags and comments
            for tag in soup(['script', 'style', 'header', 'footer', 'nav', 'aside', 'iframe', 'form']):
                tag.decompose()

            # Extract relevant part of the webpage
            main_content = soup.find(id=element_id) if element_id else soup.find(class_=element_class) if element_class else soup

            # Convert to text
            text_content = main_content.get_text(separator='\n', strip=True)

            # Convert to Markdown
            converter = html2text.HTML2Text()
            converter.ignore_links = False
            markdown_content = converter.handle(text_content)

            # Store in dictionary
            markdown_contents[url] = f"***URL: {url}***\n\n{markdown_content}"
        except Exception as e:
            print(f"Error processing {url}: {e}")

    return markdown_contents


def is_same_domain(url1, url2):
    """ Check if two URLs belong to the same domain """
    return urlparse(url1).netloc == urlparse(url2).netloc

def crawl(url, visited={}):
    """ Crawl a URL and follow links within the same domain """
    if url in visited or not is_html_url(url):
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
def save_to_file(extracted_contents, file_name='output.txt', folder='output\\'):
    for item in extracted_contents:
        with open(folder + file_name, 'a', encoding='utf-8') as f:
            f.write(item)



def make_windows_compatible(filename):
    """
    Converts a string into a format compatible with Windows file naming conventions.
    Strips invalid characters and replaces them with an underscore.
    """
    # Characters not allowed in Windows file names
    invalid_chars = '<>:"/\\|?*'

    # Replace each invalid character with an underscore
    for char in invalid_chars:
        filename = filename.replace(char, '_')

    # Windows also doesn't allow file names to end with a space or a dot
    filename = filename.rstrip('. ')

    # Check for reserved file names and append an underscore if necessary
    reserved_names = ["CON", "PRN", "AUX", "NUL", "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9", "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"]
    if filename.upper() in reserved_names:
        filename += '_'

    return filename

# read list of urls from a file
with open('list_of_blogs.txt', 'r') as f:
    urls = f.read().splitlines()
    
# crawl each url and extract the content
for url in urls:
    extracted_contents = []
    visited_links = crawl(url)
    extract_markdown_from_url(visited_links)
    filename = make_windows_compatible(url)
    save_to_file(extracted_contents, file_name=filename + '.txt') 

