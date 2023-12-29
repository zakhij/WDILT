import gspread
from configparser import ConfigParser
from gspread.exceptions import SpreadsheetNotFound, GSpreadException, APIError
import os
from datetime import datetime, date
from .models import TidbitData, LearningTidbit
from typing import List

# Helper functions
def access_sheet(config_path) -> gspread.Worksheet:
    """
    Abstracts away the work of accessing the Google sheet that
    stores the WDILT tidbit data.
    """
    config = ConfigParser()
    config.read(config_path)
    credentials_json = config.get('Credentials', 'google_credentials')
    sheet_name = config.get('Sheet', 'sheet_name')
    gc = gspread.service_account(filename=credentials_json)
    return gc.open(sheet_name).sheet1
    
def get_tidbit_data(index, row_dict):
    """
    Creates a TidbitData object from the row in the sheet. Used
    for data validation purposes.
    """
    try:
        return TidbitData(
            row_num=index,
            tidbit=row_dict['tidbit'],
            review_counter=int(row_dict['review_counter']),
            last_review_date=datetime.strptime(row_dict['last_review_date'], '%Y-%m-%d').date()
        )
    except Exception:
        return None

def check_sheet_for_reviews(sheet: gspread.Worksheet) -> List[LearningTidbit]:
    """
    Goes through the sheet, checks each row, and returns a list of
    all tidbits that are up for review.
    """
    reviewable_tidbits = []
    for index, row_dict in enumerate(sheet.get_all_records(), start=2):
        tidbit = get_tidbit_data(index, row_dict)
        if tidbit is None:
            continue
        if LearningTidbit(tidbit).check_for_review():
            reviewable_tidbits.append(LearningTidbit(tidbit))
    
    return reviewable_tidbits

# Main functions used by app in main.py
def update_review_counter(tidbit: LearningTidbit) -> None:
    """
    Leverages the update_review_counter method in the LearningTidbit class
    to update the review counter in the sheet of the inputted tidbit object.
    """
    sheet = access_sheet('settings.ini')
    tidbit.update_review_counter(sheet)

def get_tidbits_to_review() -> List[LearningTidbit]:
    """
    Gets the tidbits that need to be reviewed of the Google sheet.
    Separate from check_sheet_for_reviews to abstract away the sheet input.
    """
    sheet = access_sheet('settings.ini')
    return check_sheet_for_reviews(sheet)

def add_new_tidbit(tidbit_text: str) -> None:
    """
    Adds a new tidbit to the WDILT Google sheet based on the inputted text.
    """
    sheet = access_sheet('settings.ini')
    sheet.append_row([0,str(date.today()),tidbit_text])