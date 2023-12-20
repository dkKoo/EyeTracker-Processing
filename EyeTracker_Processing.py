import pandas as pd
import numpy as np
import zipfile
import os
import re 
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

#Open the raw data extracted by EyeTracker and save it as excel data
#Compress the above data into a zip file
#open zip file with code

def analyze_eye_tracking_data(file_path):
    # Load data
    data = pd.read_csv(file_path, sep='\t')

    # Calculate total and average speeds
    data['Left Total Speed'] = np.sqrt(data['Left Vert Speed']**2 + data['Left Horyz Speed']**2)
    data['Right Total Speed'] = np.sqrt(data['Right Vert Speed']**2 + data['Right Horyz Speed']**2)
    avg_speed_left = data['Left Total Speed'].mean()
    avg_speed_right = data['Right Total Speed'].mean()

    # Calculate CV
    cv_left = data['Left Total Speed'].std() / avg_speed_left
    cv_right = data['Right Total Speed'].std() / avg_speed_right

    # Calculate correlations
    corr_horizontal = data[['Left X', 'Right X']].corr().iloc[0, 1]
    corr_vertical = data[['Left Y', 'Right Y']].corr().iloc[0, 1]

    return {
        'file_name': os.path.basename(file_path),
        'average_speed_left': avg_speed_left,
        'average_speed_right': avg_speed_right,
        'cv_left': cv_left,
        'cv_right': cv_right,
        'correlation_horizontal': corr_horizontal,
        'correlation_vertical': corr_vertical
    }

def extract_common_pattern(file_name):
    """
    Extract common patterns from file names.
    ex: 'Hor_Cho_1.txt' -> 'Hor_Cho'
    """
    match = re.match(r"(.+)_\d+", file_name)
    if match:
        return match.group(1)
    return None

def process_zip_and_analyze(zip_file_path, save_path):
    # Directory for extracted files
    extraction_path = os.path.splitext(zip_file_path)[0] + '/'

    # Extract ZIP file
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extraction_path)

    # Analyzing extracted files
    extracted_files = os.listdir(extraction_path)
    all_results = {}

    for file in extracted_files:
        if file.endswith('.txt'):
            common_pattern = extract_common_pattern(file)
            if common_pattern not in all_results:
                all_results[common_pattern] = []

            result = analyze_eye_tracking_data(os.path.join(extraction_path, file))
            all_results[common_pattern].append(result)

    # Averaging results and selecting specific metrics
    averaged_results = []
    for pattern, results in all_results.items():
        df = pd.DataFrame(results)

        # Calculate new average metrics
        df['average_speed'] = (df['average_speed_left'] + df['average_speed_right']) / 2
        df['cv'] = (df['cv_left'] + df['cv_right']) / 2

        # Add the new averages to the original average results
        averaged_result = df.mean(numeric_only=True).to_dict()
        averaged_result['pattern'] = pattern
        averaged_results.append(averaged_result)

    # Creating the DataFrame with specific columns
    results_df = pd.DataFrame(averaged_results)
    results_df = results_df[['pattern', 'average_speed', 'cv', 'correlation_horizontal', 'correlation_vertical']]

    # Save the DataFrame to an Excel file
    excel_file_path = os.path.join(save_path, 'eye_tracking_analysis_selected_results.xlsx')
    results_df.to_excel(excel_file_path, index=False)

    return excel_file_path

# GUI for file selection and save path
def gui_select_file_and_path():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Select ZIP file
    zip_file_path = filedialog.askopenfilename(title="Select ZIP file", filetypes=[("ZIP files", "*.zip")])
    if not zip_file_path:
        messagebox.showinfo("No File Selected", "You did not select a file.")
        return

    # Select save path
    save_path = filedialog.askdirectory(title="Select Save Directory")
    if not save_path:
        messagebox.showinfo("No Directory Selected", "You did not select a directory.")
        return

    # Process and analyze the file
    excel_file_path = process_zip_and_analyze(zip_file_path, save_path)
    messagebox.showinfo("Completed", f"Analysis results saved to: {excel_file_path}")

# Run the GUI
gui_select_file_and_path()
