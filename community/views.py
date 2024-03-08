from django.db.models import F
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import ArticleSerializer, ReplySerializer


@api_view(['GET'])
def community_view(request):
    #显示所有tag
    tags = Article.objects.values('tag').distinct()

    # 显示热门前三篇文章
    hot_article = Article.objects.all().order_by('-click')[:3]

    trending_replies = Reply.objects.values('article_title', 'article_content', 'user__username', 'likes').annotate(article_title=F('article__title'), article_content=F('article__content')).order_by('-likes')[:3]

    return Response({
        'Hot topic': tags,
        'Hot Articles': hot_article,
        'Trending Discussion': trending_replies
    })


@api_view(['GET'])
@login_required
def create_article(request):
    if request.method == 'POST':
        title = request.dataT.get('title')
        content = request.data.get('content')
        #新的创建完加到数据库
        tag = request.data.get('tag')

        if not title or not content:
            return Response({'error': 'Title, and content are required.'}, status=400)

        article = Article.objects.create(title=title, content=content, tag=tag, user=request.user)
        return Response({'message': 'Article created successfully.', 'article_id': article.article_id}, status=201)
    else:
        return Response({'error': 'Create failed.'}, status=405)


@api_view(['GET'])
@login_required
def create_reply(request):
    if request.method == 'POST':
        article_id = request.data.get('article_id')  # 从请求中获取文章ID
        content = request.data.get('content')

        try:
            article = Article.objects.get(article_id=article_id)
        except Article.DoesNotExist:
            return Response({'error': 'Article not found.'}, status=404)

        Reply.objects.create(article=article, time=timezone.now(), content=content)
        return Response({'message': 'Reply posted successfully.'}, status=201)
    else:
        return Response({'error': 'Method not allowed.'}, status=405)


@api_view(['GET'])
def article_list(request):

    if request.method == 'GET':
        tag = request.GET.get('tag')
        result_articles = Article.objects.filter(tag=tag)
    else:
        result_articles = Article.objects.all()

    serializer = ArticleSerializer(result_articles, many=True)
    return Response({'result_articles': serializer.data})

@api_view(['GET'])
def search_articles(request):#搜索没问题 跳转未知

    if request.method == 'GET':
        query = request.GET.get('query')
        # tag = request.GET.get('tag')
        # 处理搜索结果
        from django.db.models import Q
        result_articles = Article.objects.filter(
            Q(tag__icontains=query) | Q(title__icontains=query) | Q(content__icontains=query)
        )
        # result_articles = Article.objects.filter(tag__icontains=tag)
    else:
        result_articles = Article.objects.none()

    serializer = ArticleSerializer(result_articles, many=True)
    return Response({'result_articles': serializer.data})


@api_view(['GET'])
def article_detail(request, article_id):
    article = get_object_or_404(Article, article_id=article_id)
    article.click += 1
    article.save(update_fields=['click'])

    # 使用ArticleSerializer序列化文章
    article_serializer = ArticleSerializer(article).data

    # 获取与文章关联的回复数据
    replies = Reply.objects.filter(article=article)
    reply_serializer = ReplySerializer(replies, many=True).data

    # 将文章和回复数据合并在响应中
    response_data = {
        'article': article_serializer,
        'replies': reply_serializer,
    }

    return Response(response_data)


