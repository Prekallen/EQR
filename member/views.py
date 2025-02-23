from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password

from .forms import LoginForm
from .models import BoardMember
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import BoardMember


# Create your views here.
# email 유효성 검사
def is_valid_email(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False

#manager
def manager(request):
    user_id = request.session.get('user')
    username = get_object_or_404(BoardMember, pk=user_id)
    return render(request, 'manager.html',{'user':username})

# login 페이지
def login(request):
    if request == "POST":
        form = LoginForm(request.POST)
        # 폼 객체, 폼 클래스를 만들 때 괄호에 POST 데이터를 담아준다.
        # POST 안에 있는 데이터가 form 변수에 들어간다.
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            # session_code 검증하기
            request.session['user'] = form.user_id
            return redirect('/manager/')
    else:
        form = LoginForm()
        # 빈 클래스 변수를 만든다.
    return render(request, 'login.html', {'form':form})

#logout
def logout(request):
    if request.session.get('user'):
        del(request.session['user'])

    return redirect('/manager/')    # 아! 로그인을 안했을 때!, user_id 가 없을 때? (세션이 만료되었을 때?)

# 회원가입 페이지
def register(request):
    if request.method == "GET":
        return render(request, 'register.html')
    elif request.method == "POST":
        username = request.POST.get('username', None)
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        re_password = request.POST.get('re_password', None)

        res_data = {}
        if not (username and email and password and re_password):
            res_data['error'] = '모든 값을 입력해야 합니다'
        elif password != re_password:
            res_data['error'] = '비밀번호가 다릅니다.'
        elif is_valid_email(email):
            exist_user = BoardMember.objects.filter(username=username)

            if exist_user:
                res_data['error'] = '아이디가 중복 입니다.'

            else:
                member = BoardMember(
                    username=username,
                    password=make_password(password),
                    email=email,
                )
                member.save()
                return redirect('/manager/')
        else:
            res_data['error'] = '유효하지 않은 이메일 형식입니다.'

    return render(request, 'register.html', res_data)



