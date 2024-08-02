import tkinter as tk
from tkinter import messagebox
from calculator import Calculator as Calc
from tkinter import simpledialog

class calculatorGUI:

    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("800x500")

        #button to get start date
        label = tk.Label(self.root,text="Start Date", font=('Arial',18))
        label.config(bg="green") # set label background or foreground color --> "fg = green"
        label.pack(padx=10)
        self.start_date = tk.Entry(self.root, font=("Arial",18))
        self.start_date.pack()

        #button to get end date
        label = tk.Label(self.root,text="End Date", font=('Arial',18))
        label.config(bg="green") # set label background or foreground color --> "fg = green"
        label.pack(padx=10)
        self.end_date = tk.Entry(self.root, font=("Arial",18))
        self.end_date.pack()

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
        self.calc_working_days = tk.Button(self.root,text = "Calculate working days",font=("Arial",18), command=self.calc_wd)
        self.calc_working_days.pack()


        self.root.mainloop() #display the gui


    def createCalc(self):
        #gets info from textboxes, creates calculator object
        start_date = self.start_date.get()
        end_date = self.end_date.get()
        days_in = self.days_in.get()
        days_out = self.days_out.get()
        shift_names = self.shift_names.get()
        outcampshifts = self.outcampshifts.get()
        shiftd1 = self.shiftd1.get()

        self.calculator = Calc(start_date,end_date,days_in,days_out,shift_names,outcampshifts,shiftd1)
        print(messagebox.showinfo(title="Message", message="Calculator Created!"))
    
    def calc_wd(self):
        #show a pop up asking for a start date
        user_input = simpledialog.askstring(title="Input",prompt="What is the start date?")
        
        str1,str2,data = self.calculator.calc_working_days(user_input)
        self.show_dataframe(str1,str2,data)
    
    def show_dataframe(self, str1,str2,data):
        # Create a new window
        display_window = tk.Toplevel(self.root)
        display_window.title(str1)

        # Create a Text widget to display the tabulated DataFrame
        text_widget = tk.Text(display_window, wrap='none', font=20)
        text_widget.pack(expand=True, fill='both')

        # Insert the formatted string into the Text widget
        text_widget.insert('1.0',str2)
        text_widget.insert('1.0', "\n")
        text_widget.insert('1.0', data) 
        text_widget.config(state='disabled')  # Make the Text widget read-only

        #button to adjust text size
        increaseButton = tk.Button(display_window,"+",command=self.increaseTextSize)
        increaseButton.pack()
        decreaseButton = tk.Button(display_window,"-",command=self.decreaseTextSize)
        decreaseButton.pack()
    
    def increaseTextSize(self):
        pass
    def decreaseTextSize(self):
        pass


calculatorGUI()