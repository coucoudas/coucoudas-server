### Docker build

```
docker build -t backend .
```

### Docker run
```
docker run -d -it -p 8000:8000 --rm --name backend backend
```

### Local run
```
docker-compose up -d --build
```