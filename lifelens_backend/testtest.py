import pandas as pd
import matplotlib.pyplot as plt

# Load the sleepData CSV
sleepData = pd.read_csv('sleepData.csv')

# Convert "Sleep onset" or another date column to a datetime format if it's not already
sleepData['Sleep Date'] = pd.to_datetime(sleepData['Sleep onset']).dt.date

# Calculate optimal sleep durations in minutes
sleepData['Sleep Duration'] = (pd.to_datetime(sleepData['Wake onset']) - pd.to_datetime(sleepData['Sleep onset'])).dt.total_seconds() / 60
optimal_light_sleep = 0.55 * sleepData['Sleep Duration']
optimal_deep_sleep = 0.20 * sleepData['Sleep Duration']
optimal_rem_sleep = 0.25 * sleepData['Sleep Duration']

# Calculate the differences (actual vs. optimal)
sleepData['Light Sleep Difference'] = sleepData['Light sleep duration (min)'] - optimal_light_sleep
sleepData['Deep Sleep Difference'] = sleepData['Deep (SWS) duration (min)'] - optimal_deep_sleep
sleepData['REM Sleep Difference'] = sleepData['REM duration (min)'] - optimal_rem_sleep

# Plotting each sleep category's actual vs. optimal durations with dates on the x-axis
plt.figure(figsize=(14, 10))

# Light Sleep
plt.subplot(3, 1, 1)
plt.plot(sleepData['Sleep Date'], sleepData['Light sleep duration (min)'], label='Actual Light Sleep (min)')
plt.plot(sleepData['Sleep Date'], optimal_light_sleep, label='Optimal Light Sleep (min)', linestyle='--')
plt.bar(sleepData['Sleep Date'], sleepData['Light Sleep Difference'], color='skyblue', alpha=0.5, label='Difference')
plt.ylabel('Light Sleep (min)')
plt.legend()

# Deep Sleep
plt.subplot(3, 1, 2)
plt.plot(sleepData['Sleep Date'], sleepData['Deep (SWS) duration (min)'], label='Actual Deep Sleep (min)')
plt.plot(sleepData['Sleep Date'], optimal_deep_sleep, label='Optimal Deep Sleep (min)', linestyle='--')
plt.bar(sleepData['Sleep Date'], sleepData['Deep Sleep Difference'], color='orange', alpha=0.5, label='Difference')
plt.ylabel('Deep Sleep (min)')
plt.legend()

# REM Sleep
plt.subplot(3, 1, 3)
plt.plot(sleepData['Sleep Date'], sleepData['REM duration (min)'], label='Actual REM Sleep (min)')
plt.plot(sleepData['Sleep Date'], optimal_rem_sleep, label='Optimal REM Sleep (min)', linestyle='--')
plt.bar(sleepData['Sleep Date'], sleepData['REM Sleep Difference'], color='purple', alpha=0.5, label='Difference')
plt.xlabel('Sleep Date')
plt.ylabel('REM Sleep (min)')
plt.legend()

plt.tight_layout()
plt.show()
