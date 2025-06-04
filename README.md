# 이미지 품질 관리 시스템

## 1. 시스템 요구사항
- Python: 3.8 이상
- Java: 8 이상
- Apache Kafka: 3.0 버전 이상

## 2. 설치 및 실행 방법
### 2.1. Python 환경 설정
**1. 가상 환경 생성**
```
python -m venv .venv
```

**2. 가상 환경 활성화**
```
.venv\Scripts\activate
```

**3. 필요한 Python 패키지 설치**
```
pip install -r requirements.txt
```

### 2.2. Apache Kafka 실행
**1. Kafka 브로커 실행**
```
.\bin\windows\kafka-server-start.bat config\kraft\server.properties
```

### 2.3. 시스템 실행
**1. Consumer 스크립트 실행**
```
python main_consumer.py
```

**2. Producer 스크립트 실행**
```
python main_producer.py
```

**3. Django 개발 서버 실행**
```
python manage.py runserver
```