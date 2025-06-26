from typing import Annotated
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import zipfile
from pytubefix import YouTube
from models.urlmodels import Item
import uvicorn
from utils.fila_low_level import Queue
import tempfile
import os
import shutil

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["POST"],
)


@app.post("/videos")
async def post_vid(urls: Item, background_tasks: BackgroundTasks):

    queue = Queue()
    base_temp_dir = os.path.join(os.path.dirname(__file__), "temp")
    os.makedirs(base_temp_dir, exist_ok=True)
    temp_dir = tempfile.mkdtemp(dir=base_temp_dir)
    downloaded_files = []

    for url in urls.urls_vid:
        queue.push(url)

    for link in queue:
        ytb = YouTube(link)
        vid = ytb.streams.get_highest_resolution()
        file_path = vid.download(output_path=temp_dir)
        downloaded_files.append(file_path)

    background_tasks.add_task(shutil.rmtree, temp_dir)

    if len(downloaded_files) == 1:
        return FileResponse(
            downloaded_files[0],
            media_type="video/mp4",
            filename=os.path.basename(downloaded_files[0]),
        )

    zip_path = os.path.join(temp_dir, "videos.zip")
    with zipfile.ZipFile(zip_path, "w") as zipf:
        for file in downloaded_files:
            zipf.write(file, arcname=os.path.basename(file))

    return FileResponse(zip_path, media_type="application/zip", filename="videos.zip")


@app.post("/audios")
async def post_audio(urls: Item, background_tasks: BackgroundTasks):

    queue = Queue()
    base_temp_dir = os.path.join(os.path.dirname(__file__), "temp")
    os.makedirs(base_temp_dir, exist_ok=True)
    temp_dir = tempfile.mkdtemp(dir=base_temp_dir)
    downloaded_files = []

    for url in urls.urls_vid:
        queue.push(url)

    for link in queue:
        ytb = YouTube(link)
        audio = ytb.streams.get_audio_only()
        audio_file = audio.download(output_path=temp_dir)

        base, _ = os.path.splitext(audio_file)
        mp3_file = base + ".mp3"
        os.rename(audio_file, mp3_file)
        downloaded_files.append(mp3_file)

    background_tasks.add_task(shutil.rmtree, temp_dir)

    if len(downloaded_files) == 1:
        return FileResponse(
            downloaded_files[0],
            media_type="audio/mpeg",
            filename=os.path.basename(downloaded_files[0]),
        )

    zip_path = os.path.join(temp_dir, "audios.zip")
    with zipfile.ZipFile(zip_path, "w") as zipf:
        for file in downloaded_files:
            zipf.write(file, arcname=os.path.basename(file))

    return FileResponse(zip_path, media_type="application/zip", filename="audios.zip")


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
