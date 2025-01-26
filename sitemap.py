import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, quote, unquote
import xml.etree.ElementTree as ET


def sanitize_url(url):
    """
    Sanitize a URL by encoding spaces and other unsafe characters.
    """
    try:
        return quote(unquote(url), safe=":/?#[]@!$&'()*+,;=")
    except Exception as e:
        print(f"Failed to sanitize URL: {url}, Error: {e}")
        return None


def is_valid_html_url(url, domain):
    """
    Validate if the URL is an HTML page or directory and belongs to the given domain.
    """
    parsed = urlparse(url)
    return (
        parsed.scheme in ('http', 'https') and
        parsed.netloc == domain and
        (parsed.path.endswith(('.html', '/')) or parsed.path == "")
    )


def get_links(url, visited, session, domain):
    """
    Crawl a website and collect all valid internal links within the domain.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }
    links = set()
    try:
        response = session.get(url, headers=headers, timeout=10, allow_redirects=True)
        response.raise_for_status()

        # Skip non-HTML content
        content_type = response.headers.get("Content-Type", "").lower()
        if "text/html" not in content_type:
            print(f"Skipping non-HTML content: {url}")
            return links

    except requests.RequestException as e:
        print(f"Error accessing {url}: {e}")
        return links

    soup = BeautifulSoup(response.text, 'html.parser')
    base_url = f"{urlparse(url).scheme}://{urlparse(url).netloc}"

    for anchor in soup.find_all("a", href=True):
        href = urljoin(base_url, anchor["href"])
        sanitized_href = sanitize_url(href)

        if sanitized_href and is_valid_html_url(sanitized_href, domain):
            if sanitized_href not in visited:
                links.add(sanitized_href)
    return links


def crawl_website(start_url):
    """
    Recursively crawl a website and find all pages.
    """
    session = requests.Session()
    to_visit = {start_url}
    visited = set()
    domain = urlparse(start_url).netloc

    while to_visit:
        current_url = to_visit.pop()
        print(f"Crawling: {current_url}")
        visited.add(current_url)
        links = get_links(current_url, visited, session, domain)
        to_visit.update(links - visited)

    return visited


def generate_sitemap(urls, output_file="sitemap.xml"):
    """
    Generate a sitemap.xml file from a list of URLs.
    """
    print(f"Generating sitemap with {len(urls)} URLs...")
    urlset = ET.Element("urlset", attrib={"xmlns": "http://www.sitemaps.org/schemas/sitemap/0.9"})

    for url in sorted(urls):
        url_elem = ET.SubElement(urlset, "url")
        loc_elem = ET.SubElement(url_elem, "loc")
        loc_elem.text = url

    tree = ET.ElementTree(urlset)
    tree.write(output_file, encoding="utf-8", xml_declaration=True)
    print(f"Sitemap saved to {output_file}")


if __name__ == "__main__":
    start_url = input("Enter the starting URL: ").strip()
    if not start_url.startswith("http://") and not start_url.startswith("https://"):
        start_url = f"http://{start_url}"
    sanitized_start_url = sanitize_url(start_url)
    if not sanitized_start_url:
        print("Invalid starting URL. Exiting.")
        exit(1)

    # Crawl the website
    all_pages = crawl_website(sanitized_start_url)

    # Generate the sitemap
    output_file = "sitemap.xml"
    generate_sitemap(all_pages, output_file)
