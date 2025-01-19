from django.urls import path, include
from main import views

# 이미지를 업로드하자
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    # ex: /main/
    # 웹사이트의 첫화면은 index 페이지이다 + URL이름은 index이다
    path('', views.index, name='index'),
    # URL:8080/blog에 접속하면 blog 페이지 + URL이름은 blog이다
    path('blog/', views.blog, name='blog'),
    # URL:8080/blog/숫자로 접속하면 게시글-세부페이지(posting)
    path('blog/<int:pk>/', views.posting, name="posting"),
    # URL:8080/blog/new_post로 접속하면 새 게시글 작성
    path('blog/new_post/', views.new_post, name='new_post'),
    # URL:8080/blog/숫자/remove로 접속하면 게시글 삭제(remove_post)
    path('blog/<int:pk>/remove/', views.remove_post, name='remove_post'),
    # URL:8080/blog/숫자로 접속하면 게시글-세부페이지(posting)
    path('blog/update/<int:pk>/', views.update_post, name="update_post"),
]

# 이미지 URL 설정
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)