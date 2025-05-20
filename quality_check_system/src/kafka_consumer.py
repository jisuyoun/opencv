from kafka import KafkaConsumer
import json
import time
import sqlite3
import os
import sys
from src.config import KAFKA_BOOTSTRAP_SERVERS
from src.config import DEFECT_ALERTS_TOPIC
from src.config import CONSUMER_GROUP_ID
from src.config import DATABASE_RELATIVE_PATH

def init_db(db_path):
    """
    SQLite 데이터베이스 초기화
    """
    conn = None
    try:
        # DB 파일을 저장할 경로 생성
        db_dir = os.path.dirname(db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
        
        print(f"데이터베이스 위치: {db_dir}")
        
        # SQLite DB 연결
        conn = sqlite3.connect(db_path)

        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # defects 테이블 생성
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS defects_table (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                image_path TEXT,          -- 원본 파일 경로
                web_image_url TEXT,       -- 웹에서 접근 가능한 이미지 URL
                defect_type TEXT,         -- 불량 유형 
                current_saturation REAL,  -- 감지된 현재 이미지 채도
                reference_saturation REAL,-- 기준 이미지 채도
                tolerance REAL,           -- 허용 오차
                message TEXT,             -- 불량 설명 메시지
                timestamp DATETIME        -- 감지 타임스탬프
            )
        ''')
        conn.commit()

        print(f"데이터베이스 초기화 완료: {db_path}")
        return conn
    except sqlite3.Error as e:
        print(f"데이터베이스 초기화 실패: {e}")
        if conn:
            conn.close()
        return None
    
def save_defect_to_db(conn, defect_info):
    """
    불량 정보를 SQLite DB에 저장
    """
    try:
        cursor = conn.cursor()

        image_path = defect_info.get("image_path")
        web_image_url = defect_info.get("web_image_url")

        defect_type = defect_info.get("defect_type")
        current_saturation = defect_info.get("current_saturation")
        reference_saturation = defect_info.get("reference_saturation")
        tolerance = defect_info.get("tolerance")
        message = defect_info.get("message")
        timestamp = defect_info.get("timestamp")

        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp / 1000))

        # INSERT
        cursor.execute('''
            INSERT INTO defects_table (image_path, web_image_url, defect_type, current_saturation, reference_saturation, tolerance, message, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)               
        ''', image_path, web_image_url, defect_type, current_saturation, reference_saturation, tolerance, message, timestamp)

        conn.commit()
        print(f"불량 정보 저장 성공: {URL: {web_image_url}}")

    except Exception as e:
        print(f"불량 정보 저장 실패: {e}")
        if conn:
            conn.rollback()
            conn.close()
        return None
    
def create_kafka_consumer(topic=DEFECT_ALERTS_TOPIC, bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS, group_id=CONSUMER_GROUP_ID):
    """
    Kafka consumer 객체를 생성한다.
    """
    print(f"Kafka consumer 생성 시도: 토픽='{topic}' 브로커='{bootstrap_servers}', 그룹='{group_id}'")

    try:
        consumer = KafkaConsumer(
            topic,
            bootstrap_servers=bootstrap_servers,
            group_id=group_id,
            value_deserializer=lambda x: json.loads(x.decode("utf-8")),
            auto_offset_reset='earliest',
            enable_auto_commit=True  # 메시지를 처리한 후 자동으로 오프셋 커밋
        )
        print("Kafka consumer 생성 성공. 토픽: '{topic}', 그룹: '{group_id}'")
        return consumer
    
    except Exception as e:
        print(f"Kafka consumer 생성 실패: {e}")
        return None

def start_consuming_alerts(consumer, db_conn):
    """
    Kafka 토픽에서 메시지를 지속적으로 수신하고 처리한다.
    수신된 불량 정보를 db_conn을 사용하여 데이터베이스에 저장한다.
    """
    if consumer is None:
        print("Kafka consumer가 초기화되지 않아 메시지를 수신할 수 없습니다.")
        return
    if db_conn is None:
        print("데이터베이스 연결이 없어 불량 정보를 저장할 수 없습니다.")
        return
    
    print("Kafka consumer 시작: 메시지 수신 대기 중...")
    try:
        for message in consumer:
            defect_info = message.value

            print(f"불량 알림 메시지 수신:")
            print(f"  토픽: {message.topic}, 파티션: {message.partition}, 오프셋: {message.offset}")
            print(f"  수신 시간: {time.ctime(message.timestamp / 1000) if message.timestamp is not None else 'N/A'}")
            print(f"  내용: {defect_info}")
            print("=" * 40)

            if db_conn:
                save_defect_to_db(db_conn, defect_info)
            else:
                print("DB 연결이 없어 불량 정보를 저장할 수 없습니다.")
    except KeyboardInterrupt:
        print("Kafka consumer 중지 요청 받음")
    except Exception as e:
        print(f"메시지 수신 및 처리 중 오류 발생: {e}")
    finally:
        print("Kafka consumer 종료")
        consumer.close()
        if db_conn:
            db_conn.close()
        print("데이터베이스 연결 종료")

if __name__ == "__main__":
    print("----Kafka Consumer 테스트 시작----")

    # 상대 경로를 절대 경로로 변환
    db_path = os.path.join(os.path.dirname(__file__), DATABASE_RELATIVE_PATH)
    print(f"테스트에 사용할 SQLite DB 경로: {db_path}")

    # 데이터베이스 초기화
    db_conn = init_db(db_path)
    if db_conn is None:
        print("데이터베이스 초기화 실패")
        sys.exit(1)

    # Kafka consumer 생성
    consumer = create_kafka_consumer()
    if consumer is None:
        print("Kafka consumer 생성 실패")
        sys.exit(1)

    # Kafka consumer 시작
    start_consuming_alerts(consumer, db_conn)