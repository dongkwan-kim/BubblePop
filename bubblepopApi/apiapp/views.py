from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from submodules.url_strip import url_strip
from submodules.crawler import crawl
from apiapp.models import Article, UserProfile, UserBlackList, Report, Media


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

    #if (article.cluster is not None):
        # just show clustered articles
    #else:
        # make related articles

    # for test
    return JsonResponse({
        'url': url,
        'result': article.cluster.cluster_id,
    })


def blacklist(request):
    user = request.user
    if not user.is_authenticated:
        return HttpResponse("Unauthenticated", status=401)
    black_list = UserBlackList.objects.filter(user=user)
    return JsonResponse({
        "result": [n.get_media() for n in list(black_list)]
    })


def change_blacklist(request):

    if (request.method != "GET"):
        raise SuspiciousOperation

    media_name = request.GET['media']
    user = request.user
    media = Media.objects.get(name=media_name)
    if not user.is_authenticated:
        return HttpResponse("Unauthenticated", status=401)

    black_list = UserBlackList.objects.filter(user=user, media=media)
    if (black_list.exists()):
        black_list.delete()
        return JsonResponse({
            'media': media_name,
            'result': False
        })

    UserBlackList.objects.create(user=user, media=media)
    return JsonResponse({
        'media': media_name,
        'result': True
    })


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
    crawl()
    return JsonResponse({'result':True})

