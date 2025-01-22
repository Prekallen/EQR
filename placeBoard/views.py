from django.http import Http404
from django.shortcuts import render, redirect
from member.models import BoardMember
from .models import PlaceBoard
from .forms import BoardForm
from django.core.paginator import Paginator

# Create your views here.
# session 검사
def session_check(request):
    if not request.session.get('user'):
        return redirect('/member/login/')
    # 세션에 'user' 키를 불러올 수 없으면, 로그인하지 않은 사용자이므로 로그인 페이지로 리다이렉트 한다.

# 목록
def board_list(request):
    all_boards  = PlaceBoard.objects.all().order_by('-id')
    # 변수명을 all_boards 로 바꿔주었다.
    page        = int(request.GET.get('p', 1))
    # p라는 값으로 받을거고, 없으면 첫번째 페이지로
    pagenator   = Paginator(all_boards, 10)
    # Paginator 함수를 적용하는데, 첫번째 인자는 위에 변수인 전체 오브젝트, 2번째 인자는
    # 한 페이지당 오브젝트 2개씩 나오게 설정
    boards      = pagenator.get_page(page)
    # 처음 2개가 세팅 된다.
    return render(request, 'board_list.html', {"boards":boards})

# 작성
def board_write(request):
    session_check(request)

    if request.method == "POST":
        form = BoardForm(request.POST, request.FILES)

        if form.is_valid():
            # form의 모든 validators 호출 유효성 검증 수행
            user_id = request.session.get('user')
            member = BoardMember.objects.get(pk=user_id)

            board = PlaceBoard()
            board.place = form.cleaned_data['place']
            board.placeNum = form.cleaned_data['placeNum']
            board.address = form.cleaned_data['address']
            board.area = form.cleaned_data['area']
            board.placeImage = form.cleaned_data['placeImage']
            # 검증에 성공한 값들은 사전타입으로 제공 (form.cleaned_data)
            # 검증에 실패시 form.error 에 오류 정보를 저장
            board.writer    = member
            board.save()

            return redirect('/board/list/')

    else:
        form = BoardForm()

    return render(request, 'board_write.html', {'form':form})

 #
def board_detail(request, pk):
    # pk 에 해당하는 글을 가지고 올 수 있게 된다.
    try:
        board = PlaceBoard.objects.get(pk=pk)
    except PlaceBoard.DoesNotExist:
        raise Http404('게시글을 찾을 수 없습니다')
        # 게시물의 내용을 찾을 수 없을 때 내는 오류 message.
    return render(request, 'board_detail.html', {'board':board})

def board_update(request, pk):
    session_check(request)
    try:
        pre_board = PlaceBoard.objects.get(pk=pk)
    except PlaceBoard.DoesNotExist:
        raise Http404('게시글을 찾을 수 없습니다')
    # 게시물의 내용을 찾을 수 없을 때 내는 오류 message.
    if request.method == "POST":

        form = BoardForm(request.POST, request.FILES)

        user_id = request.session.get('user')
        member = BoardMember.objects.get(pk=user_id)
        if form.is_valid():

                new_article=PlaceBoard.objects.filter(id=pk).update(
                    place=form.cleaned_data['place'],
                    placeNum=form.cleaned_data['placeNum'],
                    address=form.cleaned_data['address'],
                    area=form.cleaned_data['area'],
                    placeImage=form.cleaned_data['placeImage'],
                )
        else:

            new_article=PlaceBoard.objects.filter(id=pk).update(

                place=form.cleaned_data['place'],
                placeNum=form.cleaned_data['placeNum'],
                address=form.cleaned_data['address'],
                area=form.cleaned_data['area'],
            )
            '''
                place=request.POST['place'],
                placeNum=request.POST['placeNum'],
                address=request.POST['address'],
                area=request.POST['area'],
                placeImage=request.POST['placeImage'],
                '''
            '''
            board = PlaceBoard()
            board.place = form.cleaned_data['place']
            board.placeNum = form.cleaned_data['placeNum']
            board.address = form.cleaned_data['address']
            board.area = form.cleaned_data['area']
            board.placeImage = form.cleaned_data['placeImage']
            # 검증에 성공한 값들은 사전타입으로 제공 (form.cleaned_data)
            # 검증에 실패시 form.error 에 오류 정보를 저장
            board.writer    = member
            board.save()
            '''

        return redirect('/board/list/')

    else:


        return render(request, 'board_update.html', {'board':pre_board}) #'form':form