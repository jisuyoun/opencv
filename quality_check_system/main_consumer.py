import os
import sys
from src.kafka_consumer import create_kafka_consumer, start_consuming_alerts, init_db
from src.config import (
    KAFKA_BOOTSTRAP_SERVERS, DEFECT_ALERTS_TOPIC,
    CONSUMER_GROUP_ID, DATABASE_RELATIVE_PATH
)

"""
kafka 메시지를 수신하고 db에 저장한다.
"""
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, DATABASE_RELATIVE_PATH)

if __name__ == '__main__':
    print("--- main_consuer.py 시스템 시작 ---")
    print(f"데이터베이스 파일 경로: {DATABASE_PATH}")

    db_connection = init_db(DATABASE_PATH)

    if db_connection is None:
        print("데이터베이스 초기화 실패")
        sys.exit(1)

    print("Kafka Consumer 생성 시도...")

    consumer = create_kafka_consumer(
        topic=DEFECT_ALERTS_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id=CONSUMER_GROUP_ID
    )

    if consumer:
        print("Kafka Consumer 생성 완료")
        start_consuming_alerts(consumer, db_connection)
    else:
        print("Kafka Consumer 생성 실패로 시스템 종료")
    
        if db_connection:
            db_connection.close()
            print("데이터베이스 연결 종료")
        
        sys.exit(1)
    print("--- consumer 시스템 완료 ---")