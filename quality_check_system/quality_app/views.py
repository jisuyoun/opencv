from django.shortcuts import render
from .models import Defect 
import os
from quality_check_system import settings
from src.config import IMAGE_SOURCE_RELATIVE_FOLDER, PROCESSED_RELATIVE_FOLDER


def dashboard_view(request):
    """
    품질 관리 대시보드 페이지
    """
    try:
        defects = Defect.objects.all()
        print(defects)
    except Exception as e:
        print(f"데이터베이스에서 불량 기록을 가져오는 중 오류 발생: {e}")
        defect = []

    processed_folder_path = os.path.join(settings.BASE_DIR, PROCESSED_RELATIVE_FOLDER)
    total_processed_images = 0

    if os.path.exists(processed_folder_path) and os.path.isdir(processed_folder_path):
        total_processed_images = len([
            name for name in os.listdir(processed_folder_path)
            if os.path.isfile(os.path.join(processed_folder_path, name)) and name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))
        ])
        print(f"전체 처리 완료 이미지 개수 (estimation) : {total_processed_images}")

        # 불량 제품 개수
        total_defect_images = defects.count()
        print(f"불량 감지 수: {total_defect_images}")

        # 처리 대기 중 이미지 수수
        to_process_folder_path = os.path.join(settings.BASE_DIR, IMAGE_SOURCE_RELATIVE_FOLDER)
        total_to_process_images = 0
        # 폴더가 존재하고 디렉토리인지 확인
        if os.path.exists(to_process_folder_path) and os.path.isdir(to_process_folder_path):
            total_to_process_images = len([
                name for name in os.listdir(to_process_folder_path)
                if os.path.isfile(os.path.join(to_process_folder_path, name)) and name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))
            ])
        print(f"처리 대기 중 이미지 개수: {total_to_process_images}")

        # 템플릿에 전달
        context = {
            'defects': defects,
            'total_processed_images': total_processed_images,
            'total_defect_images': total_defect_images,
            'normal_image_count': max(0, total_processed_images - total_defect_images), # 정상 이미지 수
            'total_to_process_images': total_to_process_images
        }

        return render(request, 'index.html', context)