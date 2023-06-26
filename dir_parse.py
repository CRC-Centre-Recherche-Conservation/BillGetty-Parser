import os
import csv
import sys
from datetime import datetime
import locale

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
                    'Size': file_size
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

# Usage example
directory_path = os.path.dirname(os.path.abspath(__file__))  # Replace with the target directory path
output_csv_file = 'output.csv'  # Replace with the desired output CSV file name

file_list = parse_directory(directory_path)
export_to_csv(file_list, output_csv_file)