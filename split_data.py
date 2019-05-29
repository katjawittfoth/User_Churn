import pandas as pd
import numpy as np
import boto3
from keys import *

from datetime import datetime

s3 = boto3.resource('s3')
bucket = s3.Bucket('msds-630-finalproject')

print('Loading from S3...')
client = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)
obj = client.get_object(Bucket='msds-630-finalproject', Key='session_100000.csv')
sessions = pd.read_csv(obj['Body'])

print('Successfully read from S3 and convert to Pandas...')
sessions = sessions[['user_id_hash','start_timestamp']]
print('Drop all columns...')
sessions.to_csv('sessions_user_starttime.csv')
print('Save all rows with 2 columns...')
sessions['start_timestamp'] = pd.to_datetime(sessions['start_timestamp'], unit='ms')
print('Convert datetime object...')
dec1_cutoff = datetime(2018, 12, 1, 0, 0, 0)
dec14_cutoff = datetime(2018, 12, 14, 0, 0, 0)
print('Starting to filter data')
session_train = sessions[sessions['start_timestamp'] < dec1_cutoff]
session_dec1_dec14 = sessions[sessions['start_timestamp'] > dec1_cutoff]
print('Done December split...')
session_test = session_dec1_dec14[session_dec1_dec14['start_timestamp'] < dec14_cutoff]
print('Done splitting by date...\nStarting to find unique user_id...')
session_train = session_train.user_id_hash.unique()
print('Shuffling data...')
np.random.shuffle(session_train)
print(session_train.shape)
session_rows = session_train.shape[0]
train = session_train[:int(session_rows*1.0*0.8)]
val = session_train[int(session_rows*1.0*0.8):]
print('Done splitting')

print('Taking out user in test set but not in training set...')
test = session_test.user_id_hash.unique()

train = set(train)
test = set(test)
test = train.intersection(test)

train = list(train)
test = list(test)

"""
test = []
for i in test_temp:
    for j in train:
        if(i == j): 
            test.append(i)
            continue
"""
print('Done! Saving the files...')
test = pd.DataFrame(test)
train = pd.DataFrame(train)
val = pd.DataFrame(test)
train.to_csv("train.csv", index=False)
val.to_csv("val.csv", index=False)
test.to_csv("test.csv", index=False)
print('All done!')