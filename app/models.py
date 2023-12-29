from datetime import date, timedelta
from pydantic import BaseModel
import gspread

class TidbitData(BaseModel):
    """
    Data validation model that ensures that the data in each Google sheet
    row is in the correct format before creating a LearningTidbit object. 
    """
    row_num: int
    tidbit: str
    review_counter: int
    last_review_date: date

class LearningTidbit:
    """
    Class that represents each tidbit, which is found in each row. Data validation
    is done in the TidbitData model, which is used as an input.
    """
    # Hardcoded constants
    SCALE1_INIT = 3
    SCALE2 = 4
    REVIEW_COUNTER_COL = 1
    LAST_REVIEW_DATE_COL = 2
    def __init__(self, tidbit_data: TidbitData):
        # Extracting data from TidbitData
        self.row_num = tidbit_data.row_num
        self.tidbit = tidbit_data.tidbit
        self.review_counter = tidbit_data.review_counter
        self.last_review_date = tidbit_data.last_review_date
        
    def check_for_review(self) -> None:
        """
        Checks whether the tidbit needs to be reviewed. If so, it prints
        the tidbit to the console and updates the review counter.
        """
        next_review_date = self.calc_next_review_date()
        if next_review_date <= date.today():
            return True
        else:
            return False
    
    def __str__(self) -> str:
        return f"Tidbit Review #{self.review_counter}:\n{self.tidbit}"


    def calc_next_review_date(self) -> date: 
        """
        Helper function that calculates the next review date,
        based on the last review date and on review counter value.
        Scale values are used to implement spaced repetition by increasing
        the time between reviews.
        """
        if self.review_counter == 0:
        # If there have been no reviews, the next review is 1 day after the last review date
            return self.last_review_date + timedelta(days=1)

        # For subsequent reviews, use the scaling factors
        days_to_add = self.SCALE1_INIT
        for _ in range(1, self.review_counter):
            days_to_add *= self.SCALE2

        return self.last_review_date + timedelta(days=days_to_add)
    

    def update_review_counter(self, sheet) -> None:
        self.review_counter += 1
        self.last_review_date = date.today()

        # Prepare the data for batch update
        values = [[self.review_counter, str(self.last_review_date)]]
        cell_range = f"{gspread.utils.rowcol_to_a1(self.row_num, self.REVIEW_COUNTER_COL)}:" \
                    f"{gspread.utils.rowcol_to_a1(self.row_num, self.LAST_REVIEW_DATE_COL)}"
        
        #Update the sheet with new values for the review counter and last review date
        sheet.update(cell_range, values)


