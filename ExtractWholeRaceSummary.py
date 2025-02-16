import csv
import pandas as pd
import glob

# Path to the folder containing your CSV files
folder_path = "H:/CaseStudy/casestudycsv/*.csv"

# List to store the aggregated data
aggregated_data = []

# Process each file in the folder
for file in glob.glob(folder_path):
    try:
        with open(file, "r") as f:
            reader = csv.reader(f)
            rows = list(reader)  # Convert to a list for indexing
            
            # Locate the "Whole Race Summary" row
            summary_row_index = next((i for i, row in enumerate(rows) if len(row) > 0 and row[0] == "Whole Race Summary"), None)
            if summary_row_index is None:
                print(f"'Whole Race Summary' not found in {file}")
                continue
            
            # Ensure there are enough rows following "Whole Race Summary"
            if summary_row_index + 2 >= len(rows):
                print(f"Not enough rows after 'Whole Race Summary' in {file}")
                continue
            
            # Extract the header and data rows
            header_row = rows[summary_row_index + 1]
            data_row = rows[summary_row_index + 2]
            
            # Add the data row to the aggregated data with the source file
            data_dict = {header: value for header, value in zip(header_row, data_row)}
            data_dict['Source_File'] = file
            aggregated_data.append(data_dict)
    
    except Exception as e:
        print(f"Error processing file {file}: {e}")

# Create a DataFrame from the aggregated data
if aggregated_data:
    aggregated_df = pd.DataFrame(aggregated_data)
    # Save the aggregated data to a CSV file
    output_path = "H:/swimsmarter/Aggregated_Whole_Race_Summaryredo.csv"
    aggregated_df.to_csv(output_path, index=False)
    print(f"Aggregation completed. Saved to {output_path}")
else:
    print("No valid data found in the folder.")

# Display a sample of the aggregated data
if 'aggregated_df' in locals():
    print(aggregated_df.head())
