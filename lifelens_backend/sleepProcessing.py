import pandas as pandas;
import matplotlib.pyplot as plt

#Processing and cleaning data
sleepData = pandas.read_csv('sleeps.csv', nrows = 24)
filtered_Data = sleepData[sleepData['Nap'] != True]
filtered_Data = filtered_Data.iloc[1:]

filtered_Data.to_csv('sleepData.csv', index=False)