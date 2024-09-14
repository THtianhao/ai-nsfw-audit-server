import cv2
import numpy as np
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import uvicorn

from python_ai_utils.image_utils.image_convert import byte_to_cv2_image, byte_to_ndarray, byte_to_pil_image
from python_ai_utils.model_scripts.nsfw_script import predict_simge_image, check_and_download_nsfw_model, \
    process_cv_images
from python_ai_utils.model_scripts.sample_face_detection import is_single_face
from python_ai_utils.utils.fastapi_exception import error_in_file
from python_ai_utils.utils.log_util import log_util

app = FastAPI()
error_in_file(app, log_util, "https://open.feishu.cn/open-apis/bot/v2/hook/f584024c-7c12-44d2-9407-e187fbc4387e")


@app.post("/ai/audit")
async def upload_image(file: UploadFile = File(...)):
    image_bytes = file.file.read()
    cv_image = byte_to_cv2_image(image_bytes)
    cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
    image_batch = process_cv_images([cv_image])
    nsfw_info = predict_simge_image(image_batch)
    is_single = is_single_face(cv_image)
    return JSONResponse(content={"nsfw_info": nsfw_info, "is_single_face": is_single})


if __name__ == "__main__":
    check_and_download_nsfw_model()
    uvicorn.run(app, host="0.0.0.0", port=8000)
