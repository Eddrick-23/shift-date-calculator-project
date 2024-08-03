import tkinter as tk
from tkinter import messagebox
from calculator import Calculator as Calc
from tkinter import simpledialog
from tkinter import ttk
from tkcalendar import Calendar,DateEntry

class calculatorGUI:

    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("800x500")
        s = ttk.Style(self.root)
        s.theme_use('clam')

        #button to get start date
        ttk.Button(self.root, text="Start Date", command=lambda:self.getdate(setfor="start")).pack()

        #button to get end date
        ttk.Button(self.root, text="End Date", command=lambda:self.getdate(setfor="end")).pack()
        

        #gets shifts
        label = tk.Label(self.root,text="Days In", font=('Arial',18))
        label.config(bg="green") # set label background or foreground color --> "fg = green"
        label.pack(padx=10)
        self.days_in = tk.Entry(self.root, font=("Arial",18))
        self.days_in.pack()

        label = tk.Label(self.root,text="Days Out", font=('Arial',18))
        label.config(bg="green") # set label background or foreground color --> "fg = green"
        label.pack(padx=10)
        self.days_out = tk.Entry(self.root, font=("Arial",18))
        self.days_out.pack()

        label = tk.Label(self.root,text="Shift names: (Enter in sequence, each shift separated by comma e.g. in1,in2,out1)", font=('Arial',18))
        label.config(bg="green") # set label background or foreground color --> "fg = green"
        label.pack(padx=10)
        self.shift_names = tk.Entry(self.root, font=("Arial",18))
        self.shift_names.pack()

        label = tk.Label(self.root,text="Shifts out of ca20mp: e.g. out1,out2", font=('Arial',18))
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
        self.calc_working_days = tk.Button(self.root,text = "Calculate working days",font=("Arial",18), command=self.calc_wd)
        self.calc_working_days.pack()


        self.root.mainloop() #display the gui


    def createCalc(self):
        #gets info from textboxes, creates calculator object
        start_date = self.start_date
        end_date = self.end_date
        days_in = self.days_in.get()
        days_out = self.days_out.get()
        shift_names = self.shift_names.get()
        outcampshifts = self.outcampshifts.get()
        shiftd1 = self.shiftd1.get()

        self.calculator = Calc(start_date,end_date,days_in,days_out,shift_names,outcampshifts,shiftd1)
        print(messagebox.showinfo(title="Message", message="Calculator Created!"))
    
    def getdate(self,setfor):

        def set_sel(setfor):
            if setfor == "start":
                print("start date:" , cal.selection_get())
                self.start_date = cal.selection_get()
            elif setfor == "end":
                print("end date:" , cal.selection_get())
                self.end_date = cal.selection_get()
            elif setfor == "user_input":
                print("user input:", cal.selection_get())
                self.user_input = cal.selection_get()

                str1,str2,data = self.calculator.calc_working_days(self.user_input)
                self.show_dataframe(str1,str2,data)

        top = tk.Toplevel(self.root) #create separate window
        cal = Calendar(top, font = ("Arial",14), selectmode = "day", cursor = "hand1", year = 2024, month = 1,day = 1)
        cal.pack(fill = "both", expand = True)
        ttk.Button(top, text = "ok", command=lambda:set_sel(setfor)).pack()
        
        
    def calc_wd(self):
        #show a pop up asking for a start date
        self.getdate(setfor="user_input") 
    
    def show_dataframe(self, str1,str2,data):
        # Create a new window
        display_window = tk.Toplevel(self.root)
        display_window.title(str1)

        # Create a Text widget to display the tabulated DataFrame
        text_widget = tk.Text(display_window, wrap='none')
        text_widget.pack(expand=True, fill='both')

        # Insert the formatted string into the Text widget
        text_widget.insert('1.0',str2)
        text_widget.insert('1.0', "\n")
        text_widget.insert('1.0', data) 
        text_widget.config(state='disabled')  # Make the Text widget read-only
    


calculatorGUI()