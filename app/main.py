from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import List
from .google_sheets import get_tidbits_to_review, update_review_counter, add_new_tidbit
import json

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Global variables
tidbit_dict = {} # Dictionary to store tidbits to review, allows comm between frontend and backend

@app.get("/")
async def homepage(request: Request):
    return templates.TemplateResponse("home_page.html", {"request": request})

'''
@app.get("/review")
async def review_tidbits(request: Request):
    try:
        # Logic to fetch and process tidbits from Google Sheets
        tidbits = get_tidbits_to_review()
        return [str(t) for t in tidbits] # tidbits
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))'''
    
@app.get("/review")
async def review_test(request: Request):
    tidbits = get_tidbits_to_review()
    tidbits_list = [str(t) for t in tidbits] # tidbits
    for tidbit in tidbits:
        tidbit_dict[str(tidbit)] = tidbit
    tidbits_json = json.dumps(tidbits_list)
    return templates.TemplateResponse("review.html", {"request": request, "tidbits": tidbits_json})

@app.get("/newtidbits")
async def new_tidbits(request: Request):
    return templates.TemplateResponse("addtidbits.html", {"request": request})

@app.post("/process-checked-tidbits")
async def process_checked_tidbits(tidbits: List[str]):
    for tidbit_str in tidbits:
        tidbit = tidbit_dict[tidbit_str]
        update_review_counter(tidbit)

    return {"message": "Checked tidbits processed successfully"}

@app.post("/submit-tidbit")
async def new_tidbit(request: Request):
    data = await request.json()
    tidbit_text = data.get("text")
    add_new_tidbit(tidbit_text)
    return {"message": "Tidbit received"}

