from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from .scanner import run_scan

app = FastAPI()

templates = Jinja2Templates(directory="template")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


@app.post("/scan")
def scan(network: str = Form(...)):
    results = run_scan(network)
    return {
        "status": "ok",
        "count": len(results),
        "results": results
    }
