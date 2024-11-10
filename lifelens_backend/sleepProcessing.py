import pandas as pandas;

sleepData = pandas.read_csv('sleeps.csv');

print(sleepData.head())

# sleepData.fillna()

sleepData['Sleep Duration'] = pandas.to_datetime(sleepData['Wake onset']) - pandas.to_datetime(sleepData['Sleep onset']);

print(sleepData['Sleep Duration']);

optimal_light_sleep = 0.55 * sleepData['Sleep Duration'];
optimal_deep_sleep = 0.20 * sleepData['Sleep Duration'];
optimal_rem_sleep = 0.25 * sleepData['Sleep Duration'];
# optimal_total_sleep = 0.25 * sleepData['Sleep Duration'];

# optimal_light_sleep_hours = optimal_light_sleep.dt.components['hours']
# optimal_light_sleep_minutes = optimal_light_sleep.dt.components['minutes']

optimal_light_sleep_str = optimal_light_sleep.dt.floor('min').astype(str).str[-8:-3]

print(optimal_light_sleep);
print(optimal_deep_sleep);
print(optimal_rem_sleep);

sleepData['Light Sleep Difference'] = sleepData['Light sleep duration (min)'] - optimal_light_sleep;
sleepData['Deep Sleep Difference'] = sleepData['Deep (SWS) duration (min)'] - optimal_deep_sleep;
sleepData['REM Sleep Difference'] = sleepData['REM duration (min)'] - optimal_rem_sleep;

print(sleepData['Light Sleep Difference']);
print(sleepData['Deep Sleep Difference']);
print(sleepData['REM Sleep Difference']);
