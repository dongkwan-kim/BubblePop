from django.contrib import admin
from apiapp.models import Media, Cluster, Article, \
        Related, UserBlackList, Report, UserProfile


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


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'shown_news', 'clicked_news')

