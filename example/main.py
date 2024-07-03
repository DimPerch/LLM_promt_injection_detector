from fastapi import FastAPI, Request, Form, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from uuid import uuid4
import asyncio
from InjectionDetector import CanaryDetector, RexegDetector, LLM_detector


app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

tasks = {}


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


async def process_data(task_id: str,
                       input_field: str,
                       checkbox1: bool,
                       checkbox2: bool,
                       checkbox3: bool):
    if checkbox1:
        check1 = LLM_detector().check() # реализовать проверку LLM
    elif checkbox2:
        check2 = RexegDetector().check() # реализовать проверку Regex
    else:
        pass # тут настоящее выполнение основной модели
    result = {
        "input_field": input_field,
        "checkbox1": checkbox1,
        "checkbox2": checkbox2,
        "checkbox3": checkbox3
    }
    if checkbox3:
        check3 = CanaryDetector().check()
    tasks[task_id] = result


@app.post("/submit")
async def submit_data(background_tasks: BackgroundTasks,
                      input_field: str = Form(...),
                      checkbox1: bool = Form(False),
                      checkbox2: bool = Form(False),
                      checkbox3: bool = Form(False)):
    task_id = str(uuid4())
    tasks[task_id] = "processing"
    background_tasks.add_task(process_data, task_id, input_field, checkbox1, checkbox2, checkbox3)
    return JSONResponse(content={"task_id": task_id})


@app.get("/result/{task_id}")
async def get_result(task_id: str):
    result = tasks.get(task_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Task not found")
    elif result == "processing":
        return JSONResponse(content={"status": "processing"})
    else:
        return JSONResponse(content={"status": "completed", "result": result})
