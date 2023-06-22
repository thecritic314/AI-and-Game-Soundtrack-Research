import numpy as np
import matplotlib.pyplot as plt  # To visualize
import pandas as pd  # To read data
import sklearn.metrics
from sklearn.linear_model import LinearRegression

data = pd.read_csv('dataCSV.csv')
print(data)
ax = plt.axes(projection="3d")

X = data[['#Bullets']].astype(float)  # values converts it into a numpy array
Y = data['#Balls'].astype(float)  # -1 means that calculate the dimension of rows, but have 1 column
Z = data['Intensity Match'].astype(float)
linear_regressor = LinearRegression()  # create object for the class
linear_regressor.fit(X, Y)  # perform linear regression
Z_pred = linear_regressor.predict(X)  # make predictions
# print('r_squared:', sklearn.metrics.r2_score(Y, Y_pred))

# plt.scatter(X, Z)
# plt.plot(X, Z_pred, color='red')
# plt.show()

ax.scatter(X, Y, Z)
plt.show()


# regInt = LinearRegression()
# regInt.fit(data[['#Balls', '#Bullets', 'Score', 'AvgBtnFreq', 'AvgBallDist', 'RatioBalls', 'AvgBallDir']], data['Intensity Match'])
#
# regWin = LinearRegression()
# regWin.fit(data[['#Balls', '#Bullets', 'Score', 'AvgBtnFreq', 'AvgBallDist', 'RatioBalls', 'AvgBallDir']], data['Winning Match'])

# print(regInt.predict([[1, 5, 5, 25, 40, 0.5, 0.5]])[0])
# print(regWin.predict([[1, 5, 5, 25, 40, 0.5, 0.5]])[0])