# path 함수를 사용하여 URL 패턴을 정의한다.
from django.urls import path
from . import views

app_name = 'quality_app'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('api/confirm_defect/', views.confirm_defect, name='confirm_defects_api')
]
