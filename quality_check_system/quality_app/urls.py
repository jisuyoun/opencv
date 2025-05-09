# path 함수를 사용하여 URL 패턴을 정의한다.
from django.urls import path
from . import views

app_name = 'quality_app'

urlpatterns = [
    # 이 프로젝트에서는 '' 패턴은 웹사이트의 루트 경로('/')에 매핑된다.
    path('', views.test_app_view, name='test_dashboard'),
]
