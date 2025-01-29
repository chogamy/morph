# 형태소 분석기

# 사용법

호스트 서버에서 
```
docker build -f <YOUR_PATH>/morph/dockerfile -t morph .

docker run -d -p <YOUR_PORT>:<YOUR_PORT> --name morph morph

rm -r -f <YOUR_PATH>/morph
```