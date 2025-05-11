# kafka 브로커 주소
KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092'

# 불량 알림 메시지를 보낼 Kafka 토픽
DEFECT_ALERTS_TOPIC = 'product_defect_alerts'

# Consumer 그룹 ID
CONSUMER_GROUP_ID = 'quality-check-group'

# 이미지 분석 - 채도 비교 오차 범위
SATURATION_TOLERANCE = 10

# --- 파일 및 폴더 경로 ---
# 기준 이미지 파일 경로
REFERENCE_IMAGE_RELATIVE_PATH = 'data/normal/normal_reference.jpg'

# 데이터베이스 파일 경로
DATABASE_RELATIVE_PATH = 'quality_defects.db'

# 분석할 이미지들이 저장된 폴더 경로
IMAGE_SOURCE_RELATIVE_FOLDER = 'data/to_process/'

# 이미지를 처리한 후 원본을 이동시킬 폴더 경로
PROCESSED_RELATIVE_FOLDER = 'data/processed/'

# Producer가 처리된 이미지를 복사할 경로
PROCESSED_IMAGES_MEDIA_SUBFOLDER_NAME = 'processed_images'

# 웹에서 이미지에 접근할 url
WEB_IMAGE_URL_BASE = '/media/'