# thetree_sitemap
더트리 위키에 사이트맵 파일을 수동으로 만들어주는 겁니다

# 패키지 설치
```pip install pymongo pytz python-dotenv```

# env 설정
이런식으로 하면됩니다.
INCLUDED_NAMESPACES는 사이트맵에 넣을 네임스페이스 목록을 적으면 됩니다.
예) INCLUDED_NAMESPACES=테스트위키,위키운영
```
USER_DOMAIN=https://example.com
MONGO_HOST=your-mongo-host
MONGO_PORT=27017
MONGO_USER=your-username
MONGO_PASS=your-password
MONGO_DB=your-db-name
INCLUDED_NAMESPACES=
```
