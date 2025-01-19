from django import forms

from member.models import BoardMember
from django.contrib.auth.hashers import check_password



class BoardForm(forms.Form):
    # 입력받을 값 [place, placeNum, address, area, placeImage, partNum, duplPartNum,
    place = forms.CharField(error_messages={
        'required': '업체명을 입력하세요.'
    }, max_length=50, label="업체명")
    placeNum = forms.CharField(error_messages={
        'required': '업체 전화 번호를 입력하세요.'
    }, max_length=15, label="전화 번호", widget=forms.TextInput(attrs={'placeholder': '010-1234-5678'}))
    address = forms.CharField(error_messages={
        'required': '주소를 입력하세요.'
    }, max_length=100, label="주소")
    area = forms.CharField(error_messages={
        'required': '지역을 입력하세요.'
    }, max_length=50, label="지역")
    placeImage = forms.ImageField(error_messages={
        'required': '업체 사진을 올려주세요.'
    }, label="업체 사진")


    '''    
    place       = models.CharField(max_length=200, verbose_name="업체명")
    placeNum    = PhoneNumberField(verbose_name="업체 전화 번호")
    address     = models.TextField(verbose_name="주소")
    area        = models.CharField(max_length=50, verbose_name="지역")
    placeImage  = models.ImageField(upload_to='photos/', verbose_name="업체 사진")
    '''