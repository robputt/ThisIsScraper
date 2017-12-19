'''
    Scraper for ThisIsPlymouth.co.uk news stories.
'''
import requests
import re
from bs4 import BeautifulSoup


def remove_duplicates(l):
    return list(set(l))


def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)


def list_stories():
    '''
        Fetches a list of links to articles currently on the news front page.
    '''
    article_links = []
    html_doc = requests.get('http://www.plymouthherald.co.uk/news/')
    soup = BeautifulSoup(html_doc.text, 'html.parser')
    url_stub = "^http://www.plymouthherald.co.uk/news/"
    for link in soup.findAll('a', attrs={'href': re.compile(url_stub)}):
        href = link.get('href')
        if href != 'http://www.plymouthherald.co.uk/news/':
            # remove links to comments and any invalid articles, valid
            # articles have numbers in their URLs, interesting huh?
            if ('#comments-section' not in href) and (has_numbers(href)):
                article_links.append(href)

    article_links = remove_duplicates(article_links)
    return article_links


if __name__ == '__main__':
    links = list_stories()
    print("Found %s articles on news front page." % len(links))
    for link in links:
        print(link)
