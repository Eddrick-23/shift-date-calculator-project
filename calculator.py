import pandas as pd
from datetime import datetime
from itertools import cycle
from collections import defaultdict
import holidays
from tabulate import tabulate

#calculator class used for GUI pyscript

class Calculator():
    def __init__(self, start_date, end_date, daysIn,daysOut,shiftcycle,outcampshifts, d1shift):
        self.start_date = start_date
        self.end_date = end_date
        self.daysin = int(daysIn)
        self.daysout = int(daysOut)
        self.shiftcycle = shiftcycle.split(",") # specific shifts in each cycle
        self.outcampshifts = outcampshifts.split(",")
        self.shift_on_D1 = d1shift #what is the shift on self.start_date
        dates = pd.date_range(start=self.start_date, end = self.end_date).to_list()
        self.data = pd.DataFrame(dates, columns=["dates"])
        self.prepare_data()
        self.calculate_shift()
    def prepare_data(self):
        df = self.data.copy()
        df = df.set_index("dates")
        df = df.index.to_frame()
        df["dates"] = df.dates.apply(lambda x: x.day_name())
        df.rename(columns= {"dates": "day"}, inplace=True)
        self.data = df

    def calculate_shift(self): 
        '''
            calculates shifts
        '''
        startIdx = self.shiftcycle.index(self.shift_on_D1)
    
        #rotate list to start with first day
        
        status = self.shiftcycle[startIdx:]+self.shiftcycle[:startIdx]
        status = cycle(status) #convert to itertable to use next() function
        
        df = self.data.copy()
        shifts = []
        
        for i in range(len(df.index)):
            shifts.append(next(status))
        df["shifts"] = shifts
        self.data = df
    
    def calc_working_days(self,date): 
        '''
        calculate the number of working days from the "date" onwards.
        date input to be in 'YYYY-MM-DD' format
        '''
        sg_holidays = holidays.country_holidays("SG") #to check public holidays for later
        day_data = defaultdict(int)
        working_days = 0
        working_public_hols = defaultdict(int)
        working_public_hols_name = defaultdict(list)
        non_working = 0
        ph_working_days = 0
        for i in range(len(self.data.loc[pd.to_datetime(date):])):
            d = self.data.index[i].date() #get the datetime obj
            day,shift = self.data.iloc[i]
            if shift not in self.outcampshifts: #if it is a working day
                day_data[day] += 1
                working_days += 1
                if d in sg_holidays:
                    working_public_hols[day] += 1
                    ph_working_days += 1
                    working_public_hols_name[day].append(sg_holidays.get(d))
            else:
                non_working += 1
        #dataframe consisting of working days for each date
        df = pd.DataFrame(day_data.items(), columns= ["Days","Days Working"])
        custom_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        df['Days'] = pd.Categorical(df['Days'], categories=custom_order, ordered=True)
        # Sort DataFrame based on 'Category' column
        sorted_df = df.sort_values(by='Days')
        df_freqHols = pd.DataFrame(working_public_hols.items(),columns=["Days","Freq Holidays"])
        df_holNames = pd.DataFrame(working_public_hols_name.items(), columns=["Days","Holiday(s)"])
        sorted_df = sorted_df.merge(df_freqHols, on="Days", how = "left").fillna(0)
        sorted_df = sorted_df.merge(df_holNames, on="Days", how = "left").fillna("None")

        s1 = (f"From {date} to {self.data.index[-1].date()}")
        s2 = (f'Total:{working_days+non_working}, working:{working_days}, non working :{non_working}, Working on Public Holidays: {ph_working_days}')
        
        return s1,s2,tabulate(sorted_df,headers=["Day","Freq","PH Freq","Public Holidays"], tablefmt='grid', showindex=False)

