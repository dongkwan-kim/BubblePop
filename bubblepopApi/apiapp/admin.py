from django.contrib import admin
from apiapp.models import Media, Cluster, Article, \
        CachedArticle, Related, UserBlackList, Report


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('name', 'rss_list', 'political_view', 'icon')


@admin.register(Cluster)
class ClusterAdmin(admin.ModelAdmin):
    list_display = ('cluster_id',)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'media', 'article_url')
    list_filter = ('media',)


@admin.register(CachedArticle)
class CachedArticleAdmin(admin.ModelAdmin):
    list_display = ('article', 'cluster')
    list_filter = ('cluster',)


@admin.register(Related)
class RelatedAdmin(admin.ModelAdmin):
    list_display = ('article_a', 'article_b', 'similarity', 'reports')


@admin.register(UserBlackList)
class UserBlackListAdmin(admin.ModelAdmin):
    list_display = ('user', 'media')
    list_filter = ('user',)


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('user', 'article_a', 'article_b', 'content')
    list_filter = ('user',)

