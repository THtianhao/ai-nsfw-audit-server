from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import uvicorn

from inspireface.sample_face_detection import case_face_detection_image
from python_ai_utils.image_utils.image_convert import file_to_ndarray, file_to_cv2_image
from python_ai_utils.model_scripts.nsfw_script import predict_simge_image

app = FastAPI()


@app.post("/ai/audit")
async def upload_image(file: UploadFile = File(...)):
    image_array = file_to_ndarray(file)
    cv_image = file_to_cv2_image(file)
    result = predict_simge_image(image_array)
    fd_result = case_face_detection_image(cv_image)
    return JSONResponse(content={"file_info": result})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
