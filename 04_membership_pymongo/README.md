# MongDB, pymongo를 이용해 회원관리 구현

![](https://youtu.be/xHsJqBKmRtc)

## MongoDB docker 설치

```zsh
docker images
docker run --name mongodb -v ~/PycharmProjects/data:/data/db -d -p 27017:27017 mongo
docker ps -a
docker start mongodb
docker exec -it mongodb bash
```

몽고디비 터미널을 실행하려면 도커 프롬프트에서 mongosh 입력 후 엔터

```docker
> show dbs
> use db이름
> show collections
> db.컬렉션이름.find()
```

## 구현 시 주의점

회원번호 자동 증가 -> 회원번호의 최댓값을 가져와 +1

=> `cnt = self.mycollection.find_one(sort=[("_id", -1)])["_id"]`

검색할 때 특정 단어를 포함한 모든 회원 출력 -> 정규표현식 이용

=> `select_arg1 = {select_key: {"$regex": select_value}}`
