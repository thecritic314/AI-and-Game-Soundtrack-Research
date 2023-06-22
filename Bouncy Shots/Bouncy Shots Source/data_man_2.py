import numpy as np
import matplotlib.pyplot as plt  # To visualize
import pandas as pd  # To read data
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error
from sklearn.metrics import log_loss
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import array

data = pd.read_csv('dataCSV.csv')
inputs = data.iloc[:, [0, 1, 2, 3, 4, 5, 6]]

# print(inputs)

# TODO: NORMALIZE
# normal_data = RobustScaler().fit(data)
# print(normal_data.transform(data))
normal_input_scaled = MinMaxScaler().fit(inputs)
# print(normal_inputs.transform(inputs))
# normal_int = RobustScaler().fit(intensity_data)
# normal_win = RobustScaler().fit(winning_data)




# print(scalerWin.transform(data[['#Balls', '#Bullets', 'Score', 'AvgBtnFreq', 'AvgBallDist', 'RatioBalls', 'AvgBallDir']]))

regInt = RandomForestRegressor()
regInt.fit(inputs, data['Intensity Match'])
#
regWin = RandomForestRegressor()
regWin.fit(inputs, data['Winning Match'])

regInt = LinearRegression()
regInt.fit(normal_input_scaled.transform(inputs), data['Intensity Match'])


regWin = LinearRegression()
regWin.fit(normal_input_scaled.transform(inputs), data['Winning Match'])


X = normal_input_scaled.transform(inputs)
intense = data['Intensity Match']
win = data['Winning Match']

poly = PolynomialFeatures(degree=1, include_bias=False)
poly_features = poly.fit_transform(X)

x1_train, x1_test, int_train, int_test = train_test_split(poly_features, intense, test_size=0.50)
x2_train, x2_test, win_train, win_test = train_test_split(poly_features, win, test_size=0.50)

model1, model2 = RandomForestRegressor(), RandomForestRegressor()
model1.fit(x1_train, int_train)
model2.fit(x2_train, win_train)

y1hat = model1.predict(x1_test)
for idx in range(len(y1hat)):
    if y1hat[idx] > 1:
        y1hat[idx] = 1
    if y1hat[idx] < 0:
        y1hat[idx] = 0
y2hat = model2.predict(x2_test)
for idx in range(len(y2hat)):
    if y2hat[idx] > 1:
        y2hat[idx] = 1
    if y2hat[idx] < 0:
        y2hat[idx] = 0

int_test = int_test.to_numpy()
win_test = win_test.to_numpy()
int_test = np.clip(int_test, 0, 1)
win_test = np.clip(win_test, 0, 1)


rmse1 = mean_squared_error(int_test, y1hat) ** 0.5
rmse2 = mean_squared_error(win_test, y2hat) ** 0.5


#model1, model2 = RandomForestClassifier(), RandomForestClassifier()  # USE CSVROUNDED
#model1.fit(x1_train, int_train)
#model2.fit(x2_train, win_train)

#y1hat = model1.predict(x1_test)
#y2hat = model2.predict(x2_test)

#ll1 = log_loss(int_test, model1.predict_proba(x1_test)[:, 1])
#ll2 = log_loss(win_test, model2.predict_proba(x2_test)[:, 1])
#acc1 = accuracy_score(int_test, y1hat)
#acc2 = accuracy_score(win_test, y2hat)

#plt.scatter(data['#Balls'], data['Intensity Match'])
#plt.show()


#print(rmse1, rmse2)

#print(model1.intercept_)
