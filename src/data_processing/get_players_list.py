import pandas as pd

def getPlayersList(file_path, output_path):
    with open(file_path, 'r') as file:
        data = pd.read_csv(file)
        data = data.iloc[:, 0]
        data = data.drop_duplicates()
        print(data)
        data.to_csv(output_path, index=False, header=False)


path = '../data/processed/final.csv'
output_path = '../data/processed/players_list.csv'

data = getPlayersList(path, output_path)
