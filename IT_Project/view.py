from django.shortcuts import render


def home_page(request):
    return render(request, 'home.html')

def about_us(request):
    return render(request, 'about_us.html')
