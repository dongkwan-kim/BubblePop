import feedparser
import time
from newspaper import Article
from konlpy.tag import Hannanum
#from konlpy.tag import Mecab
#from apiapp.models import Article, Media
from url_strip import url_strip


def get_URLs(rss_link):
    parsed = feedparser.parse(rss_link)
    links = []
    for entry in parsed.entries:
        links.append(url_strip(entry.link))
    return links

def get_article(url):
    article = Article(url,language='ko')
    article.download()
    article.parse()
    return article

def test():
    rss_list = [
        # "https://www.reddit.com/",
        "http://www.chosun.com/site/data/rss/politics.xml",
        "http://rss.joins.com/joins_politics_list.xml",
    ]

    hannanum = Hannanum()
    # mecab = Macab()

    for rss_link in rss_list:
        print("Start get_URLs and read files from : " + rss_link)
        start_time = time.time()
        links = get_URLs(rss_link)
        for link in links:
            parse_time = time.time()
            article = get_article(link)
            file = open("./test/%s.txt" % (article.title),
                    'w', encoding="utf8")
            nouns = hannanum.nouns(article.text)
            # nouns = mecab.nouns(article.text)

            for noun in nouns:
                file.write("%s\n" % noun)
            file.close()
            parse_time = time.time() - parse_time
            print("parse files from %s: %f" % (link, parse_time))
        start_time = time.time() - start_time
        print("Process time : %f" % (start_time))

if __name__ == "__main__":
    test()

