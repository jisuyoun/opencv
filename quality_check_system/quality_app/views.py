from django.shortcuts import render
from .models import Defect 
import os
from quality_check_system import settings
from src.config import IMAGE_SOURCE_RELATIVE_FOLDER, PROCESSED_RELATIVE_FOLDER


def dashboard_view(request):
    """
    품질 관리 대시보드 페이지
    """
    # 템플릿에 전달할 기본 context
    context = {
        'defects': [], 
        'total_processed_images': 0,
        'total_defect_images': 0,
        'normal_image_count': 0,
        'total_to_process_images': 0,
        'error_message': None, 
    }

    # 1. 데이터베이스에서 불량 기록 목록을 가져오기
    try:
        defects_queryset = Defect.objects.all() .order_by('-timestamp')

        # --- QuerySet을 JSON 직렬화 가능한 딕셔너리의 리스트 형태로 변환 ---
        defects_list = list(defects_queryset.values())

        # 템플릿에 전달할 변수에 변환된 리스트를 할당
        context['defects'] = defects_list  

    except Exception as e:
        print(f"데이터베이스에서 불량 기록을 가져오는 중 오류 발생: {e}")
        context['error_message'] = f"데이터베이스 오류: {e}"
        context['defects'] = [] 

    # 2. 추가적인 정보
    total_defect_images = len(context['defects'])
    processed_folder_path = os.path.join(settings.BASE_DIR, PROCESSED_RELATIVE_FOLDER)
    total_processed_images = 0
    if os.path.exists(processed_folder_path) and os.path.isdir(processed_folder_path):
        try:
             total_processed_images = len([
                 name for name in os.listdir(processed_folder_path)
                 if os.path.isfile(os.path.join(processed_folder_path, name)) and name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))
             ])
             print(f"전체 처리 완료 이미지 개수 (estimation): {total_processed_images}")
        except Exception as e:
             print(f"처리 완료 이미지 개수 계산 중 오류 발생: {e}")
             context['error_message'] = f"이미지 개수 계산 오류: {e}"
    else:
         print(f"처리 완료 폴더가 존재하지 않거나 디렉토리가 아닙니다: {processed_folder_path}")

    to_process_folder_path = os.path.join(settings.BASE_DIR, IMAGE_SOURCE_RELATIVE_FOLDER)
    total_to_process_images = 0
    if os.path.exists(to_process_folder_path) and os.path.isdir(to_process_folder_path):
         try:
             total_to_process_images = len([
                 name for name in os.listdir(to_process_folder_path)
                 if os.path.isfile(os.path.join(to_process_folder_path, name)) and name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))
         ])
         except Exception as e:
             print(f"처리 대기 중 이미지 개수 계산 중 오류 발생: {e}")
             context['error_message'] = f"대기 이미지 개수 계산 오류: {e}" 
    else:
         print(f"처리 대기 중 폴더가 존재하지 않거나 디렉토리가 아닙니다: {to_process_folder_path}")

    # ----- 템플릿 렌더링 및 HttpResponse 반환 (항상 실행되도록 수정) -----
    context['total_processed_images'] = total_processed_images
    context['total_defect_images'] = total_defect_images
    context['normal_image_count'] = max(0, total_processed_images - total_defect_images)
    context['total_to_process_images'] = total_to_process_images

    print("템플릿 'index.html' 렌더링 시작")
    return render(request, 'index.html', context)