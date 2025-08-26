from fastapi import FastAPI
from pydantic import BaseModel
from src.pipeline.predict_pipeline import CustomData, PredictPipeline
import uvicorn

app = FastAPI()


# Input schema
class InputData(BaseModel):
    gender: str
    race_ethnicity: str
    parental_level_of_education: str
    lunch: str
    test_preparation_course: str
    reading_score: float
    writing_score: float


@app.get("/")
def home():
    return {
        "message": "Go to run the Streamlit app for predictions",
        "url": "http://localhost:8501",
    }


@app.post("/predict")
def predict(data: InputData):
    custom_data = CustomData(
        gender=data.gender,
        race_ethnicity=data.race_ethnicity,
        parental_level_of_education=data.parental_level_of_education,
        lunch=data.lunch,
        test_preparation_course=data.test_preparation_course,
        reading_score=data.reading_score,
        writing_score=data.writing_score,
    )

    pred_df = custom_data.get_data_as_data_frame()

    predict_pipeline = PredictPipeline()
    result = predict_pipeline.predict(pred_df)

    return {"prediction": float(result[0])}


if __name__ == "__main__":
    # This will run the server when you do: python main.py
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
