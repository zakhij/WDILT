from fastapi import FastAPI, Request
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
    """
    Generates the homepage for the app. The homepage has two buttons: one to redirect
     the user to the /review page, and one to redirect the user to the /newtidbits page
    """
    return templates.TemplateResponse("home_page.html", {"request": request})

    
@app.get("/review")
async def review_test(request: Request):
    """
    Generates the page that displays the tidbits that are up for review. 
    Initializing the page will generate the list of tidbits that are up 
    for review and pass them through to the frontend.
    """
    tidbits = get_tidbits_to_review()
    tidbits_list = [str(t) for t in tidbits] # tidbits
    for tidbit in tidbits:
        tidbit_dict[str(tidbit)] = tidbit
    tidbits_json = json.dumps(tidbits_list)
    return templates.TemplateResponse("review.html", {"request": request, "tidbits": tidbits_json})

@app.get("/newtidbits")
async def new_tidbits(request: Request):
    """
    Generates the page that allows the user to add new tidbits. Logic to add tidbits
    is handled in the frontend and in /submit-tidbit endpoint.
    """
    return templates.TemplateResponse("addtidbits.html", {"request": request})

@app.post("/process-checked-tidbits")
async def process_checked_tidbits(tidbits: List[str]):
    """
    Takes the list of tidbits that the user checked as "reviewed"
    on the /review page and updates the review counter for each.
    """
    for tidbit_str in tidbits:
        tidbit = tidbit_dict[tidbit_str]
        update_review_counter(tidbit)
    return {"message": "Checked tidbits processed successfully"}

@app.post("/submit-tidbit")
async def new_tidbit(request: Request):
    """
    Adds a new tidbit to the WDILT Google sheet based on the inputted text. 
    Used on the /newtidbits page.
    """
    data = await request.json()
    tidbit_text = data.get("text")
    add_new_tidbit(tidbit_text)
    return {"message": "Tidbit received"}

