from datetime import datetime
import pandas as pd
import numpy as np

def timeconvert(ts):
    ts = int(ts)/1000
    return (datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))

def preprocess(events):
    events = events.loc[events.event=='8'] # take purchase events only 
    events['time'] = events['event_timestamp'].apply(timeconvert)
    events['time'] = pd.to_datetime(events['time']) 
    events['day_current'] = events['time'].dt.dayofyear # convert to day of year
    
    purchase = events.groupby(['user_id_hash','day_current'])['event'].count() # total purchase amt 
    purchase = purchase.to_frame()
    purchase['event'] = 1
    return purchase.reset_index()


def extract_purchase_dec(purchase):

    purchase_14 = purchase.loc[purchase.day_current > 334] # purchase in first two weeks of Dec
    purchase_7 = purchase_14.loc[purchase_14.day_current < 342] # purchase in the first week of Dec
    purchase_14 = purchase_14.groupby("user_id_hash")['event'].count().to_frame()
    purchase_14['event'] = 1
    purchase_7 = purchase_7.groupby("user_id_hash")['event'].count().to_frame()
    purchase_7['event'] = 1
    return purchase_7, purchase_14

def merge(user_id,purchase_7,purchase_14):
    user_id = pd.DataFrame(user_id['user_id_hash'])
    label = pd.merge(user_id, purchase_7, on=['user_id_hash'], how='left')
    label = pd.merge(label, purchase_14, on=['user_id_hash'], how='left')
    label.columns = ["user_id_hash", "user_purchase_binary_7_days", "user_purchase_binary_14_days"]
    label = label.fillna(0)
    return label

events = pd.read_csv('events.csv')
user_id_hash = events.user_id_hash.unique()
user_id = pd.DataFrame(user_id_hash)
user_id.columns = ['user_id_hash']

purchase = preprocess(events)
purchase_7, purchase_14 = extract_purchase_dec(purchase)

label = pd.merge(user_id, purchase_7, on = 'user_id_hash', how='left')
label = pd.merge(label, purchase_14, on='user_id_hash', how='left')

label = label.fillna(0)
label.columns = ['user_id_hash','user_purchase_binary_7_days','user_purchase_binary_14_days']
label.to_csv('label.csv', index=False)
