import asyncio
import os
from typing import Optional

import uvicorn
from fastapi import FastAPI, BackgroundTasks

from CONSTANTS import TIMEOUT
from bs4_worker import BS4Worker, background_bs4_worker

app = FastAPI()


@app.get("/search")
async def parse_tax(query: str, background_tasks: BackgroundTasks,
                    task_type: Optional[str] = 'json'):  # download, json

    worker = BS4Worker(query, task_type)

    if task_type == 'download':
        # create new thread
        background_tasks.add_task(background_bs4_worker, query, task_type)
        return {'status': 'ok'}

    return worker.parse()


if __name__ == '__main__':
    # fix self._check_closed() on windows
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    os.environ['TIMEOUT'] = TIMEOUT
    uvicorn.run(app)
