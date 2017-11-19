from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from submodules.url_strip import url_strip
from apiapp.models import Article, UserProfile, UserBlackList, Report, Media


def test(request):
    return HttpResponse("test works")

def check_url(request):
    if (request.method != "GET"):
        raise SuspiciousOperation
    url = request.GET['url']
    url = url_strip(url)
    # check url

    """
    try:
        Article.object.get(article_url = url)

    except DoesNotExist:

        return JsonResponse({'url':url,'result':False})
    except MultipleObjectsReturned:
        print("More than 2 articles in same url.")
        return JsonResponse({'url':url,'result':True})
    """

    return JsonResponse({'url':url,
        'result':Article.objects.filter(article_url = url).exists()})

def find_articles(request):
    if (request.method != "GET"):
        raise SuspiciousOperation
    url = request.GET['url']
    user = request.user
    if not user.is_authenticated:
        return HttpResponse("Unauthenticated",status=401)
    black_list = UserBlackList.objects.filter(user = user)
    article = Article.objects.get(article_url = url)

    #if (article.cluster is not None):
        # just show clustered articles
    #else:
        # make related articles

    # for test
    return JsonResponse({'url':url,'result':article.cluster.cluster_id})


def blacklist(request):
    user = request.user
    if not user.is_authenticated:
        return HttpResponse("Unauthenticated",status=401)
    black_list = UserBlackList.objects.filter(user = user)
    return JsonResponse({"result":list(black_list)})



def change_blacklist(request):
    if (request.method != "GET"):
        raise SuspiciousOperation
    media_name = request.GET['media']
    user = request.user
    media = Media.objects.get(name = media_name)
    if not user.is_authenticated:
        return HttpResponse("Unauthenticated",status=401)
    black_list = UserBlackList.objects.filter(user = user,media = media)
    if (black_list.exists()):
        black_list.delete()
        return JsonResponse({'media':media_name,'result':False})

    UserBlackList.objects.create(user=user,media=media)
    return JsonResponse({'media':media_name,'result':True})



def report(request):
    if (request.method != "GET"):
        raise SuspiciousOperation
    url1 = request.GET['url_a']
    url2 = request.GET['url_b']
    user = request.user
    article1 = Article.objects.get(article_url = url1)
    article2 = Article.objects.get(article_url = url2)
    if (url1 <= url2):
        Report.objects.create(user=user,article_a=article1, \
                article_b=article2,content=' ')
    else:
        Report.objects.create(user=user,article_a=article2,\
                article_b=article1,content=' ')
    return JsonResponse({'url_a':url1,'url_b':url2,'result':True})



