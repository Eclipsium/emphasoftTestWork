# Testing work for [Emphasoft](https://emphasoft.com/)

## Used libraries 
* [FastApi + Uvicorn](https://fastapi.tiangolo.com/)
* [asyncio](https://docs.python.org/3/library/asyncio.html)
* [BeautifulSoup4 + lxml parser](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
* [requests](https://docs.python-requests.org/en/master/)
* [aiofiles](https://github.com/Tinche/aiofiles)

## Server preparation 

1. First, you need install requirements in file `req.txt`


    ```pip install -r req.txt```


2. Next, you need start FastApi server:

    ```python main.py```
   
   or 
   
   ```uvicorn main:app```

3. Server running on http://127.0.0.1:8000 by default.

   
## Creating task
To start the task, you need to send a GET request to `http://localhost:8000/search` with 2 params:
1. `query` - required (String)
2. `task_type` - optional (String). `download | json`, default `json`. If `task_type` isn't valid, starting default task 

Example request: ```requests.get("http://localhost:8000/search?query=Form 11-C&task_type=download")```

