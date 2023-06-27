import os
import csv
import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from datetime import datetime
import locale

# variables
directory_path = os.path.dirname(os.path.abspath(__file__))
name_default_csv = 'output'

def convert_size(size_in_bytes):
    size_in_mb = size_in_bytes / (1024 * 1024)
    return round(size_in_mb, 2)

def parse_directory(directory):
    file_list = []
    script_file = os.path.basename(sys.argv[0])
    locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')  # Set French locale for date formatting
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file != script_file:
                file_path = os.path.join(root, file)
                file_name, file_ext = os.path.splitext(file)
                file_size = os.path.getsize(file_path)
                file_size_mb = convert_size(file_size)
                file_date = os.path.getmtime(file_path)
                file_date_fr = datetime.fromtimestamp(file_date).strftime('%d/%m/%Y')  # Format date in French
                file_info = {
                    'Name': file_name,
                    'Date': file_date_fr,
                    'Path': os.path.relpath(file_path, directory),
                    'Extension': file_ext,
                    'Size': file_size,
                    'Size_mb': file_size_mb
                }
                file_list.append(file_info)
    return file_list

def export_to_csv(file_list, output_file):
    fieldnames = ['Name', 'Date', 'Path', 'Extension', 'Size', 'Size_mb']
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(file_list)
    print(f"CSV export completed. Output file: {output_file}")

def browse_directory():
    directory = filedialog.askdirectory(title="Select Directory")
    if directory:
        directory_entry.delete(0, tk.END)
        directory_entry.insert(0, directory)

def browse_output_directory():
    output_directory = filedialog.askdirectory(title="Select Output Directory")
    if output_directory:
        output_directory_entry.delete(0, tk.END)
        output_directory_entry.insert(0, output_directory)

def change_name_output():
    global name_default_csv
    name_default_csv = output_file_entry.get()

def execute_script():
    directory = directory_entry.get()
    output_directory = output_directory_entry.get()

    if directory and output_directory:
        file_list = parse_directory(directory)
        output_file = os.path.join(output_directory, f'{name_default_csv}.csv')
        export_to_csv(file_list, output_file)
        tk.messagebox.showinfo("CSV Export", "CSV export completed successfully.")
    else:
        tk.messagebox.showwarning("Missing Input", "Please select both the directory and output directory.")

# Create the main Tkinter window
window = tk.Tk()
style = ttk.Style(window)
style.theme_use("clam")
window.title("Directory Parser")
window.geometry("500x325")

# Create and position the directory selection widgets
directory_label = tk.Label(window, text="Select Directory:")
directory_label.pack()

directory_entry = tk.Entry(window, width=50)
directory_entry.pack()

browse_directory_button = tk.Button(window, text="Browse", command=browse_directory)
browse_directory_button.pack()

# Create and position the output directory selection widgets
output_directory_label = tk.Label(window, text="Select Output Directory:")
output_directory_label.pack()

output_directory_entry = tk.Entry(window, width=50)
output_directory_entry.insert(0, directory_path)
output_directory_entry.pack()

browse_output_directory_button = tk.Button(window, text="Browse", command=browse_output_directory)
browse_output_directory_button.pack()

# Get name of csv output file
output_file_label = tk.Label(window, text="Rename CSV file")
output_file_label.pack()

output_file_entry = tk.Entry(window, width=20)
output_file_entry.insert(0, name_default_csv)
output_file_entry.pack()

add_output_file_button = tk.Button(window, text="Add", command=change_name_output)
add_output_file_button.pack()



#run
browse_output_directory_button = tk.Button(window, text="Run it!", command=execute_script, borderwidth=5, bg = "red")
browse_output_directory_button.pack(padx=20, pady=20)

# Start the GUI event loop
window.mainloop()
