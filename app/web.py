# app/web.py

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.scanner import scan_network

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "results": [],
            "network": None,
            "error": None,
        },
    )


@app.post("/scan", response_class=HTMLResponse)
def scan(request: Request, network: str = Form(...)):
    try:
        results = scan_network(network)
    except Exception as e:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "results": [],
                "network": network,
                "error": str(e),
            },
        )

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "results": results,
            "network": network,
            "error": None,
        },
    )
