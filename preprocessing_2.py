import pandas as pd
import numpy as np

#Read data from csv files and json files
movies = pd.read_csv("moviesDb.csv")
gg = pd.read_csv("golden_globe_awards.csv")
oa = pd.read_csv("the_oscar_award.csv")

#phân tích các bảng
def phantich():
    print("Phân tích bảng moviesDb:")
    print(f"Số cột: {len(movies.columns)}")
    for col in movies.columns:
        print(col)

    print("Phân tích bảng golden_globe:")
    print(f"Số cột: {len(gg.columns)}")
    for col in gg.columns:
        print(col)

    print("Phân tích bảng oscar_awards:")
    print(f"Số cột: {len(oa.columns)}")
    for col in oa.columns:
        print(col)

def df_info(df):
    print(df.columns)
    print(df['id'].count())

def oscar_award_processing(df):
    df.dropna(inplace = True)
    df.rename(columns={'year_film': 'year', 'film':'title'}, inplace=True)
    return df

def golden_globe_processing(df):
    df.loc[df['category'] == 'Picture', 'film'] = df.loc[df['category'] == 'Picture', 'nominee']
    df.rename(columns={'year_film':'year', 'film':'title'}, inplace= True)
    df.dropna(inplace=True)
    return df

def movies_db_processing(df):
    df['year'] = df['year'].astype('int64')
    df = df.drop_duplicates(subset=['title', 'year'])
    print(df['id'].count())
    return df

new_oa = oscar_award_processing(oa)
new_gg = golden_globe_processing(gg)
new_movies = movies_db_processing(movies)

print(new_oa[['title', 'year']].head(5))
print(new_gg[['title', 'year']].head(5))
print(new_movies[['title', 'year']].head(5))

movies_gg_df = pd.merge(new_movies, new_gg, how='left', on=['title', 'year'])
movies_gg = movies_gg_df[['id', 'title', 'budget', 'revenue', 'runtime', 'year',
 'success','genre', 'certification_US', 'vote_average', 'vote_count', 'country', 'win']].rename(columns={'win':'win_golden_globe'})
#print(df_info(movies_gg))
gg_count = movies_gg.groupby(['title', 'year'], as_index= False)['win_golden_globe'].count()

movies_oa = pd.merge(new_movies, new_oa, how='left', on=['title', 'year'])[['title', 'year', 'winner']].rename(columns={'winner':'win_oscar_award'})
oa_count = movies_oa.groupby(['title', 'year'], as_index= False)['win_oscar_award'].count()

# gg_count = movies_gg.groupby(['title', 'year']).count()[['title', 'year', 'win_golden_globe']].rename(columns={'win_golden_globe':'win_golden_globe_count'})
# movies_gg = pd.merge(movies_gg.drop_duplicate(subset=['title', 'year']), gg_count, how='left', on=['title', 'year'])
# print(movies_gg.head(10))
movies_gg_count = pd.merge(new_movies, gg_count, how='left', on=['title', 'year'])
movies_gg_oa_count = pd.merge(movies_gg_count, oa_count, how='left', on=['title', 'year'])

print(movies_gg_oa_count)
print(movies_gg_oa_count.columns)
