import numpy as np
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import uvicorn

from python_ai_utils.image_utils.image_convert import byte_to_cv2_image, byte_to_ndarray
from python_ai_utils.model_scripts.nsfw_script import predict_simge_image, check_and_download_nsfw_model, \
    process_cv_images
from python_ai_utils.model_scripts.sample_face_detection import is_single_face

app = FastAPI()


@app.post("/ai/audit")
async def upload_image(file: UploadFile = File(...)):
    image_bytes = file.file.read()
    cv_image = byte_to_cv2_image(image_bytes)
    image_batch = process_cv_images([cv_image])
    nsfw_info = predict_simge_image(image_batch)
    is_single = is_single_face(cv_image)
    return JSONResponse(content={"nsfw_info": nsfw_info, "is_single_face": is_single})


if __name__ == "__main__":
    check_and_download_nsfw_model()
    uvicorn.run(app, host="0.0.0.0", port=8000)
