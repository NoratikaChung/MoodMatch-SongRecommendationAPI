from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from io import BytesIO
from moodmatch_core import run_moodmatch
import uvicorn

app = FastAPI()

# CORS so React Native can call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/recommend")
async def recommend(
    file: UploadFile = File(...),
    language: str = Form(None),
    mood: str = Form(None)
):
    image = Image.open(BytesIO(await file.read())).convert("RGB")
    result = run_moodmatch(image, language, mood)
    return result

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=7860)
