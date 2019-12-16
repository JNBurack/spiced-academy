import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import timedelta

class Supermarket():

    def __init__(self):
        self.supermarket = []

        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
        dfs = []

        for day in days:
            print(day)
            day = pd.read_csv(f'/Users/justinburack/github/hypepperameters-code/Week9/{day}.csv', sep=';')
            dfs.append(day)
            print(day)

        dfs2 = []
        for df in dfs:
    # For df in the list of dfs, sort by customer_no
            df.set_index('customer_no')
            df.sort_index()
        # Set index to timestamp and append to second list
            df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
            dfs2.append(df)
            #return self.dfs2

        # Separate into separate dfs by customer_no
        customer_no_dfs = []
        for day in dfs2:
            customer_no_df = []
            for customer_no, sam in day.groupby('customer_no'):
                #print(sam)
                #print('max', sam['timestamp'].max())
                #print('min', sam['timestamp'].min())
                customer_no_df.append(sam)
            customer_no_dfs.append(customer_no_df)

        for day in customer_no_dfs:
            day_list = []
            for item in day:
                item = item.set_index('timestamp').reset_index()
                item = self.add_thirty(item)
                #print('length of DF is:', len(item))
                #print('length of DAY is:', len(day))
                #print('length of ENTIRE is:', len(customer_no_dfs))
                day_list.append(item)
                #print('***APPENDED***')
            self.supermarket.append(day_list)

        return
    #return self.supermarket

    # Upsamples customer_no subsamples in 30s intervals and eliminates non-unique indices
    def add_thirty(self, sam):
        for index, row in sam.iterrows():
            try:
                if sam['timestamp'][index+1] == sam['timestamp'][index]:
                    print(sam['timestamp'][index+1], 'is identical to', sam['timestamp'][index])
                    sam['timestamp'][index+1] += timedelta(seconds=30)
                    print('new timestamp is now', sam['timestamp'][index+1])
            except(KeyError):
                pass
            sam = sam.set_index('timestamp').resample('30s').ffill()
            return sam

    # Drops duplicates from customer_no subsamples
    def drop_duplicate(self, sam):
        for index, row in sam.iterrows():
            try:
                if sam['timestamp'][index+1] == sam['timestamp'][index]:
                    print(sam['timestamp'][index+1], 'is identical to', sam['timestamp'][index])
                    sam.drop([index+1], axis=0, inplace=True)
                    print('duplicate row dropped')
            except(KeyError):
                pass
            return self.sam
