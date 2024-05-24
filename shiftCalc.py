import pandas as pd
from datetime import datetime
from itertools import cycle

#define the calendar class which stores the shifts
class Calendar():
    def __init__(self,start_date,end_date):
        '''
        To initialize, class, input the start date and end date. 
        A list of dates is created for the corresponding start and end dates given.
        The date-shift pairs are stored in a dictionary
        '''
        self.start_date = start_date
        self.end_date = end_date
        self.date_list = pd.date_range(datetime.strptime(start_date,"%Y-%m-%d"),datetime.strptime(end_date,"%Y-%m-%d"),freq = 'D')
        self.date_shifts = {} #initialise empty dict
    def show_dates(self): 
        '''
        Displays all dates and their corresponding shifts
        '''
        print(self.date_shifts)
    
    def calculate_shift(self): 
        '''
        status_on_first_day = S1,S2,M1,M2,D1,D2 in str format
        '''
        
        sample = ["S1","S2","M1","M2","D1","D2"]
        startIdx = 0

        #ask for user input on first shift day
        while True:
            first = input(f"what is the shift on the first day {self.start_date}?: ")

            if first not in sample:
                print("shift does not exist, try: S1,S2,M1,M2,D1,D2")
                continue
            else:
                startIdx = sample.index(first) #set the first index
                break
        #rotate list to start with first day
        status = sample[startIdx:]+sample[:startIdx]
        status = cycle(status) #convert to itertable to use next() function
        
        for date in self.date_list.strftime("%Y-%m-%d"):
            self.date_shifts[date] = next(status)
    
    def show_shift_on_date(self,date): 
        
        '''
        shows the shift on a specific date. Input to be in 'YYYY-MM-DD' format
        '''
        print(f'Your shift on {date} is {self.date_shifts[date]}.')
    
    def calc_working_days(self,date): 
        '''
        calculate the number of working days from the "date" onwards.
        date input to be in 'YYYY-MM-DD' format
        '''
        dates = pd.date_range(datetime.strptime(date,"%Y-%m-%d"),datetime.strptime(self.end_date,"%Y-%m-%d"),freq = 'D')
        total_days = len(dates)
        non_working = 0
        for date in dates.strftime("%Y-%m-%d"):
            if self.date_shifts[date] in ['D1','D2']:
                non_working += 1
        
        working_days = total_days - non_working

        print(f'Total:{total_days}, working:{working_days}, non working :{non_working}')
            


            