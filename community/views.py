from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import *

tag_data = {
    'Vehicle Types': ['Sedan', 'SUV', 'Truck', 'Coupe', 'Convertible', 'Hatchback'],
    'Brands': ['Toyota', 'Honda', 'Ford', 'BMW', 'Mercedes-Benz', 'Audi'],
    'Performance': ['Sports Cars', 'Muscle Cars', 'Electric Vehicles (EVs)', 'Hybrid Cars'],
    'Features': ['Autonomous Vehicles', 'Electric Cars', 'Self-driving Cars', 'Car Modifications'],
    'Events': ['Auto Shows', 'Car Races', 'Motor Expos', 'Car Auctions'],
}

# Create tags with categories
for category, tags in tag_data.items():
    for tag_name in tags:
        Tag.objects.get_or_create(name=tag_name, category=category)


def community(request):
    #tags
    tags = Tag.objects.all()

    # 按创建时间降序排序，获取前三篇文章
    articles_by_time = Article.objects.all().order_by('-created_at')[:3]

    # 按点击量降序排序，获取前三篇文章
    articles_by_views = Article.objects.all().order_by('-views_count')[:3]

    return render(request, 'community.html', {
        'articles_by_time': articles_by_time,
        'articles_by_views': articles_by_views,
        'tags': tags
    })

def article_list(request):
    tag_name = request.GET.get('tag')
    if tag_name:
        tag = get_object_or_404(Tag, name=tag_name)
        articles = tag.articles.all()
    else:
        articles = Article.objects.all()
    return render(request, 'article_list.html', {'articles': articles, 'tag_name': tag_name})

def article_detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    article.views_count += 1
    article.save()
    replies = Reply.objects.filter(article_id=article)
    return render(request, 'article_detail.html', {'article': article, 'replies': replies})

@login_required
def create_article(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        selected_tags = request.POST.getlist('tags')

        if not title or not content:
            return HttpResponse('Title and content are required.', status=400)

        article = Article.objects.create(title=title, content=content, user=request.user) 

        for tag_name in selected_tags:
            tag = Tag.objects.get(name=tag_name)
            article.tags.add(tag)

        return redirect('article_detail', article_id=article.pk)
    else:
        tags = Tag.objects.all()  # 获取所有现有标签，传递给模板，以便在表单中显示
        return render(request, 'create_article.html', {'tags': tags})

@login_required
def create_reply(request, article_id):
    if request.method == 'POST':
        content = request.POST.get('content')
        article = get_object_or_404(Article, pk=article_id)
        Reply.objects.create(ArticleID=article, Time=timezone.now(), Content=content)
        return redirect('article_detail', article_id=article_id)
    else:
        return redirect('article_detail', article_id=article_id)