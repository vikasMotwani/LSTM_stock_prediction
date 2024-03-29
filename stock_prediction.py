# -*- coding: utf-8 -*-
"""NeuralNetworks1

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1EYklOgOJvODyvkBAzqK8STr7F_o_ZzMz
"""

#LSTM for Tesla stock prediction
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.preprocessing import MinMaxScaler

stock_df = pd.read_csv('TSLA.csv')
stock = stock_df['Close'].values.reshape(-1, 1)
dates = pd.to_datetime(stock_df['Date'])
stock.shape
stock_df.head()

sc = MinMaxScaler(feature_range=(0,1))
stock = sc.fit_transform(stock)

#selecting length for LSTM
sequence_length = 10
X, y = [], []

for i in range(len(stock) - sequence_length):
  X.append(stock[i: i+sequence_length, 0])
  y.append(stock[i+sequence_length, 0])

X, y = np.array(X), np.array(y)

X = np.reshape(X, (X.shape[0], X.shape[1], 1))

X_train, X_test, y_train, y_test, dates_train, dates_test = train_test_split(X, y, dates[sequence_length:], test_size = 0.2)

model = Sequential()
model.add(LSTM(units = 20, return_sequences=True, input_shape = (X.shape[1], 1)))
model.add(LSTM(units = 20, return_sequences = False))
model.add(Dense(units = 1))

model.compile(optimizer = 'adam', loss = 'mean_squared_error')
model.fit(X_train, y_train, epochs = 2, batch_size = 50)

loss = model.evaluate(X_test, y_test)
print("loss = ",  loss)

y_predict = model.predict(X_test)
y_predict_inverse = sc.inverse_transform(y_predict)
y_test_inverse = sc.inverse_transform(y_test.reshape(-1, 1))

plt.figure(figsize=(10, 5))
plt.plot(y_predict_inverse[::3], color = "red",  label = "Predictions")
plt.plot(y_test[::3], color= "blue", label = "Actual")
plt.title('LSTM Stock Prediction')
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend()
plt.show()

train_loss = model.evaluate(X_train, y_train)
print("Train loss = ",  train_loss)

y_train_predict = model.predict(X_train)
y_train = sc.inverse_transform(y_train.reshape(-1, 1))
y_train_predict = sc.inverse_transform(y_train_predict)

plt.figure(figsize=(10, 5))
plt.plot(y_train[::10], color = "yellow", label = "train")
plt.plot(y_train_predict[::10], color = "green", label = "train predict")
plt.title('LSTM Stock Prediction')
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend()
plt.show()

