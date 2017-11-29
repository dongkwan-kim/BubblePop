from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from numpy import argsort
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from submodules.url_strip import url_strip
from submodules.crawler import crawl
from submodules.cluster import cluster
from submodules.get_media import save_media
from apiapp.models import Article, UserProfile, UserBlackList, Report, Media, Cluster
from django.views.decorators.csrf import csrf_exempt


import json
import datetime


def test(request):
    return HttpResponse("test works")


@csrf_exempt
def check_url(request):

    if (request.method != "POST"):
        raise SuspiciousOperation

    url = request.POST['url']
    url = url_strip(url)
    result = Article.objects.filter(article_url=url).exists()

    if result:
        token = request.POST['token']
        profile = UserProfile.objects.filter(token=token)
        if profile:
            profile = profile[0]
            profile.shown_news += 1
            profile.save()

    return JsonResponse({
        'url': url,
        'result': result,
    })


@csrf_exempt
def find_articles(request):

    if (request.method != "POST"):
        raise SuspiciousOperation

    url = request.POST['url']
    url = url_strip(url)
    token = request.POST['token']
    profile = UserProfile.objects.filter(token=token)
    if profile:
        profile = profile[0]
        user = profile.user
    else:
        return JsonResponse(
                status=401,
                data={'success': False}
            )


    # for debug don't erase
    #user = request.user
    #url = request.GET['url']
    #url = url_strip(url)
    #profile = UserProfile.objects.get(user=user)

    profile.clicked_news += 1
    profile.save()

    black_list = UserBlackList.objects.filter(user=user)
    article = Article.objects.get(article_url=url)
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

        base = Cluster.objects.all().count()
        for key in cluster_dict:
            now_cluster = Cluster.objects.create(cluster_id = base+key)
            for article_idx in cluster_dict[key]:
                articles_for_cluster[article_idx].cluster = now_cluster
                articles_for_cluster[article_idx].save()
        article = Article.objects.get(article_url = url)

    related_articles = Article.objects.filter(cluster=article.cluster).exclude(article_url = article.article_url)

    if related_articles.count() == 0:
        return JsonResponse({'success':False,'article_list':None})

    blacked_media = [b.media for b in black_list]
    related_diff = related_articles.exclude(media__in=blacked_media)
    reported = Report.objects.filter(user=user,article_a=article)
    related_diff = related_diff.exclude(id__in=[a.article_b.id for a in reported])
    reported = Report.objects.filter(user=user,article_b=article)
    related_diff = related_diff.exclude(id__in=[a.article_a.id for a in reported])

    if len(related_diff) > 10:
        tfidf = TfidfVectorizer(norm='l2', min_df=0, use_idf=True, smooth_idf=False,
                                sublinear_tf=True, tokenizer=lambda doc: doc.split(' '))
        rel_articles_inc_original = [article] + related_diff
        X = tfidf.fit_transform(rel_articles_inc_original)
        top_sim_args = argsort(cosine_similarity(X)[0])[::-1][1:11]
        new_articles = []
        for idx in top_sim_args:
            new_articles.append(rel_articles_inc_original[idx])
        related_diff = new_articles

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
        'black_list': [str(m) for m in blacked_media],
    })


@csrf_exempt
def blacklist(request):
    token = request.POST['token']
    profile = UserProfile.objects.filter(token=token)
    if profile:
        user = profile[0].user
        black_list = UserBlackList.objects.filter(user=user)
        result = True
    else:
        black_list = []
        result = False

    return JsonResponse({
        "black_list": [n.media.mid for n in list(black_list)],
        "result": result,
    })


@csrf_exempt
def change_blacklist(request):

    if (request.method != "POST"):
        raise SuspiciousOperation

    media_list = request.POST.getlist('media[]')
    token = request.POST['token']
    profile = UserProfile.objects.filter(token=token)
    if profile:
        user = profile[0].user
    else:
        return HttpResponse("Unauthenticated", status=401)

    res = []
    for media_id in media_list:
        media = Media.objects.get(mid=media_id)
        black_list = UserBlackList.objects.filter(user=user, media=media)
        if (black_list.exists()):
            black_list.delete()
            res.append({
                'media': media_id,
                'result': False
            })
        else:
            UserBlackList.objects.create(user=user, media=media)
            res.append({
                'media': media_id,
                'result': True
            })

    return JsonResponse(json.dumps(res, ensure_ascii=False), safe=False)


@csrf_exempt
def report(request):

    if (request.method != "POST"):
        raise SuspiciousOperation

    token = request.POST['token']
    profile = UserProfile.objects.filter(token=token)
    if profile:
        user = profile[0].user
    else:
        return HttpResponse("Unauthenticated", status=401)

    url1 = url_strip(request.POST['url_a'])
    url2 = request.POST['url_b']
    content = request.POST['content']

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

