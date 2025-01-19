from tracemalloc import get_object_traceback

from django.shortcuts import render, get_object_or_404, redirect
from main.models import Question, Post
from django.http import HttpResponse
from django.template import loader
# Create your views here.
#index.html 페이지를 부르는 index 함수
def index(request):
    template = loader.get_template("main/index.html")
    context = {

    }
    return HttpResponse(template.render(context, request))
'''
    question_list = Question.objects.order_by('-create_date')
    context = {'question_list': question_list}
    return render(request, 'index.html', context)
'''
# blog.html 페이지를 부르는 blog 함수
def blog(request):
    #모든 Post를 가져와 postlist에 저장
    postlist= Post.objects.all()
    #blog.html페이지 열 때, 모든 Post인 postlist도 같이 가져옴
    return render(request, 'main/blog.html', {'postlist': postlist})

# blog의 게시글(posting)을 부르는 posting 함수
def posting(request, pk):
    # 게시글(Post) 중 pk(primary_key)를 이용해 하나의 게시글(post)를 검색
    post = Post.objects.get(pk=pk)
    # posting.html 페이지를 열 때, 찾아낸 게시글(post)을 post라는 이름으로 가져옴
    return render(request, 'main/posting.html', {'post':post})

# 글쓰기(new_post)를 부르는 new_post 함수
def new_post(request):
    if request.method == 'POST':
        if request.POST['mainphoto']:
            new_article=Post.objects.create(
                postname=request.POST['postname'],
                contents=request.POST['contents'],
                mainphoto=request.POST['mainphoto'],
            )
        else:
            new_article=Post.objects.create(
                postname=request.POST['postname'],
                contents=request.POST['contents'],
                mainphoto=request.POST['mainphoto'],
            )
        return redirect('/blog/')
    return render(request, 'main/new_post.html')

#삭제(remove_post)를 부르는 remobe_post 함수
def remove_post(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('/blog/')
    return render(request, 'main/remove_post.html', {'Post': post})

def update_post(request, pk):
    # 게시글(Post) 중 pk(primary_key)를 이용해 하나의 게시글(post)를 검색
    post = Post.objects.get(pk=pk)
    if request.method == 'POST':
        if request.POST['mainphoto']:
            new_article=Post.objects.update(
                postname=request.POST['postname'],
                contents=request.POST['contents'],
                mainphoto=request.POST['mainphoto'],
            )
        else:
            new_article=Post.objects.update(
                postname=request.POST['postname'],
                contents=request.POST['contents'],
                mainphoto=request.POST['mainphoto'],
            )
        return redirect('/blog/')
    return render(request, 'main/update_post.html', {'post':post})


'''
def main(request):
    return'''