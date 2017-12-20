'''
    Scraper for ThisIsPlymouth.co.uk news stories.
'''
import re
import sys
import logging
import requests
import datetime
import base64
from bs4 import BeautifulSoup
from this_is_scraper.db import init_db
from this_is_scraper.db import get_db_session
from this_is_scraper.db import Articles


logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)


def remove_duplicates(l):
    return list(set(l))


def has_numbers(input_str):
    return any(char.isdigit() for char in input_str)


def list_stories():
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


def get_article_by_link(db_sess, link):
    articles = []
    result = db_sess.query(Articles). \
        filter(Articles.article_link == link).all()
    for article in result:
        articles.append(article)
    return articles


def insert_link(db_sess, link):
    new_article = Articles(article_link=link,
                           article_dt=datetime.datetime.now(),
                           article_status='pending')
    db_sess.add(new_article)
    db_sess.commit()


def insert_new_links(db_sess, links):
    add_count = 0
    for link in links:
        logging.debug("Processing %s." % link)
        curr_linked_articles = get_article_by_link(db_sess, link)
        if len(curr_linked_articles) == 0:
            logging.debug("%s doesn't exist in DB, adding." % link)
            insert_link(db_sess, link)
            add_count += 1
        else:
            logging.debug("%s already exists in DB, skipping." % link)
    return add_count


def get_pending_links(db_sess):
    pending_articles = db_sess.query(Articles). \
        filter(Articles.article_status == 'pending').all()
    return pending_articles


def extract_content(link):
    html_doc = requests.get(link)
    html_doc = html_doc.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    title = soup.title.string
    title = title.replace(' - Plymouth Herald', '')
    article_div = soup.findAll("div", {"class":"article-body"})
    for div in article_div:
        paragraphs = div.findAll("p")
    ret_text = ""
    for paragraph in paragraphs:
        ret_text += "%s <br/><br/>" % paragraph.get_text().strip()
    return title, ret_text.encode('utf-8')


def process_pending_articles(db_sess):
    pending_articles = get_pending_links(db_sess)
    for article in pending_articles:
        logging.debug("Processing %s." % article.article_link)
        try:
            title, content = extract_content(article.article_link)
            article.article_content = base64.b64encode(content)
            article.article_title = title
            article.article_status = 'complete'
        except:
            article.article_status = 'failed'
        db_sess.commit()


def main():
    logging.info("Checking database...")
    init_db()
    db_sess = get_db_session()
    links = list_stories()
    logging.info("Found %s articles on news front page." % len(links))
    logging.info("Inserting new articles to DB.")
    added = insert_new_links(db_sess, links)
    logging.info("%s new articles added to DB." % added)
    logging.info("Fetching pending articles.")
    process_pending_articles(db_sess)
    logging.info("Done!")


if __name__ == '__main__':
    main()
