from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.models import Sequential
import lstm
import time  # helper libraries
import matplotlib.pyplot as plt
import math


def build_model(layers):
    d = 0.2
    model = Sequential()
    model.add(LSTM(50, input_shape=(layers[1], layers[0]), return_sequences=True))
    model.add(Dropout(d))
    model.add(LSTM(50, input_shape=(layers[1], layers[0]), return_sequences=False))
    model.add(Dropout(d))
    model.add(Dense(16, init='uniform', activation='tanh'))
    model.add(Dense(1, init='uniform', activation='tanh'))
    model.compile(loss='mse', optimizer='adam', metrics=['accuracy'])
    return model


X_train, y_train, X_test, y_test = lstm.load_data('spy', 50, True)
print("X_train", X_train.shape)
print("y_train", y_train.shape)
print("X_test", X_test.shape)
print("y_test", y_test.shape)

model = build_model([6, 50])

model.fit(
    X_train,
    y_train,
    batch_size=512,
    nb_epoch=40,
    validation_split=0.1)

trainScore = model.evaluate(X_train, y_train, verbose=0)
print('Train Score: %.2f MSE (%.2f RMSE)' % (trainScore[0], math.sqrt(trainScore[0])))

testScore = model.evaluate(X_test, y_test, verbose=0)
print('Test Score: %.2f MSE (%.2f RMSE)' % (testScore[0], math.sqrt(testScore[0])))

p = model.predict(X_test)

x1 = []
x2 = []

for i in range(len(p) - 1):
    if len(x1) == 0:
        x1.append(0)
    else:
        x1.append(x1[-1] + ((p[i] - p[i - 1]) / p[i - 1]) * 100)

for i in range(len(p) - 1):
    if len(x2) == 0:
        x2.append(0)
    else:
        x2.append(x2[-1] + ((y_test[i] - y_test[i - 1]) / y_test[i - 1]) * 100)

plt.plot(x1, color='red', label='prediction')
plt.legend(loc='upper left')
plt.show()

p = model.predict(lstm.get_prediction_data('spy', 50, 100))
plt.plot(p, color='red', label='prediction')
plt.legend(loc='upper left')
plt.show()
