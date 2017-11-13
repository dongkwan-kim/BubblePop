import feedparser
from newspaper import Article
import time
#from konlpy.tag import Mecab

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
    rss_list = [
        #"https://www.reddit.com/",
        "http://www.chosun.com/site/data/rss/politics.xml",
        "http://rss.joins.com/joins_politics_list.xml",

        ]
    #mecab = Macab()
    for rss_link in rss_list:
        print("Start get_URLs and read files from : "+rss_link)
        start_time = time.time()
        links = get_URLs(rss_link)
        for link in links:
            article = get_article(link)
            file = open("./test/%s.txt"%(article.title),
                    'w',encoding="utf8")
            #file.write(article.title)
            #nouns = mecab.nouns(article.content)

            #for noun in nouns:
            #    file.write("%s\n"%noun)
            file.close()
        print("Process time : %f"%(time.time()-start_time))

if __name__ == "__main__":
    test()


