import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from enum import Enum
from typing import Optional
from preprocessing.cleaning_data import preprocess
from predict.prediction import predict

app = FastAPI(title="Property Price Prediction")

class PropertyType(str, Enum):
    APARTMENT = "APARTMENT"
    HOUSE = "HOUSE"
    OTHERS = "OTHERS"

class BuildingState(str, Enum):
    NEW = "NEW"
    GOOD = "GOOD"
    TO_RENOVATE = "TO RENOVATE"
    JUST_RENOVATED = "JUST RENOVATED"
    TO_REBUILD = "TO REBUILD"

# request body: area, property_type, rooms_number, zip_code are mandatory
class Property(BaseModel):
    area: int
    property_type: PropertyType
    rooms_number: int
    zip_code: int
    land_area: Optional[int] | None = None
    garden: Optional[bool] | None = None
    garden_area: Optional[int] | None = None
    equipped_kitchen: Optional[bool] | None = None
    full_address: Optional[str] | None = None
    swimming_pool: Optional[bool] | None = None
    furnished: Optional[bool] | None = None
    open_fire: Optional[bool] | None = None
    terrace: Optional[bool] | None = None
    terrace_area: Optional[int] | None = None
    facades_number: Optional[int] | None = None
    building_state: Optional[BuildingState] | None = None

@app.get("/")
async def root():
    return {"Server status": "alive"}

@app.post("/predict")
async def make_prediction(property: Property):
    try:
        print(property)
        print(type(property), "CHECK")
        property = property.dict()
        property = preprocess(property)  # preprocess() is defined in cleaning_data.py
        print(property)
        price_prediction = predict(property)  # predict() is defined in prediction.py
        return price_prediction
    except:
        return {'warning': 'Please check your inputs.'}

@app.get("/predict")
async def expected_inputs():
    message = 'Mandatory fields are the following: area, property_type, rooms_number and zip_code. For property_type, please use either "APARTMENT", "HOUSE" or "OTHERS". Other fields are optional. For building_state, please use either "NEW", "GOOD", "TO RENOVATE", "JUST RENOVATED" or "TO REBUILD". For garden, equipped_kitchen, swimming_pool, furnished, open_fire and terrace, please indicate 0 or 1. All the other fields take numerical values, except for the full_adress.'
    return {"message": message}


@app.get("/predict/format")
async def expected_inputs_format():
    return {
        """
{"data":
   {"area": int,
    "property_type": "APARTMENT" | "HOUSE" | "OTHERS",
    "rooms_number": int,
    "zip_code": int,
    "land_area": Optional[int],
    "garden": Optional[bool],
    "garden_area": Optional[int],
    "equipped_kitchen": Optional[bool],
    "full_address": Optional[str],
    "swimming_pool": Optional[bool],
    "furnished": Optional[bool],
    "open_fire": Optional[bool],
    "terrace": Optional[bool],
    "terrace_area": Optional[int],
    "facades_number": Optional[int],
    "building_state": Optional["NEW" | "GOOD" | "TO RENOVATE" | "JUST RENOVATED" | "TO REBUILD"]
    }
}
"""
    }


if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)


"""
{"data":
   {"area": int,
    "property_type": "APARTMENT" | "HOUSE" | "OTHERS",
    "rooms_number": int,
    "zip_code": int,
    "land_area": Optional[int],
    "garden": Optional[bool],
    "garden_area": Optional[int],
    "equipped_kitchen": Optional[bool],
    "full_address": Optional[str],
    "swimming_pool": Optional[bool],
    "furnished": Optional[bool],
    "open_fire": Optional[bool],
    "terrace": Optional[bool],
    "terrace_area": Optional[int],
    "facades_number": Optional[int],
    "building_state": Optional["NEW" | "GOOD" | "TO RENOVATE" | "JUST RENOVATED" | "TO REBUILD"]
    }
}
"""
