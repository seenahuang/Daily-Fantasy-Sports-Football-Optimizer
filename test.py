import pandas as pd 

NOT_SUNDAY = ['GB', 'CHI', 'HOU', 'NO', 'DEN', 'OAK']

def match(element, array): 
    for i in range(len(array)):
        if element == array[i]:
            return True
    return False

salary_data = pd.read_csv("/Users/seenahuang/Desktop/DFS/DKSalaries.csv")

iterate = salary_data[['TeamAbbrev', 'Name']]
salary_data.drop(['TeamAbbrev'], axis=1)

for i in range(len(iterate)):
    if match(iterate[['TeamAbbrev']].values[0][0], NOT_SUNDAY): 
        iterate.drop(i)

combined_df = iterate.join(salary_data.set_index('Name'), on='Name')
print(combined_df)