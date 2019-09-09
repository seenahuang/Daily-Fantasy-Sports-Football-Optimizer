import pandas as pd
import math
  
# salary_df: dataframe of salaries for one position
# projection_df: dataframe of projections for one position
# count: number of players being considered for this position
# extract_values: combines two ,
# put name, salary, and projection fields into array
def extract_values(salary_df, projection_df, count):
    combined_df = salary_df.join(projection_df.set_index('Name'), on='Name')
    combined_df = combined_df.sort_values(by=['Salary'], ascending=False)
    info_vector = []
    for i in range(count):
        info = combined_df.iloc[[i]][['Name','Salary','FPTS']]
        name = info['Name'].values[0]
        salary = info['Salary'].values[0]
        projection = info['FPTS'].values[0]
        if math.isnan(projection):
            info_vector.append((name, salary, 0))
        else:
            info_vector.append((name,salary,projection))
    return info_vector


# salary_data: full data for salaries of each player, all positions
# position_projections: array of df that has projections per position. Order of array must be qb, rb, wr, te, d
# position_counts: array of how many players being considered for each position. Order must be qb, rb, wr, te, d
# package: splits salary data by position. Return array of arrays, each element is array of
# (name,salary, projection) for each position in rb, wr, qb, te, d order
def package(salary_data, position_projections, position_counts):
    positions = salary_data.groupby('Position')
    #salary dataframes
    running_back_df = positions.get_group('RB').sort_values(by=['Salary'],ascending=False)
    wide_receiver_df = positions.get_group('WR').sort_values(by=['Salary'],ascending=False)
    quarterback_df = positions.get_group('QB').sort_values(by=['Salary'],ascending=False)
    tight_end_df = positions.get_group('TE').sort_values(by=['Salary'],ascending=False)
    defense_df = positions.get_group('DST').sort_values(by=['Salary'],ascending=False)

    all_salaries = [quarterback_df,running_back_df, wide_receiver_df, tight_end_df, defense_df]


    all_positions_info = []

    for i in range(len(all_salaries)):
        all_positions_info.append(extract_values(all_salaries[i], position_projections[i], position_counts[i]))

    return all_positions_info

def only_sunday(df_list, teams):
    for df in df_list:
        df.drop(teams)
