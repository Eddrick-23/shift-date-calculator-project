import tkinter as tk
from tkinter import messagebox
from calculator import Calculator as Calc
from tkinter import ttk
from tkcalendar import Calendar
import datetime

class calculatorGUI:

    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("800x550")
        s = ttk.Style(self.root)
        s.theme_use('clam')

        #button to get start date
        self.start_date_var = tk.StringVar(self.root, value="Not set")
        tk.Label(self.root, textvariable=self.start_date_var, font=("Arial",15)).pack()
        ttk.Button(self.root, text="Start Date", command=lambda:self.getdate(setfor="start")).pack()
        #button to get end date
        self.end_date_var = tk.StringVar(self.root, value = "Not set")
        tk.Label(self.root, textvariable=self.end_date_var, font=("Arial",15)).pack()
        ttk.Button(self.root, text="End Date", command=lambda:self.getdate(setfor="end")).pack()

        #gets shifts
        label = tk.Label(self.root,text="Days In", font=('Arial',18))
        label.config(bg="green") # set label background or foreground color --> "fg = green"
        label.pack(pady = 5)
        self.days_in = tk.Entry(self.root, font=("Arial",18))
        self.days_in.pack(anchor=tk.CENTER)

        label = tk.Label(self.root,text="Days Out", font=('Arial',18))
        label.config(bg="green") # set label background or foreground color --> "fg = green"
        label.pack(pady=5)
        self.days_out = tk.Entry(self.root, font=("Arial",18))
        self.days_out.pack()

        label = tk.Label(self.root,text="Shift names: (Enter in sequence, each shift separated by comma e.g. in1,in2,out1)", font=('Arial',18))
        label.config(bg="green") # set label background or foreground color --> "fg = green"
        label.pack(padx=10)
        self.shift_names = tk.Entry(self.root, font=("Arial",18))
        self.shift_names.pack()

        label = tk.Label(self.root,text="Shifts out of camp: e.g. out1,out2", font=('Arial',18))
        label.config(bg="green") # set label background or foreground color --> "fg = green"
        label.pack(padx=10)
        self.outcampshifts = tk.Entry(self.root, font=("Arial",18))
        self.outcampshifts.pack()

        label = tk.Label(self.root,text="Shift on first day", font=('Arial',18))
        label.config(bg="green") # set label background or foreground color --> "fg = green"
        label.pack(padx=10)
        self.shiftd1 = tk.Entry(self.root, font=("Arial",18))
        self.shiftd1.pack()

        #button which creates calculator
        self.button = tk.Button(self.root, text= "Create Calculator", font=("Arial",18), command=self.createCalc)
        self.button.pack()

        #button which calculates working days from a desired start date to end date
        self.calc_working_days = tk.Button(self.root,text = "Calculate working days",font=("Arial",18), command= self.calc_wd)
        self.calc_working_days.pack()

        #button to get shift on a specific date
        self.get_shift_on_date = tk.Button(self.root, text="Get shift on date", font=("Arial",18), command=self.query_shift)
        self.get_shift_on_date.pack()

        self.root.mainloop() #display the gui


    def createCalc(self):
        #gets info from textboxes, creates calculator object
        
        output = self.input_check()
        if output == None:
            return
        start_date,end_date, days_in, days_out, shift_names, outcampshifts, shiftd1 = output

        self.calculator = Calc(start_date,end_date,days_in,days_out,shift_names,outcampshifts,shiftd1)
        print(messagebox.showinfo(title="Message", message="Calculator Created!"))
    
    def getdate(self,setfor, y=2024, m=1, d=1):

        def set_sel(setfor):
            if setfor == "start":
                self.start_date_var.set(cal.selection_get())
                self.start_date = cal.selection_get()
            elif setfor == "end":
                self.end_date_var.set(cal.selection_get())
                self.end_date = cal.selection_get()
            elif setfor == "user_input":
                self.user_input = cal.selection_get()

                if self.user_input < self.start_date or self.user_input > self.end_date:
                    messagebox.showerror(title="Error", message= f"{self.user_input} is out of range of \n start date: {self.start_date} \n end date: {self.end_date}")
                    return
                str1,str2,data = self.calculator.calc_working_days(self.user_input)
                self.show_dataframe(str1,str2,data)
            elif setfor == "query":
                print("user input:", cal.selection_get())
                self.user_input = cal.selection_get()

                if self.user_input < self.start_date or self.user_input > self.end_date:
                    messagebox.showerror(title="Error", message= f"{self.user_input} is out of range of \n start date: {self.start_date} \n end date: {self.end_date}")
                    return
                day,shift = self.calculator.get_shift_on_date(self.user_input)

                messagebox.showinfo("Query", message=f"Your shift on {self.user_input} is {day}, {shift}." )
                
        

        top = tk.Toplevel(self.root) #create separate window
        cal = Calendar(top, font = ("Arial",14), selectmode = "day", cursor = "hand1", year = y , month = m,day = d)
        cal.pack(fill = "both", expand = True)
        ttk.Button(top, text = "ok", command=lambda:set_sel(setfor)).pack()
        
    def query_shift(self):

        t = datetime.date.today() #gets todays date
        
        self.getdate(setfor="query", y = t.year, m = t.month, d = t.day)


    def calc_wd(self):

        t = datetime.date.today() #gets todays date

        self.getdate(setfor="user_input", y= t.year, m = t.month, d = t.day) 

    def show_dataframe(self, str1,str2,data):

        
        #Create a new window
        display_window = tk.Toplevel(self.root)
        display_window.title(str1)

        tk.Label(display_window, text=str2).pack()
        
        #Create treeview widget
        tree = ttk.Treeview(display_window, columns=list(data.columns), show="headings")
        style = ttk.Style()
        style.configure("Treeview", background="black", foreground="white")
        style.configure("Treeview.Heading", background="black", foreground="yellow")
        tree.pack(expand=True, fill = 'both')

        #Define column headings:
        for col in data.columns:
            tree.heading(col, text = col)
            tree.column(col, width = 100, anchor="w")

        #Insert data into Treeview window
        for _, row in data.iterrows():
            tree.insert("","end", values = list(row))


        
    

    def input_check(self):
        '''
            Checks for valid user inputs. Prints an error message for invalid inputs
        '''
        try: 
            start_date = self.start_date
            end_date = self.end_date
            days_in = self.days_in.get()
            days_out = self.days_out.get()
            shift_names = self.shift_names.get()
            outcampshifts = self.outcampshifts.get()
            shiftd1 = self.shiftd1.get()
        except AttributeError:
            messagebox.showerror(title="Error", message="Missing value field!")
            return
        attributelist = [days_in, days_out,shift_names, outcampshifts, shiftd1]
        for a in attributelist:
            if len(a) == 0:
                messagebox.showerror(title="Error", message="Missing value field!")
                return
        
        #check for valid start and end date
        if self.start_date > self.end_date: 
            messagebox.showerror(title="Error", message= "Start date must be before end date!")
            return
        
        #check for valid days in and days out input
        try:
            din = int(self.days_in.get())
            dout = int(self.days_out.get())
        except ValueError:
            messagebox.showerror(title="Error", message="days in and days out must be positive integers!")
            return
        if din <= 0 or dout <= 0:
            messagebox.showerror(title="Error", message="days in and days out must be positive integers!")
            return

        #check for valid shift names and that number of shifts match days in and days out
        
        shiftnames = self.shift_names.get()
        shiftnames = shift_names.replace(" ","") #remove whitespace
        shiftnames = shiftnames.split(",")
        final_shift_names = []
        for s in shiftnames:
            if s != "" and s not in final_shift_names:
                final_shift_names.append(s)
        target_length = din + dout
        if len(final_shift_names) != target_length:
            messagebox.showerror(title="Error", message=f"Length of shift names do not match cycle length. \n You have {len(final_shift_names)} shift names \n Your cycle length is {target_length} \n These are your current shifts {final_shift_names}" )
            return
        
        #check for valid outshift days
        outshifts = outcampshifts.replace(" ","")
        outshifts = outshifts.split(",")
        final_outshifts = []
        for s in outshifts:
            if s != "" and s not in final_outshifts:
                final_outshifts.append(s)
        if len(final_outshifts) != dout:
            messagebox.showerror(title="Error", message=f"Your outshift days: {final_outshifts} do not match your days out: {dout}.")
            return
        if not set(final_outshifts) <= set(final_shift_names):
            messagebox.showerror(title="Error", message=f"Your outshift days: {final_outshifts} do not match your shift names: {final_shift_names}.")
            return
        
        #check for valid shift on d1
        if shiftd1 not in final_shift_names:
            messagebox.showerror(title="Error", message=f"Your shift on day 1: {shiftd1} does not exist in your shift names: {final_shift_names}")
            return
        return start_date,end_date, days_in, days_out, shift_names, outcampshifts, shiftd1


calculatorGUI()