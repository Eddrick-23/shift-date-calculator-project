import pandas as pd
from datetime import datetime
from itertools import cycle
from collections import defaultdict

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
        dates = pd.date_range(start=self.start_date, end = self.end_date).to_list()
        self.data = pd.DataFrame(dates, columns=["dates"])
        self.prepare_data()
    def prepare_data(self):
        df = self.data.copy()
        df = df.set_index("dates")
        df = df.index.to_frame()
        df["dates"] = df.dates.apply(lambda x: x.day_name())
        df.rename(columns= {"dates": "day"}, inplace=True)
        self.data = df
    
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
        
        df = self.data.copy()
        shifts = []
        
        for i in range(len(df.index)):
            shifts.append(next(status))
        df["shifts"] = shifts
        self.data = df

    
    def show_shift_on_date(self,date): 
        
        '''
        shows the shift on a specific date. Input to be in 'YYYY-MM-DD' format
        '''
        bar = self.data.loc[pd.to_datetime(date)].to_frame()
        return bar

    
    def calc_working_days(self,date): 
        '''
        calculate the number of working days from the "date" onwards.
        date input to be in 'YYYY-MM-DD' format
        '''
        day_data = defaultdict(int)
        working_days = 0
        non_working = 0
        for i in range(len(self.data.loc[pd.to_datetime(date):])):
            day,shift = self.data.iloc[i]
            if shift not in ["D1","D2"]:
                day_data[day] += 1
                working_days += 1
            else:
                non_working += 1
        #dataframe consisting of working days for each date
        df = pd.DataFrame(day_data.items(), columns= ["Days","Days Working"])
        custom_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        df['Days'] = pd.Categorical(df['Days'], categories=custom_order, ordered=True)
        # Sort DataFrame based on 'Category' column
        sorted_df = df.sort_values(by='Days')

        print(f'Total:{working_days+non_working}, working:{working_days}, non working :{non_working}')
        print(sorted_df.to_markdown(index=False))
            


            