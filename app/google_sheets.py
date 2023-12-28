import gspread
from configparser import ConfigParser
from gspread.exceptions import SpreadsheetNotFound, GSpreadException, APIError
import os
from datetime import datetime, date
from .models import TidbitData, LearningTidbit
from typing import List

def access_sheet(config_path) -> gspread.Worksheet:
    config = ConfigParser()
    config.read(config_path)
    credentials_json = config.get('Credentials', 'google_credentials')
    sheet_name = config.get('Sheet', 'sheet_name')
    gc = gspread.service_account(filename=credentials_json)
    return gc.open(sheet_name).sheet1
    

def get_tidbit_data(index, row_dict):
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
    reviewable_tidbits = []
    for index, row_dict in enumerate(sheet.get_all_records(), start=2):
        print("Checking row:", index)
        tidbit = get_tidbit_data(index, row_dict)
        if tidbit is None:
            continue
        if LearningTidbit(tidbit).check_for_review():
            reviewable_tidbits.append(LearningTidbit(tidbit))
    
    return reviewable_tidbits

def update_review_counter(tidbit: LearningTidbit) -> None:
    sheet = access_sheet('settings.ini')
    
    tidbit.update_review_counter(sheet)


def get_tidbits_to_review() -> List[LearningTidbit]:
    # Get the directory of the current script

    sheet = access_sheet('settings.ini')
    print(sheet)

    return check_sheet_for_reviews(sheet)

def add_new_tidbit(tidbit_text: str) -> None:
    sheet = access_sheet('settings.ini')
    sheet.append_row([0,str(date.today()),tidbit_text])