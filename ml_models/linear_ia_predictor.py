from common.Distributions import *
from sklearn.model_selection import train_test_split
from sklearn import linear_model
import pandas as pd
import pickle

#create data
num_samples_per_mean_ia = 1000
num_ia_per_sample = 50
mean_ias = [45.45, 50, 66.66, 100]

# create data
inputs = []
labels = []
for mean_ia in mean_ias:
    arrival_time_distribution = Exponential(mean_ia)
    for sample_idx in range(num_samples_per_mean_ia):
        inputs.append(arrival_time_distribution.create(num_ia_per_sample))
        labels.append(mean_ia)

# convert data to pandas dataframe
inputs = pd.DataFrame(inputs)
labels = pd.DataFrame(labels)

# split training data into train and test
X_train, X_test, y_train, y_test = train_test_split(inputs, labels, test_size=0.2, random_state=0)

# create model
model = linear_model.LinearRegression()

# fit the model
model.fit(X_train, y_train)

# print first few predictions on
preds = model.predict(X_train[:3])
print(preds)

# R2 score on training data
print('R2 score on training data: ' + str(model.score(X_train, y_train)))

# R2 score on test data
print('R2 score on test data: ' + str(model.score(X_test, y_test)))

# save model for further use
with open('compressed_models/linear_ia_predictor.pkl', 'wb') as f:
    pickle.dump(model, f)




