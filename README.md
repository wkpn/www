# Single-page personal profile

Requirements:
- <a href="https://github.com/encode/starlette">starlette<a>
- <a href="https://github.com/encode/uvicorn">uvicorn</a> for local deploying and testing

Deployment:
```shell
npm i -g now
now --prod
```

Local deployment:
```shell
pip3 install -r requirements.txt
uvicorn app:app --host 127.0.0.1 --port 8080
```

