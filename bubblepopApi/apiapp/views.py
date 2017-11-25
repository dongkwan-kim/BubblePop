from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from submodules.url_strip import url_strip
from submodules.crawler import crawl
from submodules.cluster import cluster
from apiapp.models import Article, UserProfile, UserBlackList, Report, Media, Cluster
from django.views.decorators.csrf import csrf_exempt

import json
import random

# Make this value for deploy
NOW_TEST = True


def test(request):
    return HttpResponse("test works")

def check_url(request):
    if (request.method != "GET"):
        raise SuspiciousOperation
    url = request.GET['url']
    url = url_strip(url)
    # check url

    return JsonResponse({
        'url': url,
        'result': Article.objects.filter(article_url=url).exists(),
    })


def find_articles(request):

    if (request.method != "GET"):
        raise SuspiciousOperation

    url = request.GET['url']
    user = request.user
    if not user.is_authenticated:
        return HttpResponse("Unauthenticated", status=401)

    black_list = UserBlackList.objects.filter(user=user)
    article = Article.objects.get(article_url = url)
    media = article.media
    affinity = media.political_view


    if (article.cluster is None):
        date = article.published_at
        articles_for_cluster = Article.objects.filter(published_at=date)
        nouns_list = [a.morphemed_content for a in articles_for_cluster]
        cluster_dict = cluster(nouns_list)
        print(cluster_dict)
        base = Cluster.objects.all().count()
        for key in cluster_dict:
            now_cluster = Cluster.objects.create(cluster_id = base+key)
            for article_idx in cluster_dict[key]:
                articles_for_cluster[article_idx].cluster = now_cluster
                articles_for_cluster[article_idx].save()
        article = Article.objects.get(article_url = url)





    related_articles = Article.objects.filter(cluster=article.cluster).exclude(article_url = article.article_url)
    same_view_media = Media.objects.all().filter(political_view=affinity)
    related_diff = related_articles
    related_diff = related_diff.exclude(media__in=same_view_media)
    blacked_media = [b.media for b in black_list]
    related_diff = related_diff.exclude(media__in=blacked_media)
    if not related_diff.exists():
        related_diff = related_articles

    count = related_diff.count()

    result = None
    success = False
    if count>0:
        news_idx = random.randrange(0,count)
        result = related_diff[news_idx].article_url
        success = True

    return JsonResponse({
        'url': url,
        'result': result,
        'success': success
    })


def blacklist(request):
    user = request.user
    if not user.is_authenticated:
        return HttpResponse("Unauthenticated", status=401)
    black_list = UserBlackList.objects.filter(user=user)
    return JsonResponse({
        "result": [n.get_media() for n in list(black_list)]
    })


@csrf_exempt
def change_blacklist(request):

    if (request.method != "GET"):
        raise SuspiciousOperation

    media_list = request.GET.getlist('media[]')
    user = request.user
    if not user.is_authenticated:
        if NOW_TEST:
            user = User.objects.all()[0]
        else:
            return HttpResponse("Unauthenticated", status=401)

    res = []
    for media_name in media_list:
        media = Media.objects.get(name=media_name)
        black_list = UserBlackList.objects.filter(user=user, media=media)
        if (black_list.exists()):
            black_list.delete()
            res.append({
                'media': media_name,
                'result': False
            })
        else:
            UserBlackList.objects.create(user=user, media=media)
            res.append({
                'media': media_name,
                'result': True
            })

    return JsonResponse(json.dumps(res, ensure_ascii=False), safe=False)


def report(request):

    if (request.method != "GET"):
        raise SuspiciousOperation

    url1 = request.GET['url_a']
    url2 = request.GET['url_b']
    content = request.GET['content']
    user = request.user
    article1 = Article.objects.get(article_url=url1)
    article2 = Article.objects.get(article_url=url2)
    if (url2 < url1):
        article1, article2 = article2, article1

    Report.objects.create(
        user=user,
        article_a=article1,
        article_b=article2,
        content=content,
    )
    return JsonResponse({
        'url_a': url1,
        'url_b': url2,
        'result': True,
    })

def force_crawl(request):
    count,all = crawl()
    return JsonResponse({'crawl':count,'all':all})

