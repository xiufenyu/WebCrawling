# https://m.lewenshu.com/article/5506/2207905.html

BASE_URL = "http://m.qqxs.co/book/19034/"
FIRST_CHAPTER = "http://m.qqxs.co/book/19034/8887270.html"

import requests
from bs4 import BeautifulSoup
import time


def make_request(url):
    html_doc = requests.get(url).text
    soup = BeautifulSoup(html_doc, "html.parser")
    title = soup.find("h1", {"id":"nr_title"}).text
    # print("title:", title)

    article_body = soup.find("div", {"id": "nr1"})
    article = ""
    if article_body:
        for br in article_body:
            article += br.text
    pb_next = soup.find("a", {"id": "pb_next"}, href=True)
    new_url = None
    new_url = BASE_URL + pb_next["href"]
    
    return [title, article_body, new_url]



if __name__ == "__main__":
    title = ""
    body = None
    url = FIRST_CHAPTER
    while url is not None:
        tuples = make_request(url)
        title, body, new_url = tuples[0], tuples[1], tuples[2]
        print("title: " + title + ", url:" + url)
        with open ("novel.txt", "a") as f:
            f.write(title + "\n")
            f.write(body.text + "\n")
        time.sleep(5)
        url = new_url
