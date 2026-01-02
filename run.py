import uvicorn
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)
from app.web import app

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)
