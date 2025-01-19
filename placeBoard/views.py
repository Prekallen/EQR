from django.http import Http404
from django.shortcuts import render, redirect
from member.models import BoardMember
from .models import PlaceBoard
from .forms import BoardForm

# Create your views here.
# 목록
def board_list(request):
    boards= PlaceBoard.objects.all().order_by('-id')
    return render(request, 'board_list.html', {"boards":boards})

# 작성
def board_write(request):
    if not request.session.get('user'):
        return redirect('/member/login/')
    # 세션에 'user' 키를 불러올 수 없으면, 로그인하지 않은 사용자이므로 로그인 페이지로 리다이렉트 한다.

    if request.method == "POST":
        form = BoardForm(request.POST)

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