from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Article, Reply
from .serializers import ArticleSerializer, ReplySerializer
from django.db.models import F, Q
from django.utils import timezone

@api_view(['GET'])
def community_view(request):
    # Fetch distinct tags from articles and hot articles based on click count
    tags = Article.objects.values('tag').distinct()
    hot_articles = Article.objects.all().order_by('-click')[:3]
    # Annotate trending replies with article title and content, ordered by likes
    trending_replies = Reply.objects.annotate(
        article_title=F('article__title'), 
        article_content=F('article__content')
    ).order_by('-likes')[:5]

    # Serialize the articles and replies
    hot_articles_serialized = ArticleSerializer(hot_articles, many=True)
    trending_replies_serialized = ReplySerializer(trending_replies, many=True)

    # Return tags, serialized hot articles, and serialized trending replies
    return Response({
        'Tags': tags,
        'Hot Articles': hot_articles_serialized.data,
        'Trending Replies': trending_replies_serialized.data
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_article(request):
    # Extract title, content, and tag from request data
    title = request.data.get('title')
    content = request.data.get('content')
    tag = request.data.get('tag')

    # Validate title and content
    if not title or not content:
        return Response({'error': 'Title and content are required.'}, status=400)

    # Create article with the provided data and return success response
    article = Article.objects.create(title=title, content=content, tag=tag, user=request.user)
    return Response({'message': 'Article created successfully.', 'article_id': article.pk}, status=201)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_reply(request, pk):
    # Extract content from request data and find the related article
    content = request.data.get('content')
    article = get_object_or_404(Article, pk=pk)

    # Create reply for the article and return success response
    Reply.objects.create(article=article, time=timezone.now(), content=content, user=request.user)
    return Response({'message': 'Reply posted successfully.'}, status=201)

@api_view(['GET'])
def article_list(request):
    # Filter articles by tag if provided, otherwise return all articles
    tag = request.query_params.get('tag')
    if tag:
        articles = Article.objects.filter(tag=tag)
    else:
        articles = Article.objects.all()

    # Serialize and return the articles
    serializer = ArticleSerializer(articles, many=True)
    return Response({'articles': serializer.data})

@api_view(['GET'])
def search_articles(request):
    # Search articles by tag, title, or content containing the query
    query = request.query_params.get('query')
    if query:
        articles = Article.objects.filter(
            Q(tag__icontains=query) | 
            Q(title__icontains=query) | 
            Q(content__icontains=query)
        )
    else:
        articles = Article.objects.none()

    # Serialize and return the search results
    serializer = ArticleSerializer(articles, many=True)
    return Response({'search_results': serializer.data})

@api_view(['GET'])
def article_detail(request, pk):
    # Get article by PK, increment click count, and save
    article = get_object_or_404(Article, pk=pk)
    article.click += 1
    article.save()

    # Serialize the article and its replies, then return them
    article_serializer = ArticleSerializer(article)
    replies = Reply.objects.filter(article=article)
    reply_serializer = ReplySerializer(replies, many=True)

    return Response({
        'Article': article_serializer.data,
        'Replies': reply_serializer.data
    })
