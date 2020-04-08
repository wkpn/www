# Single-page personal profile

## Requirements:
- <a href="https://github.com/encode/starlette">starlette<a>
- <a href="https://github.com/encode/uvicorn">uvicorn</a> for local deploying and testing
- <a href="https://stem.torproject.org/"stem</a> for deploying as a TOR hidden service

## Install requirements:
```shell
pip3 install -r requirements.txt
```

## Deployment:
```shell
npm i -g now
now --prod
```

## Local deployment:
```shell
uvicorn app:app --host 127.0.0.1 --port 8080
```
Your application would be available at `http://127.0.0.1:8080`


## Local deployment with a locally-trusted certificate (e.g. from a <a href="https://github.com/FiloSottile/mkcert">mkcert</a>):
```shell 
uvicorn app:app --host 127.0.0.1 --port 8080 --ssl-certfile=cert.pem --ssl-keyfile=key.pem
```
Your application would be available at `https://127.0.0.1:8080`


## Docker deployment as a TOR hidden service
```shell
docker build --rm -t hidden_service -f Dockerfile .
docker run --name hidden -d hidden_service
```

Your application would be available at `http://random_onion_address.onion` according to your private key