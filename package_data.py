import pandas as pd


def extract_values(df): 
    info_vector = []
    for i in range(len(df)):
        info = df.iloc[[i]][['Name','Salary']]
        name = info['Name'].values[0]
        salary = info['Salary'].values[0]
        info_vector.append((name, salary))
    return info_vector



def package(data):
    positions = data.groupby('Position')
    running_back_df = positions.get_group('RB').sort_values(by=['Salary'],ascending=False)
    wide_receiver_df = positions.get_group('WR').sort_values(by=['Salary'],ascending=False)
    quarterback_df = positions.get_group('QB').sort_values(by=['Salary'],ascending=False)
    tight_end_df = positions.get_group('TE').sort_values(by=['Salary'],ascending=False)
    defense_df = positions.get_group('DST').sort_values(by=['Salary'],ascending=False)

    all_positions = [running_back_df, wide_receiver_df, quarterback_df, tight_end_df, defense_df]

    all_positions_info = []

    for i in range(len(all_positions)): 
        all_positions_info.append(extract_values(all_positions[i]))

    return all_positions_info


