import pandas as pd
import os

# Directory containing the CSV files
csv_directory = "../data/raw/cricksheet/interim"

output_directory = "../data/raw/cricksheet/final"
os.makedirs(output_directory, exist_ok=True)  

# Initialize an empty DataFrame
combined_dataframe = None

# Loop through all files in the directory
for filename in os.listdir(csv_directory):
    if filename.endswith(".csv"):
        print(filename)
        # Construct full file path
        file_path = os.path.join(csv_directory, filename)
        
        # Read the CSV file, skipping the first row
        df = pd.read_csv(file_path, skiprows=1)
        
        # If combined_dataframe is None, initialize it with the first DataFrame
        if combined_dataframe is None:
            combined_dataframe = df
        else:
            # Join with the existing DataFrame
            combined_dataframe = combined_dataframe.join(df, how='outer', rsuffix=f"_{filename}")

combined_dataframe.sort_values(by=['Player', 'Match Type'], inplace=True)

# Save the combined DataFrame to a new CSV file if needed
output_file = "combined_output.csv"
combined_dataframe.to_csv(output_file, index=False)
print(f"Combined data saved to {output_file}")
