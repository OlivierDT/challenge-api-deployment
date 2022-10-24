from array import array
import pickle

pkl_filename = "./model/saved_model.pkl"

with open(pkl_filename, "rb") as file:
    model = pickle.load(file)


def predict(preprocessed_data: array):

    y_predict = model.predict(preprocessed_data)
    print(y_predict)
    print(type(y_predict))
    y_predict = y_predict[0][0]
    print(y_predict)
    print(type(y_predict))
    return y_predict
