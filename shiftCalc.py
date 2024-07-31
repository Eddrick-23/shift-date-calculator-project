import pandas as pd
from datetime import datetime
from itertools import cycle
from collections import defaultdict
import holidays
from tabulate import tabulate

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
    def set_new_cycle(self, reset_type = "all"):
        '''
            Sets a new X in X out cycle based on the same time period
            Parameters
            ==========
            reset_type (str):
                "all" --> Sets new X in X out shift cycle
                "changeD1" --> Maintains shift cycle and changes shift on Day 1
        '''
        if reset_type not in ["all","changeD1"]:
            raise Exception("Reset type should be specified as 'all or 'changeD1'.")
        if reset_type == "all":
            dates = pd.date_range(start=self.start_date, end = self.end_date).to_list()
            self.data = pd.DataFrame(dates, columns=["dates"])
            self.prepare_data()
        self.calculate_shift(changeFirstDayOnly = (reset_type == "changeD1"))
    def get_shift_info(self):
        '''
            gets user shift cycle information
        '''
        self.quit = False
        #get cycle size: x in x out
        while True:
            try:
                comb = input("How many days in and out? (X in,X out)")
                if comb in ["Quit","quit"]:
                    self.quit = True
                    break
                incamp, outcamp = map(int, comb.split(","))
            except:
                print("Please enter an integer")
                print("Enter values in the format Days in, Days out. e.g. 2,3 for 2 days in 3 days out.")
            if incamp <=0:
                print("Days in must be at least 1!")
                continue
            if outcamp <=0:
                print("Days out must be at least 1!")
                continue
            break
        
        if self.quit:
            print("Quitting!")
            return
        #get what a typical cycle is like e.g. in1,in2,out1,out2
        cycle_length = incamp + outcamp
        while True:
            sample = input("In 1 cycle, what is the sequence of shifts? Enter the shifts seperated by commas. E.g. in1,in2,out1: ")
            if sample in ["Quit","quit"]:
                self.quit = True
                break
            sample = sample.split(",")
            if len(sample) != cycle_length:
                print(f"You should have a total of {cycle_length} shifts. You only entered {len(sample)}!")
                print("Please enter the shifts in sequence, seperated by commas!")
                print("Example: In1,In2,Out1,Out2")
                print(f"Your current shifts are : {sample}")
                continue      
            break

        if self.quit:
            print("Quitting!")
            return
        
        #get the non working days
        while True:
            outshifts = input("What are the non working days? Enter the shifts seperated by commas. E.g. out1,out2: ")
            if outshifts in ["Quit","quit"]:
                self.quit = True
                break
            outshifts = outshifts.split(",")
            if len(outshifts) != outcamp:
                print(f"You should have a total of {outcamp} out days. You entered {len(outshifts)}!")
                print("Please enter the shifts seperated by commas!")
                print("Example: Out1,Out2")
                print(f"Your current shifts are : {outshifts}")
                continue
            if not(set(outshifts) <= set(sample)): #check if elements in outshifts match those in sample
                print("Your shifts do not match!")
                print(f"Your shift cycle: {sample}")
                print(f"Your non working shifts{outshifts}")
                continue
            break

        self.shiftcycle = sample
        self.outcampshifts = outshifts

    def get_shift_on_D1(self):
        while True:
            first = input(f"what is the shift on the first day {self.start_date}?: ")
            if first in ["Quit","quit"]:
                self.quit = True
                break
            if first not in self.shiftcycle:
                print(f"shift does not exist, try: {self.shiftcycle}")
                continue
            else:
                startIdx = self.shiftcycle.index(first) #set the first index
                return startIdx


    def calculate_shift(self, changeFirstDayOnly = False): 
        '''
            calculates shifts
        '''
        self.quit = False
        if not changeFirstDayOnly:
            self.get_shift_info()

        if self.quit:
            print("Quitting")
            return
        #ask for user input on first shift day
        startIdx = self.get_shift_on_D1()
        
        if self.quit:
            print("Quitting!")
            return
    
        #rotate list to start with first day
        
        status = self.shiftcycle[startIdx:]+self.shiftcycle[:startIdx]
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

        print(f"From {date} to {self.data.index[-1].date()}")
        print(f'Total:{working_days+non_working}, working:{working_days}, non working :{non_working}, Working on Public Holidays: {ph_working_days}')
        
        print(tabulate(sorted_df,headers=["Day","Freq","PH Freq","Public Holidays"], tablefmt='grid', showindex=False))
            


            