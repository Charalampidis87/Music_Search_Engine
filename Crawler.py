import requests
from bs4 import BeautifulSoup
import json
import urllib.parse
import re
from Indexer import index
from main import start_server


def clean(text):
    text = (text.encode('ascii', 'ignore')).decode("utf-8")
    text = re.sub("&.*?;", "", text)
    text = re.sub(">", "", text)
    text = re.sub("[\]\|\[\@\,\$\%\*\&\\\(\)\":]", "", text)
    text = re.sub("-", " ", text)
    text = text.replace("'", "")
    text = text.replace("|", "")
    text = text.replace("\n", " ")
    text = re.sub("\.+", "", text)
    text = re.sub("^\s+", "", text)
    text = text.lower()
    text = text.replace("/", "")
    while "  " in text:
        text = text.replace("  ", " ")
    return text


def crawl(url):
    print('Crawling: ' + url)
    visited_urls.append(url)
    response = requests.get(url, headers=headers)
    content = BeautifulSoup(response.text, 'lxml')
    content_text = clean(content.get_text())
    output.append({'url': url, 'page': content_text})

    # Get href links of the document (absolute and relative)
    href_links = content.find_all('a', href=True)
    for link in href_links:
        link_absolute = urllib.parse.urljoin(domains, link.get('href'))
        if (start_url in link_absolute) and (link_absolute not in urls):
            urls.append(link_absolute)

    # Get links from document text (capture dynamic JavaScript links)
    content_string = str(content)
    content_links = re.findall(r'(\b' + domains + '.*?)[\'"]', content_string)
    for link in content_links:
        if (start_url in link) and (link not in urls):
            urls.append(link)
    return


if __name__ == '__main__':
    domains = 'https://www.allmusic.com'
    start_url = 'https://www.allmusic.com/artist/eminem-mn0000157676'
    headers = {'user-agent': 'Mozilla/5.0 (Linux; U; Android 4.1.1; en-gb; Build/KLP) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Safari/534.30'}
    urls = []
    visited_urls = []
    urls.append(start_url)
    output = []

    for link in urls:
        if (start_url in link) and (link not in visited_urls):
            crawl(link)

    with open('output.json', 'w') as output_file:
        output_file.write(json.dumps(output))

    # Create Inverted Index
    print('Creating inverted index')
    index()
    print('Inverted index is ready')

    # Start Web Server
    start_server()