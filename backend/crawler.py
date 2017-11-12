import feedparser
from newspaper import Article

def get_URLs(rss_link):
    parsed = feedparser.parse(rss_link)
    links = []
    for entry in parsed.entries:
        links.append(entry.link)

    return links

def get_article(url):
    article = Article(url,language='ko')
    article.download()
    article.parse()
    return article

def test():
    file = open("test.txt",'w',encoding="utf8")
    rss_list = [
        #"https://www.reddit.com/",
        "http://www.chosun.com/site/data/rss/politics.xml",
        "http://rss.joins.com/joins_politics_list.xml",

        ]
    for rss_link in rss_list:
        links = get_URLs(rss_link)
        for link in links:
            article = get_article(link)
            file.write(article.title)
            file.write("\n")
    file.flush()
    file.close()

if __name__ == "__main__":
    test()


