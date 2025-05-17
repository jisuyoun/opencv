import cv2
import numpy as np
import os
import sys

try:
    from src.config import SATURATION_TOLERANCE
    from src.config import REFERENCE_IMAGE_RELATIVE_PATH
except ImportError:
    print("상대 경로 임포트 실패.")
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__)) # src 폴더 절대 경로
        project_root = os.path.dirname(current_dir) # 프로젝트 루트 절대 경로

        if project_root not in sys.path:
             sys.path.insert(0, project_root)
             print(f"프로젝트 루트 '{project_root}'를 sys.path에 추가했습니다.")
        else:
             print(f"프로젝트 루트 '{project_root}'는 이미 sys.path에 있습니다.")

        from src.config import SATURATION_TOLERANCE
        from src.config import REFERENCE_IMAGE_RELATIVE_PATH
        print("config 모듈을 절대 경로로 임포트했습니다.")

    except ImportError as e:
        print(f"FATAL ERROR: config 모듈을 임포트할 수 없습니다. 경로 또는 파일 존재 여부를 확인하세요: {e}")
        sys.exit(1) # 오류 코드와 함께 프로그램 종료

# 정상 이미지의 평균 채도
reference_avg_saturation = None

def calculate_average_saturation(image):
    """
    OpenCV 이미지를 받아 평균 채도를 계산한다.
    """
    
    if image is None:
        return None
    try:
        hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        _, saturation, _ = cv2.split(hsv_img)
        avg_saturation = np.mean(saturation)
        return float(avg_saturation)
    except Exception as e:
        print(f"평균 채도 계산 중 오류 발생: {e}")
        return None
    
def load_and_analyze_reference_image(reference_image_path):
    """
    정상 이미지 파일을 로드하고, 평균 채도를 계산하여 reference_avg_saturation에 저장한다.
    """
    global reference_avg_saturation
    print(f"정상 이미지 로드 시작: {reference_image_path}")
    if not os.path.exists(reference_image_path):
        print(f"기준 이미지 파일이 존재하지 않습니다: {reference_image_path}")
        reference_avg_saturation = None
        return False
    reference_img = cv2.imread(reference_image_path)
    if reference_img is None:
        print(f"오류: 기준 이미지 파일을 읽을 수 없습니다 - {reference_image_path}")
        reference_avg_saturation = None
        return False
    
    avg_saturation = calculate_average_saturation(reference_img)
    if avg_saturation is not None:
        reference_avg_saturation = avg_saturation
        print(f"정상 이미지 평균 채도 설정 완료: {reference_avg_saturation}")
        return True
    else:
        print(f"정상 이미지 평균 채도 계산 실패: {reference_avg_saturation}")
        reference_avg_saturation = None
        return False
    
def analyze_image_for_defect(image_path):
    """
    저장된 이미지 파일 경로를 받아 정상 이미지 채도와 비교하여 불량 여부를 판단한다.
    """
    if reference_avg_saturation is None:
        print("오류: 기준 채도 값이 설정되지 않았습니다.")
        return False
    
    print(f"이미지 분석 시작: {image_path}")
    try:
        img = cv2.imread(image_path)
        if img is None:
            print(f"이미지 파일을 열 수 없습니다: {image_path}")
            return False, {"error": "이미지 파일을 찾을 수 없습니다.", "image_path": image_path}
        
        current_avg_saturation = calculate_average_saturation(img)
        if current_avg_saturation is None:
            print(f"채도 계산 실패: {image_path}")
            return False, {"error": "채도 계산 실패", "image_path": image_path}
        
        print(f"현재 이미지 채도: {current_avg_saturation: .2f}, 정상 채도: {reference_avg_saturation: .2f}, 오차: {SATURATION_TOLERANCE}")

        loqwe_bound = reference_avg_saturation - SATURATION_TOLERANCE
        upper_bound = reference_avg_saturation + SATURATION_TOLERANCE

        is_defect = False
        defect_type = None
        message = "정상 제품입니다."

        if current_avg_saturation < loqwe_bound:
            is_defect = True
            defect_type = "저채도"
            message = f"저채도 불량 제품입니다. 현재 채도: {current_avg_saturation: .2f}, 기준 채도: {reference_avg_saturation: .2f}"
        elif current_avg_saturation > upper_bound: 
            is_defect = True
            defect_type = "과채도"
            message = f"과채도 불량 제품입니다. 현재 채도: {current_avg_saturation: .2f}, 기준 채도: {reference_avg_saturation: .2f}"

        if is_defect:
            defect_info = {
                "is_defective": image_path, # 정상 이미지 경로
                "defect_type": defect_type,
                "current_avg_saturation": current_avg_saturation,
                "reference_avg_saturation": reference_avg_saturation,
                "tolerance": SATURATION_TOLERANCE,
                "message": message
            }        
            return True, defect_info
        else:
            return False, {"message": message}
    except Exception as e:
        print(f"이미지 분석 중 오류 발생: {e}")
        return False, {"error": str(e), "image_path": image_path}
    
if __name__ == "__main__":
    current_dir_main = os.path.dirname(os.path.abspath(__file__)) # src 폴더 절대 경로
    project_root_main = os.path.dirname(current_dir_main) # 프로젝트 루트 절대 경로

    #print(f"current_dir: {current_dir_main}")
    #print(f"project_root: {project_root_main}")
    
    normal_image_path = project_root_main + "/data/normal/normal_reference.jpg"
    #print(f"normal_image_path: {normal_image_path}")

    load_and_analyze_reference_image(normal_image_path)
    analyze_image_for_defect(normal_image_path)