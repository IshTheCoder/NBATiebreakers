from load_data import load_data
from keras.models import Sequential, Model
from keras.layers import Input, Dense, Dropout
import numpy as np

players17 = load_data("player2016-2017.csv");
players16 = load_data("player2015-2016.csv");
players15 = load_data("player2014-2015.csv");
players14 = load_data("player2013-2014.csv");
players13 = load_data("player2012-2013.csv");
players = players17 + players16 + players15 + players14 + players13;
data = np.array(players);
lebron = np.array([76,76,35.6,9.7,18.6,.520,1.1,3.7,.309,8.6,14.9,.573,.551,4.7,6.5,.731,1.5,6.0,7.4,6.8,1.4,0.6,3.3,1.9,25.3]);
for i in range(len(data[0])):
    ma = np.max(data[:,i]);
    data[:,i] /= ma;
    lebron[i] /= ma;

print(np.shape(data));
batch_size = 50
# epochs = 20
epochs = 50


input_img = Input(shape=(25,))
# "encoded" is the encoded representation of the input
encoded = Dense(3, activation='sigmoid')(Dense(100, activation='relu')(input_img))
# "decoded" is the lossy reconstruction of the input
decoded = Dense(25, activation='sigmoid')(Dense(100, activation='relu')(encoded))

# this model maps an input to its reconstruction
model = Model(input=input_img, output=decoded)
encoder = Model(input=input_img, output=encoded)

model.summary();

model.compile(optimizer='adam', loss='mean_squared_error');

story = model.fit(data, data,
                  batch_size=batch_size, epochs=epochs,
                  verbose=1, validation_data=(data, data))

np.save("compress",encoder.predict(data));

lebron = np.reshape(lebron, (1,25));
small_lebron = encoder.predict(lebron);
print(small_lebron);
#for i in range(len(test1)):
#    print(test1[i], test2[i]);

