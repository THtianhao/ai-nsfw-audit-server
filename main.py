from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI()

@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    # 获取图片的文件名和内容类型
    file_info = {
        "filename": file.filename,
        "content_type": file.content_type,
        "file_size": len(await file.read())  # 计算图片的字节大小
    }

    # 返回包含文件信息的 JSON 响应
    return JSONResponse(content={"file_info": file_info})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
