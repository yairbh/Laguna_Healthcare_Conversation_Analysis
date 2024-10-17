"""
Find CM by two metrics:
1- The speaker with max(count) of questions marks
2- The speaker who said 'recorded' first
Column 'CM' holds values 'True' for CMs and 'False' for members
"""
#imports
import pandas as pd
import numpy as np

def count_question_marks(group):
    group['?_count'] = group['text'].str.count(r'\?(\s*\?)+|\?')
    #group['?_count'] = group['text'].str.count(r'\?')#
    return group

def first_recorded_speaker(df):
    first_recorded = df[df['text'].str.contains(r'\recorded\b', case=False, na=False)].head(1)
    if not first_recorded.empty:
        df['first_recorded_speaker'] = first_recorded['speaker'].values[0]
    else:
        df['first_recorded_speaker'] = None
    return df

def first_this_is(df):
    first_this_is = df[df['text'].str.contains(r'this is', case=False, na=False)].head(1)
    if not first_this_is.empty:
        df['first_this_is'] = first_this_is['speaker'].values[0]
    else:
        df['first_this_is'] = None
    return df

#def choose_CM(row):
    #    if pd.isna(row['first_recorded_speaker']) and pd.isna(row['speaker_most']):
    #        return np.nan
    #   elif pd.isna(row['first_recorded_speaker']):
    #        return row['speaker_most']
    #    elif pd.isna(row['speaker_most']):
    # row['first_recorded_speaker']
    #   elif row['first_recorded_speaker'] == row['speaker_most']:
    #       return row['first_recorded_speaker']
    #   elif row['first_recorded_speaker'] != row['speaker_most']:
#       return row['first_recorded_speaker']
##
def choose_CM(row):
    if pd.isna(row['first_recorded_speaker']) and pd.isna(row['speaker_most']) & pd.isna(row['first_this_is']):
        return np.nan

    elif row['first_recorded_speaker'] == row['speaker_most'] == row['first_this_is']:
        return row['first_recorded_speaker']

    elif (row['first_recorded_speaker'] == (row['first_this_is'])) and (
            row['first_recorded_speaker'] != row['speaker_most']):
        return row['first_recorded_speaker']

    elif pd.isna(row['first_recorded_speaker']):
        return row['first_this_is']

    elif pd.isna(row['first_this_is']):
        return row['speaker_most']

    elif pd.isna(row['speaker_most']):
        return row['first_recorded_speaker']



#upload data
df = pd.read_csv('raw_df_.csv')

#sort data by time, to find the first occurrence of the word 'recorded'
df = df.sort_values(by=['recording_id', 'time'])

#  identify the first occurrence of 'record'
df_recorded = df.groupby('recording_id').apply(first_recorded_speaker)

#prepare df for merge by 'recording_id'
df_recorded = df_recorded[['first_recorded_speaker']].reset_index()[['recording_id','first_recorded_speaker']]
df_recorded = df_recorded.drop_duplicates()
df_recorded = df_recorded.set_index('recording_id')



df_this_is = df.groupby('recording_id').apply(first_this_is)
df_this_is = df_this_is[['first_this_is']].reset_index()[['recording_id','first_this_is']]
df_this_is = df_this_is.drop_duplicates()
df_this_is = df_this_is[['recording_id','first_this_is']].drop_duplicates().set_index('recording_id')


df_ = df.copy()
df_ = pd.merge(df_, df_recorded, on='recording_id', how='left')
df_ = pd.merge(df_, df_this_is, on='recording_id', how='left')


df_qmarks = df.sort_values(by=['recording_id', 'time']) #sort by id and time

#find speaker with max(count) questions marks
df_qmarks = df_qmarks.groupby(['recording_id', 'speaker']).apply(count_question_marks).reset_index(drop=True)
question_counts = df_qmarks.groupby(['recording_id', 'speaker'])['?_count'].sum().reset_index()
most_questions_speaker = question_counts.loc[question_counts.groupby('recording_id')['?_count'].idxmax()]
df_qmarks = df_qmarks.merge(question_counts, on=['recording_id', 'speaker'], suffixes=('', '_sum'))
df_qmarks = df_qmarks.merge(most_questions_speaker[['recording_id', 'speaker']], on='recording_id', suffixes=('', '_most'))
df_qmarks = df_qmarks[['recording_id','speaker_most']].drop_duplicates().set_index('recording_id')


df_ = pd.merge(df_, df_qmarks, on='recording_id', how='left')



df_merged = df_[['recording_id','first_recorded_speaker','speaker_most','first_this_is']].drop_duplicates()


df_merged['CM_'] = df_merged.apply(choose_CM, axis=1)
df_CM = df_merged[['recording_id','CM_']]

df_final = pd.merge(df_, df_CM, on='recording_id', how='left')

df_final['CM'] = df_final['speaker'] == df_final['CM_']
df_final = df_final.drop(columns=['CM_','Unnamed: 0','utterance_id','member_id','file_name'])
#TODO remove redundant cols


print(df_final.head())
print(df_CM['CM_'].value_counts())

#QA
a = df_merged[df_merged['recording_id'] == '00190bc2-3aa4-43d5-9e92-5f6be6767f93']

print('Completed!')