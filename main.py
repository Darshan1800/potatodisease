
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf


app = FastAPI()

def read_file_as_image(data) -> np.ndarray:
    image = np.array(Image.open(BytesIO(data)).resize((256,256)))
    return image

@app.get('/')  # basic get view
def basic_view():
    return {"WELCOME": "GO TO /docs route, or /post or send post request to /predict "}

MODEL = tf.keras.models.load_model("potatoes.h5")



CLASS_NAMES = ["Early Blight", "Late Blight", "Healthy"]



@app.post("/predict")
async def predict(
    file: UploadFile = File(...)
):
    image = read_file_as_image(await file.read())
    img_batch = np.expand_dims(image, 0)

    predictions = MODEL.predict(img_batch)

    predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
    confidence = np.max(predictions[0])
    return {
        'class': predicted_class,
        'confidence': float(confidence)
    }

if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=8000)
