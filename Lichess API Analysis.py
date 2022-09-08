# Track Chess Ratings over time and see progress
# By Shyam Kumar Rajput
import requests
import berserk
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
from scipy import stats


# API - retrieving data
session = berserk.TokenSession("lip_0aD0JjE76AuLNaMFPbDj")
client = berserk.Client(session=session)
user = "skrajput01"
all_data = requests.get(f'https://lichess.org/api/user/{user}/rating-history').json()

# dates-rankings as array for a specific Chess variant
variant_data = np.asarray(all_data[8]['points'])
#0. Bullet, 1. Blitz, 2. Rapid, 3. Classical, 4. Correspondence, 5. Chess960, 6. King of the Hill, 7.Three-check, 8. Antichess, 9. Atomic, 10.Racing Kings, 11.Crazyhouse, 12.UltraBullet

# Issue (solved) - Month values are 0-11 (datetime requies 1-12)
variant_data[:, 1] = variant_data[:, 1] + 1
print(variant_data)

# (y-axis) rankings
y_rankings = variant_data[:,3]
# (x-axis) dates 
dates_dates = variant_data[:,:3]
x_dates = [datetime.date(*x) for x in variant_data[:,:3]]
new_dates = []
# Convert date into ordinal form (proleptic Gregorian ordinal of date)
for i in range(len(x_dates)):
	new_dates.append(x_dates[i].toordinal())


# Linear Regression
slope, intercept, r, p, std_err = stats.linregress(new_dates, y_rankings)
def myfunc(new_dates):
	return slope * new_dates + intercept


mymodel = list(map(myfunc, new_dates))
plt.plot(x_dates, mymodel)


# x-axis ticks (to show months)
locator = mdates.MonthLocator()
fmt = mdates.DateFormatter('%b')
plt.gca().xaxis.set_major_locator(locator)
plt.gca().xaxis.set_major_formatter(fmt)
# Plot
plt.plot(x_dates, y_rankings, marker="x")
plt.xlabel("Date")
plt.ylabel("Ranking")
plt.title(user + " Antichess Ranking History")
plt.show()
