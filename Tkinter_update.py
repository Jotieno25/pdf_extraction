import temp_extraction as tempext
import os
import tkinter as tk
import customtkinter as ctk
from customtkinter import *
from PIL import Image
from tkinter import filedialog
from datetime import datetime
import pandas as pd




def is_valid_date(date_string):
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def is_valid_excel_file(file_path):
    # Check if the file exists and has a valid Excel extension
    if os.path.isfile(file_path) and file_path.lower().endswith(('.xls', '.xlsx')):
        try:
            # Try to read the file using pandas
            pd.read_excel(file_path)
            return True
        except Exception as e:
            print(f"Error reading Excel file: {e}")
            return False
    return False


def run_temp_export(start_date, end_date, config_file, read_file, export_template, output_file_name):
    # Define the date range ! later convert this is UI input
    start_date = start_date
    end_date = end_date

    # read path input
    file_path_temperature = read_file
    file_path_config = config_file
    file_path_export = export_template

    if len(file_path_export) == 0:
        return '\nPlease enter Excel template file'
    elif is_valid_excel_file(file_path_export) is False:
        return '\nError in reading Excel template file'
    elif is_valid_excel_file(file_path_config) is False:
        return '\nError in reading Config file'
    else:
        if len(file_path_temperature) == 0:
            return '\nNo Temperature input file'
        elif is_valid_excel_file(file_path_temperature) is False:
            return '\nError in reading Temperature input file'
        elif is_valid_date(start_date) is False and is_valid_date(end_date) is False:
            return '\nError in date inputs'
        else:
            # running the temperature export
            # set up class object
            temperature_data = tempext.TemperatureData()
            temperature_data.start_date = start_date
            temperature_data.end_date = end_date
            temperature_data.write_path = file_path_export

            # read and set up temperature configuration
            temperature_data.read_temp_config(file_path_config)
            print(temperature_data.config_temp)

            # read house configuration
            temperature_data.read_house_config(file_path_config)

            # read temperature record input and export to export list of dictionaries
            temperature_data.read_temp_record(file_path_temperature)
            temperature_data.filter_temp_record()
            # rearrange export list of dictionaries according to the sheets to be written, first rearrange date then rearrange sheet
            temperature_data.export_list = temperature_data.rearrange_list(temperature_data.export_list, 'date','write_sheet')

            result = temperature_data.write_export()
            if result != 'completed':
                print('\nerror in writing temperature export')
                return result
            else:
                temperature_data.write_workbook.save(output_file_name)
                print('\nCompleted temperature export')
                return f'\nTemperature file written and exported!\n{temperature_data.write_total} records added'




def browse_file(entry):
    filename = filedialog.askopenfilename()
    entry.delete(0, tk.END)
    entry.insert(0, filename)


def run():
    temp_file = temp_file_entry.get()
    start_date = start_date_entry.get()
    end_date = end_date_entry.get()
    bacteria_file = bacteria_file_entry.get()
    template_file = template_file_entry.get()
    output_text_content = run_temp_export(start_date,
                                        end_date,
                                        'Config.xlsx',
                                        temp_file,
                                        template_file,
                                        'output.xlsx')
    output_text.insert(tk.END, output_text_content)
    output_text.see(tk.END)





# Set the appearance and theme (optional)
ctk.set_appearance_mode("Dark")  # Modes: "System", "Dark", "Light"
ctk.set_default_color_theme("dark-blue")  # Themes: "blue" (default), "green", "dark-blue"

# Create the main window
root = ctk.CTk()
root.title("User Interface")
root.geometry("900x700")


logo_image = ctk.CTkImage(Image.open("Arup_logo.png"), size =(100,28))
logo_label = ctk.CTkLabel(root, image =logo_image, text ="")
logo_label.pack(pady=10)

# Define a bold font for section headers
bold_font = ctk.CTkFont(weight="bold", size=14)

# ---------------------------
# Template Export Section
# ---------------------------
template_frame = ctk.CTkFrame(root)
template_frame.pack(pady=10, padx=20, fill="x")

ctk.CTkLabel(template_frame, text="Export to Excel Template File", font=bold_font).grid(row=0, column=0, columnspan=3, pady=5)
ctk.CTkLabel(template_frame, text="File:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
template_file_entry = ctk.CTkEntry(template_frame, width=500)
template_file_entry.grid(row=1, column=1, padx=5, pady=5)
ctk.CTkButton(template_frame, text="Browse", command=lambda: browse_file(template_file_entry)).grid(row=1, column=2, padx=5, pady=5)

# ---------------------------
# Temperature Export Section
# ---------------------------
temp_frame = ctk.CTkFrame(root)
temp_frame.pack(pady=10, padx=20, fill="x")

ctk.CTkLabel(temp_frame, text="Temperature Export", font=bold_font).grid(row=0, column=0, columnspan=3, pady=5)
ctk.CTkLabel(temp_frame, text="File:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
temp_file_entry = ctk.CTkEntry(temp_frame, width=500)
temp_file_entry.grid(row=1, column=1, padx=5, pady=5)
ctk.CTkButton(temp_frame, text="Browse", command=lambda: browse_file(temp_file_entry)).grid(row=1, column=2, padx=5, pady=5)

# ---------------------------
# Temperature Date Section
# ---------------------------
temp_date_frame = ctk.CTkFrame(root)
temp_date_frame.pack(pady=10, padx=20, fill="x")

ctk.CTkLabel(temp_date_frame, text="Start Date: (YYYY-MM-DD)").grid(row=0, column=0, padx=5, pady=5, sticky="w")
start_date_entry = ctk.CTkEntry(temp_date_frame, width=200)
start_date_entry.grid(row=0, column=1, padx=5, pady=5)

ctk.CTkLabel(temp_date_frame, text="End Date: (YYYY-MM-DD)").grid(row=1, column=0, padx=5, pady=5, sticky="w")
end_date_entry = ctk.CTkEntry(temp_date_frame, width=200)
end_date_entry.grid(row=1, column=1, padx=5, pady=5)

# ---------------------------
# Bacteria Export Section
# ---------------------------
bacteria_frame = ctk.CTkFrame(root)
bacteria_frame.pack(pady=10, padx=20, fill="x")

ctk.CTkLabel(bacteria_frame, text="Bacteria Export", font=bold_font).grid(row=0, column=0, columnspan=3, pady=5)
ctk.CTkLabel(bacteria_frame, text="File:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
bacteria_file_entry = ctk.CTkEntry(bacteria_frame, width=500)
bacteria_file_entry.grid(row=1, column=1, padx=5, pady=5)
ctk.CTkButton(bacteria_frame, text="Browse", command=lambda: browse_file(bacteria_file_entry)).grid(row=1, column=2, padx=5, pady=5)

# ---------------------------
# Run Button and Output Text
# ---------------------------
run_frame = ctk.CTkFrame(root)
run_frame.pack(pady=10, padx=20, fill="both", expand=True)

ctk.CTkButton(run_frame, text="Run", command=run, width=150).pack(pady=10)


# CTkTextbox provides a modern text area with built-in styling
output_text = ctk.CTkTextbox(run_frame, width=800, height=200)
output_text.pack(pady=10)



# Start the main event loop
root.mainloop()

