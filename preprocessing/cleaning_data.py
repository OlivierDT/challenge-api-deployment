import json
import pandas as pd

with open(
    "./input.json",
    "r",
) as file:
    data = json.load(file)
    data = data["data"]
    print(data)
    print(type(data))


def preprocess(data):

    state_of_building = data["building_state"]
    bedrooms = data["rooms_number"]
    area = data["area"]
    swimming_pool = data["swimming_pool"]
    list1 = [state_of_building, bedrooms, area, swimming_pool]
    df = pd.DataFrame(list1)

    df = df.replace("HOUSE", 1)
    df = df.replace("APARTMENT", 0)
    df = df.replace("TO_RESTORE", 1)
    df = df.replace("TO REBUILD", 2)
    df = df.replace("TO_RENOVATE", 3)
    df = df.replace("JUST_RENOVATED", 4)
    df = df.replace("GOOD", 5)
    df = df.replace("NEW", 6)
    df = df.replace(True, 1)
    df = df.replace(False, 0)
    print(df, "in preprocess")

    df_no_Nan = df.dropna(axis=0, how="any")

    X_predict = [list(df_no_Nan.loc[:, 0])]

    print(X_predict)
    print(type(X_predict))
    preprocessed_data = X_predict
    return preprocessed_data


