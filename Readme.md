# Pika-two Back-end
## 1. 개발환경 설정
### 소스 디렉토리 내에서 아래 코드 실행
```sh
pika-two-BE$ docker build -t pikatwo-be . # 도커 이미지 빌드
pika-two-BE$ docker run --name pikatwo-be -d -p 5000:5000 -v "$(pwd)":/opt/code pikatwo-be # 도커 이미지 실행
```

### 컨테이너 죽이기
```sh
pika-two-BE$ docker stop pikatwo-be && docker rm pikatwo-be # 도커 이미지 죽이기
```
