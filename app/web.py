from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from.scanner import scan

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

@app.post("/scan", response_class=HTMLResponse)
def run_scan(request: Request, network: str = Form(...)):
    results = scan(network)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "results": results
        }
    )
