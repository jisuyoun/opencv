from kafka import KafkaProducer
import json
import time
import os
import sys

from src.config import KAFKA_BOOTSTRAP_SERVERS
from src.config import DEFECT_ALERTS_TOPIC

def create_kafka_producer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS):
    """
    kafka producer 객체를 생성한다.
    """
    print(f"Kafka producer 생성 시도: 브로커={bootstrap_servers}")

    try:
        producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda x: json.dumps(x).encode("utf-8")
        )
        print("Kafka producer 생성 성공")
        return producer
    except Exception as e:
        print(f"Kafka producer 생성 실패: {e}")
        return None

def send_defect_alert(producer, topic, defect_info):
    """
    불량에 대한 정보를 kafka 토픽으로 전송한다.
    """
    if producer is None:
        print("producer가 초기화되지 않아 메시지를 보낼 수 없습니다.")
        return
    
    print(f"'{topic}' 토픽으로 불량 알림 전송 시도...")

    try:
        defect_info["timestamp"] = int(time.time() * 1000) # 현재 시간
        future = producer.send(topic, value=defect_info)
        result = future.get(timeout=10) # 10초 대기
        print(f"불량 알림 전송 성공: 토픽='{result.topic}', 파티션={result.partition}, 오프셋={result.offset}")
    except Exception as e:
        print(f"불량 알림 전송 실패: {e}")

if __name__ == "__main__":
    print("----Kafka Producer 테스트 시작----")

    print(f"테스트에 사용할 Kafka 브로커: {KAFKA_BOOTSTRAP_SERVERS}")
    print(f"테스트에 사용할 Kafka 토픽: {DEFECT_ALERTS_TOPIC}")
    
    test_producer = create_kafka_producer()
    if test_producer:
        print("Kafka producer 테스트 메시지 전송 시도...")

        test_defect_data = {
            "image_path": "/data/normal/normal_reference.jpg",
            "web_image_url": "/data/defect/defect_pencil.jpg",
            "defect_type": "TestSaturationLow",
            "current_saturation": 35.5,
            "reference_saturation": 100.0,
            "tolerance": 10,
            "message": "This is a test message from kafka_producer.py __main__ block.",
        }

        send_defect_alert(test_producer, DEFECT_ALERTS_TOPIC, test_defect_data)

        test_producer.flush()
        test_producer.close()
        print("producer 테스트 메시지 전송 완료 및 producer 종료")
    else:
        print("producer 생성 실패 및 테스트 종료")

    print("----Kafka Producer 테스트 끝----")