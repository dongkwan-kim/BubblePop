from django.contrib.auth.models import User
from django.db import models
import binascii
import os


class Media(models.Model):
    name = models.CharField(
        max_length=10,
        verbose_name='이름'
    )
    rss_list = models.TextField(
        verbose_name='RSS 리스트'
    )
    political_view = models.FloatField(
        verbose_name='성향'
    )
    icon = models.URLField(
        verbose_name='아이콘'
    )
    mid = models.IntegerField(
        verbose_name='식별자'
    )

    def __str__(self):
        return self.name


class Cluster(models.Model):
    cluster_id = models.IntegerField(
        verbose_name='클러스터 식별자'
    )

    def __str__(self):
        return str(self.cluster_id)


class Article(models.Model):
    title = models.TextField(
        verbose_name='제목'
    )
    content = models.TextField(
        verbose_name='본문'
    )
    morphemed_content = models.TextField(
        verbose_name='형태소 본문'
    )
    media = models.ForeignKey(
        Media,
        verbose_name='신문사',
        on_delete=models.CASCADE
    )
    writer = models.CharField(
        max_length=10,
        verbose_name='작성자',
        null=True
    )
    published_at = models.DateField(
        auto_now_add=True,
        verbose_name='발행일'
    )
    article_url = models.URLField(
        verbose_name='URL 링크',
        unique=True
    )
    category = models.CharField(
        max_length=10,
        verbose_name='분류',
        default='정치',
        null=True
    )
    cluster = models.ForeignKey(
        Cluster,
        verbose_name='클러스터',
        null=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return str(self.media) + '-' + self.title


class UserBlackList(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='사용자',
        on_delete=models.CASCADE
    )
    media = models.ForeignKey(
        Media,
        verbose_name='언론사',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.user) + '-' + str(self.media)

    def get_media(self):
        return str(self.media)


class Report(models.Model):
    article_a = models.ForeignKey(
        Article,
        related_name='reported_article_a',
        on_delete=models.CASCADE,
        verbose_name='기사A'
    )
    article_b = models.ForeignKey(
        Article,
        related_name='reported_article_b',
        on_delete=models.CASCADE,
        verbose_name='기사B'
    )
    user = models.ForeignKey(
        User,
        verbose_name='사용자',
        null=True,
        on_delete=models.SET_NULL
    )
    content = models.TextField(
        verbose_name='제보내용',
        null=True
    )

    def __str__(self):
        return str(self.user) + '-' + str(self.id)


class UserProfile(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='사용자',
        on_delete=models.CASCADE
    )
    shown_news = models.IntegerField(
        default=0,
        verbose_name='뉴스피드 등장한 뉴스'
    )
    clicked_news = models.IntegerField(
        default=0,
        verbose_name='클릭한 뉴스'
    )
    token = models.CharField(
        max_length=10,
        default='',
        verbose_name='토큰',
    )

    def save_token(self):
        self.token = binascii.hexlify(os.urandom(10)).decode("utf-8")
        self.save()
        return self.token

