from tracemalloc import get_object_traceback

from django.core.paginator import Paginator
from django.db.models import FloatField, F, ExpressionWrapper
from django.db.models.functions import ACos, Cos, Radians, Sin
from math import radians, sin, cos, sqrt, atan2
from django.shortcuts import render, get_object_or_404, redirect
# from main.models import Question, Post
from django.http import HttpResponse, JsonResponse
from django.template import loader

from django.utils import timezone
from django.db.models import Q
from main.forms import ParticipantForm
from main.models import Participant
from placeBoard.models import PlaceBoard
from django.contrib import messages
import datetime


# Create your views here.
#index.html 페이지를 부르는 index 함수
# 1-1. 갓파더위크 설명
def godfather_info(request):

    return render( request, 'godfather_info.html')

def event_map(request):
    places = PlaceBoard.objects.all()  # 모든 매장을 가져옴
    unique_areas = places.values_list('area', flat=True).distinct()
    return render(request, 'event_map.html', {'places': places, 'unique_areas': unique_areas})

def haversine(lat1, lon1, lat2, lon2):  # 거리 계산
    R = 6371.0  # 지구 반지름(km)
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance

# 3-A-1. 전체 업장 리스트 노출
def place_list(request):
    query = request.GET.get('q')
    lat = request.GET.get('lat')
    lng = request.GET.get('lng')


    if query:
        # 검색어가 있는 경우
        place_list = PlaceBoard.objects.filter(place__icontains=query)
    else:
        # 검색어가 없는 경우
        place_list = PlaceBoard.objects.all()

        if lat and lng:
            try:
                user_lat = float(lat)
                user_lng = float(lng)

                # 위도와 경도 값이 없는 객체 제외
                place_list = place_list.exclude(latitude__isnull=True).exclude(longitude__isnull=True)

                places_with_distance = []
                for place in place_list:
                    dist = haversine(user_lat, user_lng, place.latitude, place.longitude)
                    place.distance = dist  # 장소 객체에 거리 속성 추가
                    try:
                        places_with_distance.append(place)
                    except Exception as e:
                        print(f"Error appending place to list: {e}")

                # 거리 순으로 정렬
                places_with_distance.sort(key=lambda x: x.distance)
                place_list = places_with_distance

            except (ValueError, TypeError) as e:
                print(f"위치 정보 변환 오류: {e}")

    paginator = Paginator(place_list, 10)  # 기본 목록을 사용
    page = request.GET.get('page')
    places = paginator.get_page(page)

    # 현재 페이지 번호를 정수형으로 변환
    current_page = places.number

    # 총 페이지 수
    total_pages = paginator.num_pages

    # 페이지 그룹 계산
    page_group = (current_page - 1) // 10
    start_page = page_group * 10 + 1
    end_page = min(start_page + 9, total_pages)
    page_numbers = range(start_page, end_page + 1)

    # 기존의 GET 파라미터에서 'page'를 제거하여 query_string 생성
    query_params = request.GET.copy()
    if 'page' in query_params:
        del query_params['page']
    query_string = query_params.urlencode()

    context = {
        'places': places,
        'page_numbers': page_numbers,
        'has_previous_group': start_page > 1,
        'has_next_group': end_page < total_pages,
        'previous_group_page': start_page - 1,
        'next_group_page': end_page + 1,
        'query_string': query_string,
    }

    return render(request, 'placeList.html', context)

# 3-B-1. 개인 정보 제공 동의 페이지 노출 (팝업 or 페이지)
def event_check(request):

    return render( request, 'eventCheck.html')

# 3-B-2. 개인 정보 인력 (이름, 휴대폰 번호)
def events(request):
    if request.method == "GET":
        form = ParticipantForm()
        # placeBoard 업체 리스트 조회 (가정: PlaceBoard 모델을 사용)
        place_list = PlaceBoard.objects.all()

        return render(request, 'event.html', {'form':form, 'place_list':place_list})
    elif request.method == "POST":
        form = ParticipantForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            num = form.cleaned_data.get('num')
            # mail = form.cleaned_data.get('mail')
            place_id = form.cleaned_data.get('placeId')
            now = timezone.now()
            time_threshold = now - datetime.timedelta(hours=12)  # 예: 12시간 이내 중복 검사
            place_board = PlaceBoard.objects.get(id=place_id)
            dupl = False


            # 중복 여부 검사
            duplicate_time_check = Participant.objects.filter(
                Q(name=name) & Q(num=num) & Q(placeId=place_id) & Q(date__gte=time_threshold)
            ).exists()
            # 중복 체크 후 중복 여부 및 중복 등록
            duplicate_check = Participant.objects.filter(
                Q(name=name) & Q(num=num) & Q(placeId=place_id)
            ).exists()

            if duplicate_time_check:
                messages.error(request, "중복된 참가자가 이미 등록되었습니다.")
            else:
                dupl = duplicate_check  # 중복 여부 설정
                if duplicate_check:
                    #기존 중복 되어 있던 참가자 중복 여부 상태 변경
                    existing_participant = Participant.objects.get(
                        Q(name=name) & Q(num=num) & Q(placeId=place_id)
                    )
                    if existing_participant.dupl is False:
                        existing_participant.dupl = True
                        existing_participant.save()

                        # 중복 참여 인원 추가
                        place_board = PlaceBoard.objects.get(id=place_id)
                        place_board.duplPartNum += 1
                        place_board.save()

                else :

                    # 새로운 참가자 생성 및 저장
                    new_participant(name,num,place_id,dupl) # mail,

                    #placeBoard 참가자 인원 증가
                    place_board = PlaceBoard.objects.get(id=place_id)
                    place_board.partNum += 1
                    place_board.save()

                    messages.success(request, "참가자가 성공적으로 등록되었습니다.")
                    return redirect('event_list')  # 이벤트 리스트 페이지로 리디렉션 (적절한 URL 이름으로 변경)

def new_participant(name, num, place_id, dupl): #mail,
    save_participant = Participant(
        name=name,
        num=num,
        # mail=mail,
        placeId=place_id,
        date=timezone.now(),
        dupl=dupl,
    )
    save_participant.save()

def autocomplete(request):
    if 'term' in request.GET:
        qs = PlaceBoard.objects.filter(place__icontains=request.GET.get('term'))
        names = list()
        for place in qs:
            names.append({'label': place.place, 'value': place.id})
        return JsonResponse(names, safe=False)
    return JsonResponse([], safe=False)

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
