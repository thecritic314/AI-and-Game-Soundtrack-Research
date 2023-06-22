# imports
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, PolynomialFeatures
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Merge sample_input.csv and sample_output.csv
# lag = 0
# while lag <= 2500:
lag = 250
data = pd.DataFrame()
for x in range(1, 27):
    sheet1 = "chaos"  # TODO: change
    sheet2 = "chaos_ui"
    sheet1 = sheet1 + str(x) + ".csv"
    sheet2 = sheet2 + str(x) + ".csv"
    # Load csv files
    df1 = pd.read_csv(sheet1)  # TODO: change
    if (x == 14):
        df2 = pd.read_csv(sheet2)
    else:
        df2 = pd.read_csv(sheet2, sep='\t')
    # df1 = pd.read_excel('data.xlsx', sheet_name = 'play (1)')
    # df2 = pd.read_excel('data.xlsx', sheet_name = 'user_input_3 (1)')
    # print(df1)
    # print(df2)
    # print(df1.iat[1,0])
    rows_count = df1.shape[0]
    # print(rows_count)
    for i in range(rows_count):
        # for j in range(0, 3000, 500):
        df1.iat[i, 0] += lag
    # df2.to_excel(r'C:\Users\Admin\Desktop\Test.xlsx', index = False)

    # Merge two files
    input_columns_list = ['Timestamp', 'Score', 'Lives', 'Chaos', 'Level', 'Enemies', 'Bullets', 'AvgBtnFreq',
                          'GoalDist', 'StartDist', 'TimeElapsed', 'AtTower']  # TODO: change
    output_columns_list = ['Timestamp(ms)', 'Intensity', 'Winning Status']

    # print(df1.columns)
    input_column_data = df1[input_columns_list].values
    output_column_data = df2[output_columns_list].values
    size1 = df1.shape[0]
    size2 = df2.shape[0]
    merge_columns = ['Timestamp(ms)', 'Score', 'Lives', 'Chaos', 'Level', 'Enemies', 'Bullets', 'AvgBtnFreq',
                     'GoalDist', 'StartDist', 'TimeElapsed', 'AtTower', 'Intensity', 'Winning Status']  # TODO: change
    df_merge = pd.DataFrame(columns=merge_columns)
    # Create initial merge state by merging first row of each
    ts1 = df1['Timestamp'][0]
    ts2 = df2['Timestamp(ms)'][0]
    min_ts = min(ts1, ts2)
    new_row_data = [min_ts]
    new_row_data.extend(input_column_data[0, 1:])
    new_row_data.extend(output_column_data[0, 1:])
    df_merge.loc[len(df_merge.index)] = new_row_data
    # df_merge.append(new_row_data)

    i1 = 1
    i2 = 1
    while i1 < size1 or i2 < size2:
        ts1 = df1['Timestamp'][min(i1, size1 - 1)]
        ts2 = df2['Timestamp(ms)'][min(i2, size2 - 1)]
        min_ts = min(ts1, ts2)
        if i2 == size2 or (ts1 < ts2 and i1 < size1):  # merge from df1
            new_row_data = [ts1]
            new_row_data.extend(input_column_data[min(i1, size1 - 1), 1:])
            new_row_data.extend(output_column_data[i2 - 1, 1:])
            i1 += 1
        elif i1 == size1 or (ts2 < ts1 and i2 < size2):  # merge from df2
            new_row_data = [ts2]
            new_row_data.extend(input_column_data[i1 - 1, 1:])
            new_row_data.extend(output_column_data[min(i2, size2 - 1), 1:])
            i2 += 1
        else:  # merge both (same timestamp)
            new_row_data = [ts1]
            new_row_data.extend(input_column_data[i1, 1:])
            new_row_data.extend(output_column_data[i2, 1:])
            i1 += 1
            i2 += 1
        df_merge.loc[len(df_merge.index)] = new_row_data
    data = pd.concat([data, df_merge])
    # print(df_merge)
    # print(df_merge.loc[0])
    # df_merge.to_excel(r'C:\Users\Admin\Desktop\Test.xlsx', index = False)
# print(data)
# data.to_excel(r'C:\\Users\\aaron\\PycharmProjects\\XSIG\\CSVs\\BSDataLag' + str(lag) + '.xslx', index=False)
inputs = data.iloc[:, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]]  # TODO: change
normal_input_scaled = MinMaxScaler().fit(inputs)
normal = normal_input_scaled.transform(inputs)
intense = data.iloc[:, [12]]  # TODO: change
win = data.iloc[:, [13]]  # TODO: change
poly = PolynomialFeatures(degree=1, include_bias=False)
poly_features = poly.fit_transform(normal)

x1_train, x1_test, int_train, int_test = train_test_split(poly_features, intense, test_size=0.50)
x2_train, x2_test, win_train, win_test = train_test_split(poly_features, win, test_size=0.50)

model1, model2 = RandomForestRegressor(), RandomForestRegressor()
model1.fit(x1_train, np.ravel(int_train))
model2.fit(x2_train, np.ravel(win_train))

y1hat = model1.predict(x1_test)
y1hat = np.clip(y1hat, 0, 1)
y2hat = model2.predict(x2_test)
y2hat = np.clip(y2hat, 0, 1)

int_test = int_test.to_numpy()
win_test = win_test.to_numpy()
int_test = np.clip(int_test, 0, 1)
win_test = np.clip(win_test, 0, 1)

rmse1 = mean_squared_error(int_test, y1hat) ** 0.5
rmse2 = mean_squared_error(win_test, y2hat) ** 0.5

# print('Lag ' + str(lag) + ': ' + str(rmse1) + ', ' + str(rmse2))

# lag = lag + 250
