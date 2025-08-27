from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from src.pipeline.predict_pipeline import CustomData, PredictPipeline
import uvicorn

# Initialize FastAPI
app = FastAPI()

# Mount static (for CSS/JS) and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# -------------------------------
# Root route -> Render index.html
# -------------------------------
@app.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# -------------------------------
# Predict from HTML form
# -------------------------------
@app.post("/predict", response_class=HTMLResponse)
async def predict_datapoint(
    request: Request,
    gender: str = Form(...),
    race_ethnicity: str = Form(...),
    parental_level_of_education: str = Form(...),
    lunch: str = Form(...),
    test_preparation_course: str = Form(...),
    reading_score: int = Form(...),
    writing_score: int = Form(...),
):
    # Create input data object
    data = CustomData(
        gender=gender,
        race_ethnicity=race_ethnicity,
        parental_level_of_education=parental_level_of_education,
        lunch=lunch,
        test_preparation_course=test_preparation_course,
        reading_score=reading_score,
        writing_score=writing_score,
    )

    pred_df = data.get_data_as_data_frame()
    predict_pipeline = PredictPipeline()
    pred = predict_pipeline.predict(pred_df)
    results = round(pred[0], 2)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "results": results,
        },
    )


# -------------------------------
# Predict from JSON API
# -------------------------------
class InputData(BaseModel):
    gender: str
    race_ethnicity: str
    parental_level_of_education: str
    lunch: str
    test_preparation_course: str
    reading_score: int
    writing_score: int


@app.post("/predictAPI")
async def predict_api(data: InputData):
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
    pred = predict_pipeline.predict(pred_df)

    return JSONResponse({"maths_score": round(pred[0], 2)})


# -------------------------------
# Run with uvicorn
# -------------------------------
if __name__ == "__main__":
    uvicorn.run("application:app", host="0.0.0.0", port=8000, reload=True)
