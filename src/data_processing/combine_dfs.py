import pandas as pd
import os

csv_directory = "../data/raw/cricksheet/interim"
output_directory = "../data/raw/cricksheet/final"
os.makedirs(output_directory, exist_ok=True)  

combined_dataframe = pd.DataFrame() 

for filename in os.listdir(csv_directory):
    if filename.endswith(".csv"):
        print(filename)
        file_path = os.path.join(csv_directory, filename)
        
        df = pd.read_csv(file_path)
        
        combined_dataframe = pd.concat([combined_dataframe, df], ignore_index=True)

combined_dataframe.sort_values(by=['Player'], inplace=True)

output_file = os.path.join(output_directory, "combined_output.csv")
combined_dataframe.to_csv(output_file, index=False)
print(f"Combined and sorted data saved to {output_file}")
