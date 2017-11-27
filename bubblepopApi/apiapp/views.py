from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from submodules.url_strip import url_strip
from submodules.crawler import crawl
from submodules.cluster import cluster
from submodules.get_media import save_media
from apiapp.models import Article, UserProfile, UserBlackList, Report, Media, Cluster
from django.views.decorators.csrf import csrf_exempt


import json
import datetime

# Make this value for deploy
NOW_TEST = True


def test(request):
    return HttpResponse("test works")

def check_url(request):
    if (request.method != "GET"):
        raise SuspiciousOperation
    url = request.GET['url']
    url = url_strip(url)
    result = Article.objects.filter(article_url=url).exists()

    if result==True:
        user = request.user
        if user.is_authenticated:
            profile = UserProfile.objects.get(user=user)
            profile.shown_news+=1
            profile.save()

    return JsonResponse({
        'url': url,
        'result': result,
    })


def find_articles(request):

    if (request.method != "GET"):
        raise SuspiciousOperation

    url = request.GET['url']
    user = request.user
    if not user.is_authenticated:
        return HttpResponse("Unauthenticated", status=401)

    profile = UserProfile.objects.get(user=user)
    profile.clicked_news+=1
    profile.save()

    black_list = UserBlackList.objects.filter(user=user)
    article = Article.objects.get(article_url = url)
    media = article.media
    affinity = media.political_view


    if (article.cluster is None):
        date = article.published_at
        articles_for_cluster = Article.objects.filter(
                published_at__gte=date-datetime.timedelta(days=1))
        articles_for_cluster = articles_for_cluster.filter(
                published_at__lte=date+datetime.timedelta(days=1))
        nouns_list = [a.morphemed_content for a in articles_for_cluster]
        cluster_dict = cluster(nouns_list)
        #print(cluster_dict)
        base = Cluster.objects.all().count()
        for key in cluster_dict:
            now_cluster = Cluster.objects.create(cluster_id = base+key)
            for article_idx in cluster_dict[key]:
                articles_for_cluster[article_idx].cluster = now_cluster
                articles_for_cluster[article_idx].save()
        article = Article.objects.get(article_url = url)






    related_articles = Article.objects.filter(cluster=article.cluster).exclude(article_url = article.article_url)

    if related_articles.count()==0:
        return JsonResponse({'success':False,'article_list':None})

    blacked_media = [b.media for b in black_list]
    related_diff = related_articles.exclude(media__in=blacked_media)

    article_list = []
    for related in related_diff:
        article_dict = {}
        article_dict['title'] = related.title
        article_dict['description'] = related.content[:80]
        article_dict['url'] = related.article_url
        article_dict['media_name'] = related.media.name
        article_dict['media_icon'] = related.media.icon
        article_list.append(article_dict)


    return JsonResponse({
        'success': True,
        'article_list': article_list,
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

def update_media(request):
    save_media()
    return JsonResponse({'result':True})



