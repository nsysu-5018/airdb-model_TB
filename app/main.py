from fastapi import FastAPI
from pydantic import BaseModel
import TB


class InputData(BaseModel):
    sex: int
    age: int
    address: str
    id: str
    date: str
    dis_list: list[bool]
    air_data: dict[str, float]


app = FastAPI()
model = TB.model()


@app.post("/predict")
def predict(data: InputData):
    result = model.predict(data)
    output = round(float(result), 3)
    return output

