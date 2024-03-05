from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone  # Import timezone module
from .models import Article, Reply

def article_list(request):
    articles = Article.objects.all()
    return render(request, 'article_list.html', {'articles': articles})

def article_detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    replies = Reply.objects.filter(article_id=article_id)
    return render(request, 'article_detail.html', {'article': article, 'replies': replies})

@login_required
def create_article(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        tag = request.POST.get('tag')
        user_id = request.user.id
        article = Article.objects.create(title=title, content=content, tag=tag, user_id=user_id)
        return redirect('article_detail', article_id=article.id)
    return render(request, 'create_article.html')

@login_required
def create_reply(request, article_id):
    if request.method == 'POST':
        content = request.POST.get('content')
        time = timezone.now()  # Use timezone.now() to get current time
        user_id = request.user.id
        reply = Reply.objects.create(content=content, time=time, user_id=user_id, article_id=article_id)
        return redirect('article_detail', article_id=article_id)
    return redirect('article_list')
