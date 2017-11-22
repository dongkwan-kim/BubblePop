import feedparser
import time
from newspaper import Article
from konlpy.tag import Hannanum
#from konlpy.tag import Mecab
from apiapp.models import Article, Media
from submodules.url_strip import url_strip

"""
1. call "crawl" function by server.
2. get urls py get_URLs.
3. check this urls already exist.
4. get articles by new urls
5. create article objects
"""

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

def crawl():
    hannanum = Hannanum()
    media = Media.objects.all()
    for medium in media:
        links = get_URLs(medium.rss_list)
        upper_bound = len(links)
        lower_bound = -1
        idx = upper_bound//2
        while lower_bound+1 == upper_bound:
            if media.filter(rss_link=links[idx]).exists():
                upper_bound = idx
                idx = lower_bound + (idx-1-lower_bound)//2
            else:
                lower_bound = idx
                idx += (upper_bound - (idx+1))//2 +1
        if lower_bound==-1:
            continue
        new_links = links[:lower_bound]
        for link in new_links:
            article = get_article(link)
            title = article.title
            content = article.text
            nouns = hannanum.nouns(article.text)
            morphemed_content = " ".join(nouns)
            writer = article.authors[0]
            published_at = article.published_at
            category = article.category
            media.create(
                title=title,
                content = content,
                morphemed_content = morphemed_content,
                media = medium,
                writer = writer,
                published_at = published_at,
                article_url = link,
                category = category,
            )







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

