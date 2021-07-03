# Source code for https://wkpn.me

## Requirements:
- <a href="https://github.com/aio-libs/aiohttp">aiohttp</a>
- <a href="https://github.com/encode/starlette">starlette<a>
- <a href="https://github.com/encode/uvicorn">uvicorn</a> (for local deploying and testing)

## Install requirements:
```shell
pip3 install -r requirements.txt
```

## Deployment:
```shell
npm i -g vercel
vercel --prod
```

## Local deployment:
```shell
uvicorn api.app:app --host 127.0.0.1 --port 8080
```
Website will be available at `http://127.0.0.1:8080`

## Local deployment with a locally-trusted certificate (e.g. from a <a href="https://github.com/FiloSottile/mkcert">mkcert</a>):
```shell 
uvicorn api.app:app --host 127.0.0.1 --port 8080 --ssl-certfile=cert.pem --ssl-keyfile=key.pem
```
Website will be available at `https://127.0.0.1:8080`

## Local deployment with Vercel:
```shell
vercel dev
```
Website will be available at `http://127.0.0.1:3000`