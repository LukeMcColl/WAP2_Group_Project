from django.shortcuts import render
from .models import Post

def newspage(request):
    context = { 'news_list': Post.objects.all() }

    return render(request, 'showtalk/newspage.html', context=context)