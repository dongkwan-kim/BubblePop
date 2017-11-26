import feedparser
import time
import jpype
import newspaper as news
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

hannanum = None

def get_URLs(rss_link):
    parsed = feedparser.parse(rss_link)
    links = []
    for entry in parsed.entries:
        links.append(url_strip(entry.link))
    return links

def get_article(url):
    article = news.Article(url,language='ko')
    article.download()
    article.parse()
    return article


def crawl():
    global hannanum
    if hannanum==None:
        hannanum = Hannanum()
    if jpype.isJVMStarted():
        jpype.attachThreadToJVM()
    hannanum = Hannanum()
    media = Media.objects.all()
    articles = Article.objects.all()
    count = 0
    all = 0
    for medium in media:
        links = get_URLs(medium.rss_list)

        upper_bound = len(links)

        all += upper_bound

        for link in links:
            #print(link)
            if (Article.objects.filter(article_url=link)).exists():
                continue
            try:
                article = get_article(link)
            except:
                print("Fail:%s"%link)
                continue
            title = article.title
            content = article.text
            nouns = hannanum.nouns(article.text)
            morphemed_content = " ".join(nouns)
            writer=''
            if len(article.authors)==0:
                writer = 'anonymous'
            else:
                writer = article.authors[0]
            try:
                articles.create(
                    title=title,
                    content = content,
                    morphemed_content = morphemed_content,
                    media = medium,
                    writer = writer,
                    article_url = link,
                )
                count+=1
            except:
                continue
    return (count,all)






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

