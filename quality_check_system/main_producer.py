import os
import sys
import time
import shutil
import urllib.parse

# 현재 파일(main_producer.py)이 있는 디렉토리
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from src.image_processor import analyze_image_for_defect, load_and_analyze_reference_image, load_and_analyze_reference_image
from src.kafka_producer import create_kafka_producer, send_defect_alert

from src.config import (
    KAFKA_BOOTSTRAP_SERVERS, DEFECT_ALERTS_TOPIC,
    REFERENCE_IMAGE_RELATIVE_PATH, # config에서 기준 이미지 상대 경로 임포트
    IMAGE_SOURCE_RELATIVE_FOLDER, PROCESSED_RELATIVE_FOLDER, # 데이터 폴더 상대 경로 임포트
    PROCESSED_IMAGES_MEDIA_SUBFOLDER_NAME, WEB_IMAGE_URL_BASE # 웹 관련 설정 임포트
)

REFERENCE_IMAGE_PATH = os.path.join(BASE_DIR, REFERENCE_IMAGE_RELATIVE_PATH)
IMAGE_SOURCE_FOLDER = os.path.join(BASE_DIR, IMAGE_SOURCE_RELATIVE_FOLDER)
PROCESSED_FOLDER = os.path.join(BASE_DIR, PROCESSED_RELATIVE_FOLDER)
WEB_PROCESSED_IMAGE_FOLDER = os.path.join(BASE_DIR, "media", PROCESSED_IMAGES_MEDIA_SUBFOLDER_NAME)

def process_images_from_folder(folder_path, producer, topic):
    """
    지정된 폴더 내의 이미지 파일들을 처리
    """
    if not os.path.exists(folder_path):
        print(f"지정된 폴더가 존재하지 않습니다: {folder_path} 경로에 폴더 생성중...")
        
        try:
            os.makedirs(folder_path, exist_ok=True)
            print(f"폴더 생성 완료: {folder_path}")
        except OSError as e:
            print(f"폴더 생성 실패: {e}")
            return
        
    # 원본 이동 폴더 생성
    if not os.path.exists(PROCESSED_FOLDER):
        os.makedirs(PROCESSED_FOLDER, exist_ok=True)
        print(f"폴더 생성 완료: {PROCESSED_FOLDER}")

    # 웹 서비스 폴더 생성
    if not os.path.exists(WEB_PROCESSED_IMAGE_FOLDER):
        os.makedirs(WEB_PROCESSED_IMAGE_FOLDER, exist_ok=True)
        print(f"웹 이미지 저장 폴더 생성: {WEB_PROCESSED_IMAGE_FOLDER}")

    print(f"'{folder_path}' 폴더의 이미지 처리 시작")

    for filename in sorted(os.listdir(folder_path)):
        # 이미지 파일 경로 
        image_path = os.path.join(folder_path, filename)

        if os.path.isfile(image_path) and filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            print(f"처리할 파일: {filename}")

            is_defect, result_info = analyze_image_for_defect(image_path)  # 물품이 불량인지 확인
            print(f"결과 정보: {result_info}")
            #print(f"불량 여부: {is_defect}, 결과 정보: {result_info}") 

            web_image_dest_path = os.path.join(WEB_PROCESSED_IMAGE_FOLDER, filename)

            try:
                # 처리된 웹에서 보여주기 위한 이미지 경로로 이동
                shutil.copy(image_path, web_image_dest_path)

                web_image_relative_path = os.path.join(PROCESSED_IMAGES_MEDIA_SUBFOLDER_NAME, filename)

                web_image_url = urllib.parse.urljoin(WEB_IMAGE_URL_BASE, web_image_relative_path.replace('\\', '/'))
                #print(f"web_image_url: {web_image_url}")

                result_info['web_image_url'] = web_image_url

                print(f"웹 서비스 폴더로 이미지 복사 및 URL 추가: {web_image_url}")
            except Exception as e:
                print(f"웹 서비스 폴더로 이미지 복사 중 오류 발생: {e}")
                result_info['web_image_url'] = None 
                result_info['web_copy_error'] = str(e)

            # 불량 여부에 따라 Kafka로 알림 전송
            if is_defect:
                print(f"불량 감지! Kafka로 알림 전송")
                send_defect_alert(producer, topic, result_info)
            elif 'error' in result_info:
                print(f"이미지 분석 중 오류 발생 또는 로드 실패: {result_info.get('error')}")
            
            processed_image_path = os.path.join(PROCESSED_FOLDER, filename)
            try:
                os.rename(image_path, processed_image_path)
                print(f"원본 이미지 이동 완료: {processed_image_path}")
            except OSError as e:
                print(f"원본 이미지 이동 중 오류 발생: {e}")

            time.sleep(0.5)

if __name__ == "__main__":
    #print(REFERENCE_IMAGE_PATH)        # data/normal/normal_reference.jpg
    #print(IMAGE_SOURCE_FOLDER)         # data/to_process/
    #print(PROCESSED_FOLDER)            # data/processed/
    #print(WEB_PROCESSED_IMAGE_FOLDER)  # media\processed_images

    # 정상 채도 계산
    is_analyzed_success = load_and_analyze_reference_image(REFERENCE_IMAGE_RELATIVE_PATH)

    if not is_analyzed_success:
        print("정상 이미지 분석 실패. 프로그램을 종료합니다.")
        sys.exit(1)

    # kafka producer 객체 생성
    producer = create_kafka_producer(KAFKA_BOOTSTRAP_SERVERS)
    if producer:
        print("Kafka producer 생성 완료")

        # 이미지 처리 시작
        process_images_from_folder(IMAGE_SOURCE_FOLDER, producer, DEFECT_ALERTS_TOPIC)
        
        print("모든 메시지 전송 완료 대기...")

        producer.flush()
        producer.close()

        print("시스템 종료")
    else:
        print("Kafka producer 생성 실패")
        sys.exit(1)

    print("main_producer.py 끝")