import pandas as pd
import glob

# Path to the folder containing your CSV files
csv_files = glob.glob("H:/CaseStudy/casestudycsv/*.csv")  # Update this path as needed

# Initialize an empty list to store metadata
metadata_list = []

for file in csv_files:
    # Read the first 5 rows (metadata section)
    df = pd.read_csv(file, nrows=5, header=None)
    
    # Transpose the metadata for easier handling
    metadata = df.set_index(0).T
    
    # Add a column for the file name (to track the source of the metadata)
    metadata['Source_File'] = file
    
    # Append the metadata to the list
    metadata_list.append(metadata)

# Combine all metadata into a single DataFrame
metadata_df = pd.concat(metadata_list, ignore_index=True)

# Save the aggregated metadata to a CSV file
metadata_df.to_csv("H:/CaseStudy/Aggregates/Aggregated_Metadata.csv", index=False)

# Display a sample of the aggregated metadata
print(metadata_df.head())
