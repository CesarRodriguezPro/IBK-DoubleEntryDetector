import pandas as pd
import datetime
import os 
from collections import defaultdict
''' this will check if there is any wrong entry in the timestation entry log '''


class IrregularEntries:

    def __init__(self, key_api, brk):
        self.brk = brk
        self.key_api = key_api
        self.CODE = 34  # Employee Activity
        self.today = datetime.date.today()
        self.current_monday = self.today - datetime.timedelta(days=self.today.weekday())

        # self.url_data = f"https://api.mytimestation.com/v0.1/reports/?api_key={self.key_api}&" \
        #     f"Report_StartDate={self.current_monday}&Report_EndDate={self.today}&id={self.CODE}&exportformat=csv"
        # self.raw_data = pd.read_csv(self.url_data)
        self.raw_data = pd.read_csv('testData.csv')

    def save_for_test(self):
        self.raw_data.to_csv('testData.csv')

    def process_information(self):
        sorted_db = self.raw_data.sort_values(['Name', 'Date','Time'])
        comparison = sorted_db.shift(-1) == sorted_db
        sorted_db['flag'] = comparison['Name'] & comparison['Date'] & comparison['Activity']
        return sorted_db[sorted_db['flag']]

    def check_dates(self, activity):
        print(activity)

    def check_short_entrys(self):
        self.raw_data['Time'] = pd.to_datetime(self.raw_data['Time'], format='%H:%M').dt.time
        sorted_db = self.raw_data.sort_values(['Name', 'Date'])
        sorted_db = sorted_db[['Name', 'Department', 'Date', 'Activity', 'Time']]
        x = sorted_db.groupby(['Name', 'Date', 'Activity', 'Time'])
        x[['Activity', 'Time']].apply(self.check_dates)












    def display_data(self):
        sorted_db = self.process_information()
        if not sorted_db.empty:
            print('This are Irregular entries -> please check \n ')
            print(sorted_db[sorted_db['flag']][['Name', 'Department','Date', 'Time', 'Activity']].to_string())
            print(self.brk)




if __name__ == "__main__":
    brk = '_' * 120 + '\n'
    key_api = os.environ.get('TimeStationKey')
    active = IrregularEntries(key_api=key_api, brk=brk)
    active.check_short_entrys()

