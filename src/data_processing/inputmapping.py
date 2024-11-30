import requests
import pandas as pd

def getFinalName(name, df, df_combined) -> str:
    get_col_id = df_combined[df_combined['Player']==name]
    id = get_col_id["Player Code"].iloc[0]
    # Filter rows matching the given ID and create a copy to avoid SettingWithCopyWarning
    matched_rows = df[df['ID'] == id].copy()

    if matched_rows.empty:
        return f"No entries found for ID {id}"

    # Step 1: Combine single-letter words in each name
    matched_rows['Name'] = matched_rows['Name'].apply(
        lambda x: " ".join(
            ["".join([word for word in x.split() if len(word) == 1])] + # Combine single-letter words
            [word for word in x.split() if len(word) > 1]   # Keep longer words
        )

    )
    # print( matched_rows['Name'].str.split())

    # Step 2: Split each name into words and find the minimum length of the instances
    split_names = matched_rows['Name'].str.split().tolist()
    print(split_names)
    print("-------------")
    min_length = min(len(words) for words in split_names)

    # Step 3: Combine words based on the specified rules
    combined_words = []
    print(name)
    
    for i in range(len(name.split(" "))):
        # Get the words at the current index from each instance
        #check if words has i elements
        words_at_index = [words[i] for words in split_names if len(words) > i]

        if words_at_index:  # Check if words_at_index is not empty
            # Select the longest word at the current index
            longest_word = max(words_at_index, key=len)
            combined_words.append(longest_word)

    # Combine the chosen words into a final name
    final_name = " ".join(combined_words)
    return final_name

# Updated URL for direct download
file_id = "1okg9VX3K_KXJVMmTe5pEW4dpyH9XOBfX"
url = f"https://drive.google.com/uc?export=download&id={file_id}"
local_filename = "names.csv"

print("Downloading file...")
# response = requests.get(url, stream=True)
if response.status_code == 200:
    with open(local_filename, 'wb') as file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:  # Filter out keep-alive chunks
                file.write(chunk)
    print("Download complete.")
else:
    print(f"Failed to download file. HTTP status code: {response.status_code}")
    exit()

# Load the CSV into a pandas DataFrame
df = pd.read_csv(local_filename, header=None, names=["ID", "Name"])

combined_df_path = "../data/raw/cricksheet/final/combined_output.csv"
df_combined = pd.read_csv(combined_df_path, header =None, names=['Player','Fantasy Points','Player Code','Match Date','Economy','Strike Rate','4s','6s','Team','City','Match Type'])

# Test the function with a specific ID
name = "JJ Bumrah"  # Replace with the ID you want to test
final_name = getFinalName(name, df, df_combined)
print(f"The final combined name for ID {name} is: {final_name}")
