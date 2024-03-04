from django.shortcuts import render, redirect, get_object_or_404
from .forms import EditProfileForm, CustomUserCreationForm, CarPostForm, CommentForm
from .models import Transaction, CarPost, Tag
from django.contrib.auth import login as auth_login
from django.views.generic import ListView, DetailView

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

#login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile_view')
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})

#login_required
def view_transactions(request):
    transactions = Transaction.objects.filter(user=request.user)
    return render(request, 'transactions.html', {'transactions': transactions})

def transaction_detail(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    return render(request, 'transactions/detail.html', {'transaction': transaction})

def search_by_tag(request):
    tag_name = request.GET.get('tag')  # 假设从查询参数 "tag" 获取标签名
    if tag_name:
        tag = Tag.objects.filter(name=tag_name).first()
        if tag:
            car_posts = tag.car_posts.all()
        else:
            car_posts = CarPost.objects.none()  # 如果没有找到标签，返回空查询集
    else:
        car_posts = CarPost.objects.none()  # 如果没有提供标签名，也返回空查询集

    return render(request, 'community/search_results.html', {'car_posts': car_posts, 'tag': tag_name})

class CarPostListView(ListView):
    model = CarPost
    template_name = 'community/carpost_list.html'  # 指定要使用的模板

#login_required
def create_carpost(request):
    if request.method == 'POST':
        form = CarPostForm(request.POST)
        if form.is_valid():
            carpost = form.save(commit=False)
            carpost.author = request.user  # 假设 CarPost 模型有一个名为 author 的 ForeignKey 指向 User 模型
            carpost.save()
            return redirect('carpost_list')  # 重定向到帖子列表页面
    else:
        form = CarPostForm()
    return render(request, 'community/create_carpost.html', {'form': form})

def carpost_detail(request, pk):
    carpost = get_object_or_404(CarPost, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = carpost  # 设置评论关联的 CarPost
            comment.author = request.user  # 假设 Comment 模型有一个 'author' 字段
            comment.save()
            return redirect('carpost_detail', pk=carpost.pk)  # 重定向回帖子详情页面
    else:
        form = CommentForm()
    return render(request, 'community/carpost_detail.html', {'carpost': carpost, 'form': form})