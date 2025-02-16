import csv
import pandas as pd
import glob

# Path to the folder containing your CSV files
folder_path = "H:/CaseStudy/casestudycsv/*.csv"

# List to store the aggregated data
aggregated_lap_data = []

# Process each file in the folder
for file in glob.glob(folder_path):
    try:
        with open(file, "r") as f:
            reader = csv.reader(f)
            rows = list(reader)  # Convert to a list for indexing
            
            # Locate the "Lap Summary" row
            lap_summary_index = next((i for i, row in enumerate(rows) if len(row) > 0 and row[0] == "Lap Summary"), None)
            if lap_summary_index is None:
                print(f"'Lap Summary' not found in {file}")
                continue
            
            # Extract data after the "Lap Summary" row
            lap_summary_data = rows[lap_summary_index + 1:]  # All rows after the marker
            if len(lap_summary_data) < 2:
                print(f"No valid lap data found after 'Lap Summary' in {file}")
                continue
            
            # Extract headers and data
            headers = lap_summary_data[0]  # Header row
            data = lap_summary_data[1:]    # Data rows
            
            # Create a DataFrame for the lap summary
            lap_df = pd.DataFrame(data, columns=headers)
            
            # Replace empty cells in "50 splits" with Null
            if "50 splits" in lap_df.columns:
                lap_df["50 splits"].replace("", pd.NA, inplace=True)
            
            # Add a Source_File column
            lap_df['Source_File'] = file
            
            # Append to the aggregated data list
            aggregated_lap_data.append(lap_df)
    
    except Exception as e:
        print(f"Error processing file {file}: {e}")

# Combine all lap summaries into a single DataFrame
if aggregated_lap_data:
    aggregated_df = pd.concat(aggregated_lap_data, ignore_index=True)
    
    # Save the aggregated lap summary data to a CSV file
    output_path = "H:/CaseStudy/Aggregates/Aggregated_Lap_Summaryredo.csv"
    aggregated_df.to_csv(output_path, index=False)
    print(f"Aggregation completed. Saved to {output_path}")
else:
    print("No valid lap data found in the folder.")

# Display a sample of the aggregated data
if 'aggregated_df' in locals():
    print(aggregated_df.head())
