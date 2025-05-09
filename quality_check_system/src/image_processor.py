import cv2
import numpy as np

def analyze_image_for_defect(image_path):
    """
    이미지 파일 경로를 받아 불량 여부를 판단하고 불량 정보를 반환한다.
    """

    print(f"이미지 분석 시작: {image_path}")
    try:
        img = cv2.imread(image_path)
        # 이미지를 제대로 읽었는지 확인
        if img is None:
            print(f'이미지 파일을 읽을 수 없습니다: {image_path}')
            return False, {"error": "Image file not found", "image_path": image_path}
        
        
        # 이미지를 HSV 색 공간으로 변환
        hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # 채도만 추출
        saturation = cv2.split(hsv_img)[1]

        # 채도 평균 계산
        average_saturation = np.mean(saturation)

        # 불량 판단 기준
        threshold = 50

        if average_saturation < threshold:
            defect_info = {
                "image_path": image_path,
                "defect_type": "low_saturation",
                "average_saturation": float(average_saturation),
                "message": f"채도 부족 감지: 평균 채도 {average_saturation:.2f} (기준치 {threshold})"
            }
            return True, defect_info
        else:
            # 정상일 경우
            return False, None

    except Exception as e:
        print(f'이미지 분석 중 오류 발생: {e}')
        return False, {"error": str(e), "image_path": image_path}

if __name__ == '__main__':
    print("image_processor 모듈이 테스트 실행")

    path_for_success_test = "data/normal/normal_pencil.jpg"
    path_for_fail_test = "data/defect/defect_pencil.jpg"
    
    # print("정상 이미지 테스트")
    # is_read_success = analyze_image_for_defect(path_for_success_test)
    # print("비정상 이미지 테스트")
    # is_read_fail = analyze_image_for_defect(path_for_fail_test)
    # print("테스트 끝")

    is_defect_normal, defect_info_normal = analyze_image_for_defect(path_for_success_test)
    print(f"{path_for_success_test} - 불량 여부: {is_defect_normal}, 불량 정보: {defect_info_normal}")

    is_defect_defect, defect_info_defect = analyze_image_for_defect(path_for_fail_test)
    print(f"'{path_for_fail_test}' 분석 결과: 불량 여부={is_defect_defect}, 정보={defect_info_defect}")