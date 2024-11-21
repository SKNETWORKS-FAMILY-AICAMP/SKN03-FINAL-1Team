# Base image
FROM python:3.10-slim

# OS 업데이트 및 필수 패키지 설치
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# 작업 디렉토리 생성 및 설정
WORKDIR /app

# 코드 복사
COPY . /app
#COPY ./requirements.txt /app

# Python 패키지 설치
RUN pip3 install --no-cache-dir -r requirements.txt

# 실행 포트 정의 (FastAPI 기본 포트 8000)
EXPOSE 8000

# 컨테이너 상태 확인용 Healthcheck 설정
HEALTHCHECK CMD curl --fail http://localhost:8000/health || exit 1

# FastAPI 애플리케이션 실행
ENTRYPOINT ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
