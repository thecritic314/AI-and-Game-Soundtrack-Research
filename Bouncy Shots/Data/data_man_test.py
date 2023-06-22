import numpy as np
import matplotlib.pyplot as plt  # To visualize
import pandas as pd  # To read data
from sklearn import preprocessing
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import log_loss
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_squared_error

csv = pd.read_csv('dataCSVRounded.csv')
scaler = preprocessing.MinMaxScaler()
names = csv.columns
d = scaler.fit_transform(csv)
data = pd.DataFrame(d, columns=names)

print(data)

#X = data[['#Balls']].astype(float)  # values converts it into a numpy array
#Y = data['Intensity Match'].astype(float)  # -1 means that calculate the dimension of rows, but have 1 column
#linear_regressor = LinearRegression()  # create object for the class
#linear_regressor.fit(X, Y)  # perform linear regression
#Y_pred = linear_regressor.predict(X)  # make predictions
#
#plt.scatter(X, Y)
#plt.plot(X, Y_pred, color='red')
#plt.show()


regInt = LogisticRegression()
regInt.fit(data[['#Balls', '#Bullets', 'Score', 'AvgBtnFreq', 'AvgBallDist', 'RatioBalls', 'AvgBallDir']], data['Intensity Match'])


regWin = LogisticRegression()
regWin.fit(data[['#Balls', '#Bullets', 'Score', 'AvgBtnFreq', 'AvgBallDist', 'RatioBalls', 'AvgBallDir']], data['Winning Match'])

#SSDi = 0 #sum of squared differences
#SSDw = 0
#for i in range(len(data.index)):
#    pred_int = regInt.predict(data.iloc[[i], 0:7])
#    pred_win = regWin.predict(data.iloc[[i], 0:7])
#    true_int = data.iloc[[i], 7]
#    true_win = data.iloc[[i], 8]
#    x = pred_int - true_int
#    xList = x.tolist()
#    SSDi += xList[0] ** 2
#    y = pred_win - true_win
#    yList = y.tolist()
#    SSDw += yList[0] ** 2

vals = data.values
X = vals[:, :-2]
intense = vals[:, 7:8]
win = vals[:, 8:]
x1_train, x1_test, int_train, int_test = train_test_split(X, np.ravel(intense), test_size=0.50)
x2_train, x2_test, win_train, win_test = train_test_split(X, np.ravel(win), test_size=0.50)

model1, model2 = LogisticRegression(), LogisticRegression()
model1.fit(x1_train, int_train)
model2.fit(x2_train, win_train)

y1hat = model1.predict(x1_train)
#with np.nditer(y1hat, op_flags=['readwrite']) as y1:
#    for x in y1:
#        x[...] = np.round(x)
y2hat = model2.predict(x2_train)
#with np.nditer(y2hat, op_flags=['readwrite']) as y2:
#    for x in y2:
#        x[...] = np.round(x)


ll1 = log_loss(int_test, y1hat)
ll2 = log_loss(win_test, y2hat)
acc1 = mean_squared_error(int_test, y1hat) ** 0.5
acc2 = mean_squared_error(win_test, y2hat) ** 0.5
print('Intensity: %.3f' % ll1)
print('Winning: %.3f' % ll2)

#print(SSDi ** 0.5)
#print(SSDw ** 0.5)

# print(regInt.predict([[1, 5, 5, 25, 40, 0.5, 0.5]])[0])
# print(regWin.predict([[1, 5, 5, 25, 40, 0.5, 0.5]])[0])


count1b, count1i, count2b, count2i, count3b, count3i, count4b, count4i = 0, 0, 0, 0, 0, 0, 0, 0
for i in range(len(data['#Balls'])):
    ballArray = np.ravel(data['#Balls'])
    scoreArray = np.ravel(data['Intensity Match'])
    if scoreArray[i] == 0:
        if ballArray[i] == 1:
            count1b += 1
        elif ballArray[i] == 2:
            count2b += 1
        elif ballArray[i] == 3:
            count3b += 1
        elif ballArray[i] == 4:
            count4b += 1
    else:
        if ballArray[i] == 1:
            count1i += 1
        elif ballArray[i] == 2:
            count2i += 1
        if ballArray[i] == 3:
            count3i += 1
        if ballArray[i] == 4:
            count4i += 1
print(count1b, count1i, count2b, count2i, count3b, count3i, count4b, count4i)