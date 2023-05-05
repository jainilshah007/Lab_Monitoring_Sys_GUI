import tkinter as tk
import serial
from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkcalendar import DateEntry
import matplotlib.dates as mdates
from tkinter.font import Font
from tkinter import Tk, Label, font
import csv
import datetime
from matplotlib.dates import DateFormatter


ser = serial.Serial('COM3', baudrate=115200, timeout=1)  # Replace with your serial port
time=0

class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()  # call pack method here
        self.data_label = Label(self.master, text="Sensor Data: Temperature: 0°C, Humidity: 0%")
        self.data_label.pack()
        
        self.update_data()
        self.create_widgets()
        
    def create_widgets(self):
        self.button_frame = tk.Frame(self.master)
        self.button_frame.pack(padx=10, pady=10)
        self.temp_label = tk.Label(self, text="Temperature:", font=("Helvetica", 12, "bold"))
        self.temp_label.grid(row=0, column=0)

        self.hum_label = tk.Label(self, text="Humidity:", font=("Helvetica", 12, "bold"))
        self.hum_label.grid(row=1, column=0)

        self.more_button = tk.Button(self.master, text="More", command=self.toggle_buttons)
        self.more_button.pack(padx=10, pady=10)

        self.button1 = tk.Button(self.button_frame, text="RM 1", command=self.select_button1, bg="navyblue", fg="white", activebackground="green") 
        self.button2 = tk.Button(self.button_frame, text="RM 2", command=self.select_button2, bg="navyblue", fg="white", activebackground="green")
        self.button3 = tk.Button(self.button_frame, text="RM 3", command=self.select_button3,bg="navyblue", fg="white", activebackground="green")
        self.button4 = tk.Button(self.button_frame, text="RM 4", command=self.select_button4,bg="navyblue", fg="white", activebackground="green")


       
    def toggle_buttons(self):
        
        # check if buttons are visible or not
        if self.button1.winfo_viewable():
            # hide buttons
            self.button1.pack_forget()
            self.button2.pack_forget()
            self.button3.pack_forget()
            self.button4.pack_forget()
            
        else:
            # show buttons
            self.room_label = tk.Label(self.button_frame, text="Choose the Room")
            self.room_label.pack(side="top", pady=5)
            self.button1.pack(side=tk.LEFT, padx=5, pady=5)
            self.button2.pack(side=tk.LEFT, padx=5, pady=5)
            self.button3.pack(side=tk.LEFT, padx=5, pady=5)
            self.button4.pack(side=tk.LEFT, padx=5, pady=5)
            # self.button1.pack(side="left", padx=10)
            # self.button2.pack(side="left", padx=10)
            # self.button3.pack(side="left", padx=10)
            # self.button4.pack(side="left", padx=10)
            self.more_button.pack_forget()

        def function1():
            print("Function 1")
        
            def load_csv():
    # Open a file dialog to select a CSV file
                file_path = filedialog.askopenfilename()
                if file_path:
                    # Read the CSV file into a pandas DataFrame
                    df = pd.read_csv(file_path)
                    df['date'] = pd.to_datetime(df['date']) # Convert 'date' column to datetime format
                    df = df.set_index('date') # Set 'date' column as index
                    plot_data(df) # Plot the data

            # Function to plot the data
            def plot_data(df):
                # Create a new Tkinter window for the graph
                graph_window = tk.Toplevel(root)
                graph_window.title("CSV Data Plot")

                # Create a figure and plot the data
                fig = plt.Figure(figsize=(10, 5), dpi=100)
                plot = fig.add_subplot(111)
                plot.plot(df.index, df['value'])
                plot.set_xlabel('Date') # Set x-axis label as 'Date'
                plot.set_ylabel('Value')

                # Set x-axis label format as 'dd/MM/yyyy'
                date_formatter = DateFormatter('%d/%m/%Y')
                plot.xaxis.set_major_formatter(date_formatter)

                # Create a canvas to display the graph
                canvas = FigureCanvasTkAgg(fig, master=graph_window)
                canvas.draw()
                canvas.get_tk_widget().pack()

                # Create labels and date entry widgets for start date and end date
                start_date_label = tk.Label(graph_window, text="Start Date:")
                start_date_label.pack()
                start_date_entry = DateEntry(graph_window, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')
                start_date_entry.pack()
                end_date_label = tk.Label(graph_window, text="End Date:")
                end_date_label.pack()
                end_date_entry = DateEntry(graph_window, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')
                end_date_entry.pack()

                def plot_between_dates():
                    start_date = pd.Timestamp(start_date_entry.get_date())
                    end_date = pd.Timestamp(end_date_entry.get_date())
                    if start_date and end_date:
                        mask = (df.index >= start_date) & (df.index <= end_date)
                        plot.clear()
                        plot.plot(df[mask].index, df[mask]['value'])
                        plot.set_xlabel('Date') # Set x-axis label as 'Date'
                        plot.set_ylabel('Value')
                        plot.xaxis.set_major_formatter(date_formatter) # Set x-axis label format as 'dd/MM/yyyy'
                        canvas.draw()

                # Create a button to plot the graph between the selected dates
                plot_button = tk.Button(graph_window, text="Plot Between Dates", command=plot_between_dates)
                plot_button.pack()

            # Create a button to load the CSV file and plot the data
            root = tk.Tk()
            load_button = tk.Button(root, text="Load CSV File", command=load_csv)
            load_button.pack()

            root.mainloop()

        def function2():
            print("Function 2")
            
            df = pd.read_excel(r'C:\Downloads\data.csv', index_col=0)

            # Convert index to datetime format
            df.index = pd.to_datetime(df.index)

            # Create tkinter window
            window = tk.Tk()
            window.title('Temperature and Humidity Data')

            # Create figure and axes for plots
            fig, ax = plt.subplots()

            # Create plot functions
            # def plot_temperature(start_date, end_date):
            #     ax.clear()
            #     ax.plot(df[start_date:end_date].index, df[start_date:end_date]['Temperature'])
            #     ax.set_xlabel('Date')
            #     ax.set_ylabel('Temperature (Celsius)')
            #     ax.set_title('Temperature vs. Date')
                # ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %m %Y'))
                
               
            #     fig.autofmt_xdate()
            #     plt.show()
            def plot_temperature(start_date, end_date):
                ax.clear()
                temp = df[start_date:end_date]['Temperature'].round()
                ax.plot(df[start_date:end_date].index, temp)
                ax.set_xlabel('Date')
                ax.set_ylabel('Temperature (Celsius)')
                ax.set_title('Temperature vs. Date')
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %m %Y'))
                from matplotlib import ticker
                ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
                import numpy as np
                ax.set_xticks(np.arange(df[start_date:end_date].index[0].value, df[start_date:end_date].index[-1].value, dtype='datetime64[D]'))
                fig.autofmt_xdate()
                plt.show()


            def plot_humidity(start_date, end_date):
                ax.clear()
                ax.plot(df[start_date:end_date].index, df[start_date:end_date]['Humidity'])
                ax.set_xlabel('Date')
                ax.set_ylabel('Humidity (%)')
                ax.set_title('Humidity vs. Date')
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %m %Y'))
                fig.autofmt_xdate()
                plt.show()

            # Create start and end date functions
            def set_start_date():
                global start_date_entry
                start_date_entry = DateEntry(window, width=12, background='darkblue',
                                            foreground='white', borderwidth=2)
                start_date_entry.pack(side=tk.LEFT, padx=10, pady=10)
                start_date_button.config(state=tk.DISABLED)
                end_date_button.config(state=tk.NORMAL)

            def set_end_date():
                global end_date_entry
                end_date_entry = DateEntry(window, width=12, background='darkblue',
                                        foreground='white', borderwidth=2)
                end_date_entry.pack(side=tk.LEFT, padx=10, pady=10)
                plot_temp_button.config(command=lambda: plot_temperature(start_date_entry.get_date(), end_date_entry.get_date()))
                plot_humid_button.config(command=lambda: plot_humidity(start_date_entry.get_date(), end_date_entry.get_date()))
                start_date_button.config(state=tk.NORMAL)
                end_date_button.config(state=tk.DISABLED)

            # Create plot buttons
            plot_temp_button = tk.Button(window, text='Temperature Plot')
            plot_temp_button.pack(side=tk.LEFT, padx=10, pady=10)

            plot_humid_button = tk.Button(window, text='Humidity Plot')
            plot_humid_button.pack(side=tk.LEFT, padx=10, pady=10)

            start_date_button = tk.Button(window, text='Set Start Date', command=set_start_date)
            start_date_button.pack(side=tk.LEFT, padx=10, pady=10)

            end_date_button = tk.Button(window, text='Set End Date', command=set_end_date, state=tk.DISABLED)
            end_date_button.pack(side=tk.LEFT, padx=10, pady=10)

        def function3():
            print("Function 3")
# create a variable to hold the selected option
        selected_option = tk.StringVar()

        # set default value of selected option
        selected_option.set("PLOT")
        
        
        # selected_option.place(relx=0.5, rely=0.4, anchor="center")

        # create dropdown menu
        option_menu = tk.OptionMenu(root, selected_option, "Plot from recorded data", "Directly Plot", "Option 3")
        
        # create a button to execute the selected function
        # button = tk.Button(root, text="GO", command=lambda: execute_function(selected_option.get()))
        button = tk.Button(root, text="GO", command=lambda: execute_function(selected_option.get()))
        

        
        # # pack the widgets
        option_menu.pack()
        button.pack()
       
        
       

        # define a function to execute the selected function
        def execute_function(option):
            if option == "Plot from recorded data":
                function1()
            elif option == "Directly Plot":
                function2()
            elif option == "Option 3":
                function3()

        # self.quit_button = tk.Button(self.master, text="Quit", command=self.master.quit)
        # self.quit_button.pack(side=tk.BOTTOM, padx=10, pady=10)

        # self.data_label = tk.Label(self.master, text="")
        # self.data_label.pack(side=tk.BOTTOM, padx=5, pady=5)

   
    def select_button1(self):
        
            def update_plot():
                # Read the data from the AHT20 sensor
                data = ser.readline().decode('utf-8').strip().split(',')
                temperature = float(data[0])
                humidity = float(data[1])
                
                # Update the plot with the new data
                temperature_data.append(temperature)
                humidity_data.append(humidity)
                
                temperature_plot.clear()
                temperature_plot.plot(temperature_data)
                temperature_plot.set_ylabel('Temperature (°C)')
                temperature_plot.set_xlabel('Time (s)')
                
                humidity_plot.clear()
                humidity_plot.plot(humidity_data)
                humidity_plot.set_ylabel('Humidity (%)')
                humidity_plot.set_xlabel('Time (s)')
                
                # Redraw the plot
                temperature_plot.figure.canvas.draw()
                humidity_plot.figure.canvas.draw()
                
                # Schedule the function to run again in 1 second
                root.after(1000, update_plot)
                
            temperature_data = []
            temperature_plot = plt.subplot(2, 1, 1)

            # Create the humidity plot
            humidity_data = []
            humidity_plot = plt.subplot(2, 1, 2)

            # Call the update_plot function to start updating the plot
            update_plot()
         
            plt.show()
        
    def select_button2(self):
        print("Button 2 selected")

    def select_button3(self):
        print("Button 3 selected")

    def select_button4(self):
       print("Button 4 selected")      

    def update_data(self):
        try:
            ser.write(b'r')  # Request data from Arduino
            data = ser.readline().decode('utf-8').strip() 
            # Read data from Arduino
            if data:
                data = data.split(',')
                if len(data) >= 2:
                    temperature = float(data[0]) # convert temperature to float
                    humidity = float(data[1]) # convert humidity to float
                    print("Sensor data: Temperature:", temperature, "Humidity(Rh):", humidity)
                    temperature_font = font.Font(family="Helvetica", size=12, weight="bold")
                    humidity_font = font.Font(family="Helvetica", size=12, weight="bold")
                    
                    # Change background color based on temperature
                    if temperature < 23:
                        temp_bg_color = "#32CD32"
                    elif temperature >= 24 and temperature <= 26:
                        temp_bg_color = "orange"
                    else:
                        temp_bg_color = "red"
                        
                    # Change background color based on humidity
                    if humidity < 45:
                        hum_bg_color = "#32CD32"
                    elif humidity >= 45 and humidity <= 60:
                        hum_bg_color = "orange"
                    else:
                        hum_bg_color = "red"
    
                    self.temp_label.config(text="Temperature : " + str(temperature) + "°C", font=temperature_font, bg=temp_bg_color)
                    self.hum_label.config(text="Humidity(rh) : " + str(humidity) + " %", font=humidity_font, bg=hum_bg_color)
                    
                    import time
                    time.sleep(0)    
                    
                    if data:
                        temp, humidity = data
                        try:
                            with open(r'C:\Downloads\data.csv', 'a', newline='', encoding='utf-8') as csvfile:
                                writer = csv.writer(csvfile)
                                current_date = datetime.datetime.now().strftime("%d-%m-%Y")
                                current_time = datetime.datetime.now().strftime("%H:%M:%S")
                                writer.writerow([current_date,current_time, temp, humidity])
                        except Exception as e:
                            print("Error: ", e)
                    
                    time.sleep(3)    
                            
                    
                else:
                    print("Invalid data received from Arduino:", data)
                    self.data_label.config(text="Live Data")
            else:
                print("Empty data received from Arduino")
                self.data_label.config(text="Live data")
        except Exception as e:
            print("Error reading AHT20 Sensor Data:", e)
            self.data_label.config(text="Live")
        self.master.after(1000, self.update_data)



root = tk.Tk()
root.title("Lab Monitoring System - NanoSIMS")
root.configure(bg="#40E0D0")
app = App(root)
root.mainloop()



