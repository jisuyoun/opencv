from django.shortcuts import render
from django.http import HttpResponse

def test_app_view(request):
    print("test_app_view 함수가 실행되었습니다")
    return HttpResponse("<h1>Hello World!</h1><p>이것은 앱 등록 테스트입니다.</p>")

# Create your views here.
