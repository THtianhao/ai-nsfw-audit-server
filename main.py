from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import uvicorn

from python_ai_utils.image_utils.image_convert import file_to_ndarray, file_to_cv2_image
from python_ai_utils.model_scripts.nsfw_script import predict_simge_image, check_and_download_nsfw_model
from python_ai_utils.model_scripts.sample_face_detection import is_single_face

app = FastAPI()


@app.post("/ai/audit")
async def upload_image(file: UploadFile = File(...)):
    image_array = file_to_ndarray(file)
    cv_image = file_to_cv2_image(file)
    nsfw_info = predict_simge_image(image_array)
    is_single = is_single_face(cv_image)
    return JSONResponse(content={"nsfw_info": nsfw_info, "is_single_face": is_single})


if __name__ == "__main__":
    check_and_download_nsfw_model()
    uvicorn.run(app, host="0.0.0.0", port=8000)
