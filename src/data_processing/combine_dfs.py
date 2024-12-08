import pandas as pd
import os
from concurrent.futures import ThreadPoolExecutor

csv_directory = "../data/interim/product-ui"
output_directory = "../data/interim"
os.makedirs(output_directory, exist_ok=True)

def process_file(filename):
    if filename.endswith(".csv"):
        print(f"Processing: {filename}")
        file_path = os.path.join(csv_directory, filename)
        return pd.read_csv(file_path)
    return pd.DataFrame()  # Return an empty DataFrame if the file is not a CSV

# Use ThreadPoolExecutor for parallel file processing
with ThreadPoolExecutor() as executor:
    filenames = os.listdir(csv_directory)
    csv_files = [filename for filename in filenames if filename.endswith(".csv")]
    
    # Process files in parallel
    dataframes = list(executor.map(process_file, csv_files))

# Combine all DataFrames
combined_dataframe = pd.concat(dataframes, ignore_index=True)

# Sort and save the final DataFrame
combined_dataframe.sort_values(by=['Player'], inplace=True)

output_file = os.path.join(output_directory, "combined_output.csv")
combined_dataframe.to_csv(output_file, index=False)
print(f"Combined and sorted data saved to {output_file}")
