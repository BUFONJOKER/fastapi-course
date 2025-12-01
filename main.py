# import necessary libraries
import json
from fastapi import FastAPI, Path, Query, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional

# create FastAPI app
app = FastAPI()

# create Patient model using Pydantic BaseModel
class Patient(BaseModel):
    # define patient model fields
    id: Annotated[str,Field(...,description="Id of patient")]

    name: Annotated[str,Field(...,description="Name of patient")]

    city: Annotated[str,Field(...,description="City of patient")]

    age: Annotated[int,Field(...,gt=0,lt=101,description="Age of patient should be between 1 to 100")]

    gender: Annotated[Literal['male','female'],Field(...,description="Gender of patient")]

    height: Annotated[float,Field(...,gt=0,description="Height of patient in meters")]

    weight: Annotated[float,Field(...,gt=0,description="Weight of patient in kilograms")]

    # created bmi field
    @computed_field
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi

    # created verdict field based on bmi
    @computed_field
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif 18.5 <= self.bmi < 25:
            return "Normal"
        elif 25 <= self.bmi < 30:
            return "Overweight"
        else:
            return "Obesity"


class PatientUpdate(BaseModel):
    # define update patient model fields
   

    name: Annotated[Optional[str],Field(default=None)]

    city: Annotated[Optional[str],Field(default=None)]

    age: Annotated[Optional[int],Field(default=None,gt=0,lt=101,description="Age of patient should be between 1 to 100")]
    gender: Annotated[Optional[Literal['male','female']],Field(default=None,description="Gender of patient")]

    height: Annotated[Optional[float],Field(default=None,gt=0)]

    weight: Annotated[Optional[float],Field(default=None,gt=0)]


# function to load data from json file
def load_data():
    with open("patients.json",'r') as f:
        data = json.load(f)
    
    return data

# function to save data to json file
def save_data(data):
    with open("patients.json",'w') as f:
        json.dump(data, f)

# create home api
@app.get("/")
def hello():

    return {
        "message":"Hello World"
    }

# create about api
@app.get("/about")
def about():
    
    return {
        "about":"Welcome Mani in FastApi"
    }

# create get api to view all patients
@app.get("/view")
def view():
    # load data
    data = load_data()

    return data

# create get api to view patient by id
@app.get("/patient/{id}")
def view_patient(id: str=Path(
    ...,description="Patient id",
    examples="P001"  
)):

    # load data
    data = load_data()

    # check if patient exists
    if id in data:
        return data[id]
    # if patient not found raise 404 error
    else:
        raise HTTPException(
            status_code=404,
            detail="Patient Not Found"
        )

# create get api to sort patients by height, weight or bmi
@app.get('/sort')
def sort_patients(
    sort_by:str = Query(
        ..., description="sort by ['height','weight','bmi']"
    ),
    order_by:str=Query(
        'asc', description="order by asc or desc"
    )
):
    # check if sort_by is valid
    if sort_by not in ['height','weight','bmi']:
        raise HTTPException(status_code=400,detail="invalid sort by")

    # check if order_by is valid
    if order_by not in ['asc','desc']:
        raise HTTPException(status_code=400,detail="invalid sorting order")

    # determine sort order
    sort_order = True if order_by=="desc" else False

    # load data
    data = load_data()
    
    # sort patients
    sort_patients = sorted(
        data.values(), key=lambda x : x.get(sort_by), reverse=sort_order
    )

    return sort_patients

# create post api to create patient data
@app.post("/create")
def create_patient(patient:Patient):
    # load existing data from json file
    data = load_data()

    if patient.id not in data:
        # add patient to data
        data[patient.id] = patient.model_dump(exclude=['id'])
        # save data to json file
        save_data(data)

        return JSONResponse(status_code=201, content={'message':'patient data created successfully'})
    
    else:
        raise HTTPException(status_code=400, detail="Patient already exists")

# create put api to update patient data
@app.put("/update/{id}")
def update_patient(id: str,patient_update:PatientUpdate):
    # load existing data from json file
    data = load_data()

    # check if patient exists
    if id not in data:
        raise HTTPException(status_code=404, detail='patient not found')

    # get existing patient data
    existing_data = data[id]

    # get update data and change to dict and exclude unset fields
    patient_update_data = patient_update.model_dump(exclude_unset=True)

    # update existing data with new data
    for key, val in patient_update_data.items():
        existing_data[key] = val

    # adding id back to existing data
    existing_data['id'] = id

    # create Patient object to recalculate bmi and verdict
    existing_data_object = Patient(**existing_data)

    # convert back to dict and exclude id
    existing_data = existing_data_object.model_dump(exclude={'id'})

    # update data
    data[id] = existing_data

    # save data to json file
    save_data(data)

    return JSONResponse(status_code=200, content={'message':'patient data updated successfully'})

# create delete api to delete patient data
@app.delete("/delete/{id}")
def delete_patient(id:str):

    # load existing data from json file
    data = load_data()

    # check if patient exists
    if id not in data:
        raise HTTPException(status_code=404, detail="patient not found")

    # delete patient data
    del data[id]

    # save data to json file
    save_data(data)

    return JSONResponse(status_code=200, content={'message':'patient deleted successfully'})
