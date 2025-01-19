from django.db import models

# Create your models here.
class Question(models.Model):
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)

#게시글(Post)엔 제목(postname), 내용(contents)이 존재합니다
class Post(models.Model):
    postname = models.CharField(max_length=50)
    contents = models.TextField()
    #게시글 Post에 이미지 추가
    mainphoto = models.ImageField(blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    #게시글의 제목(postname)이 Post object 대신하기
    def __str__(self):
        return self.postname
    #pass