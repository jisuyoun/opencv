FROM python:3.10-slim-bookworm

WORKDIR /app

COPY requirements.txt /app/requirements.txt

# 특정 환경에서 문제가 발생할 경우 사용
RUN apt-get update && apt-get install -y --no-install-recommends libgl1-mesa-glx libglib2.0-0 && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

# 컨테이너가 외부에 노출할 포트
EXPOSE 8000

# Django 개발 서버 실행시
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
