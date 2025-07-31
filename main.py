import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import time

# Prompt user for target URL and settings
target_url = input("Enter target URL: ").strip().rstrip('/')
max_depth = int(input("Max crawl depth (default 2): ") or 2)
max_threads = int(input("Max threads (default 10): ") or 10)

visited = set()  # Track visited URLs to avoid duplicates
os.makedirs('pages', exist_ok=True)  # Create folder to save page HTML files

def normalize_url(url):
    """
    Normalize URLs by removing trailing slashes to avoid duplicates.
    """
    if url.endswith('/'):
        url = url[:-1]
    return url

def make_request(url):
    """
    Send HTTP GET request and parse content with BeautifulSoup.
    Returns BeautifulSoup object or None on failure.
    """
    try:
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            return None
        return BeautifulSoup(response.text, 'html.parser')
    except requests.RequestException:
        return None

def save_page(url, soup):
    """
    Save the HTML content of the page into 'pages' directory.
    Filenames are sanitized versions of the URLs.
    """
    filename = url.replace("http://", "").replace("https://", "").replace("/", "_") + ".html"
    filepath = os.path.join('pages', filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(str(soup))

def crawl(url, depth):
    """
    Crawl a single URL:
    - Check if already visited or max depth exceeded.
    - Fetch and parse the page.
    - Save the page content.
    - Extract and return links to crawl next.
    """
    url = normalize_url(url)
    if url in visited or depth > max_depth:
        return []

    visited.add(url)
    print(f"[{depth}] Visiting: {url}")

    soup = make_request(url)
    if soup is None:
        return []

    title = soup.title.string if soup.title else 'No Title'
    print(f"Title: {title}")

    save_page(url, soup)

    links_to_crawl = []
    base_netloc = urlparse(target_url).netloc

    for tag in soup.find_all("a"):
        href = tag.get("href")
        if href:
            full_url = urljoin(url, href)
            full_url = normalize_url(full_url)
            parsed_url = urlparse(full_url)

            # Only follow HTTP(S) links within the same domain
            if parsed_url.netloc == base_netloc and parsed_url.scheme in ['http', 'https']:
                if full_url not in visited:
                    links_to_crawl.append((full_url, depth + 1))
    return links_to_crawl

def threaded_crawl(start_url):
    """
    Manage crawling using a thread pool:
    - Maintain a queue of URLs with their depths.
    - Submit crawl tasks to threads.
    - Collect new links and continue until queue is empty.
    """
    to_crawl = [(normalize_url(start_url), 0)]

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = {}

        while to_crawl:
            # Submit crawl tasks for all URLs in queue
            for url, depth in to_crawl:
                futures[executor.submit(crawl, url, depth)] = (url, depth)
            to_crawl = []

            # Process completed tasks and gather new URLs
            for future in as_completed(futures):
                links = future.result()
                for link in links:
                    if link[0] not in visited and link[1] <= max_depth:
                        to_crawl.append(link)
            futures.clear()

# Start timer and run the threaded crawler
start_time = time.time()
threaded_crawl(target_url)
end_time = time.time()

print(f"\nVisited {len(visited)} pages in {end_time - start_time:.2f} seconds.")
