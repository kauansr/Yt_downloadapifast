from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from pytubefix import YouTube

from models.urlmodels import Item
from utils.fila_low_level import Queue

import uvicorn
import tempfile
import os
import shutil
import zipfile


app = FastAPI()


BASE_TEMP_DIR = os.path.join(
    os.path.dirname(__file__),
    "temp"
)

os.makedirs(BASE_TEMP_DIR, exist_ok=True)


# =========================
# CORS
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)


# =========================
# UTILS
# =========================

def create_temp_dir():
    return tempfile.mkdtemp(
        dir=BASE_TEMP_DIR
    )


def create_zip(files: list[str], zip_path: str):

    with zipfile.ZipFile(
        zip_path,
        "w",
        zipfile.ZIP_DEFLATED
    ) as zipf:

        for file in files:

            zipf.write(
                file,
                arcname=os.path.basename(file)
            )


# =========================
# VIDEOS
# =========================

@app.post("/videos")
async def post_vid(
    urls: Item,
    background_tasks: BackgroundTasks
):

    queue = Queue()

    for url in urls.urls_vid:
        queue.push(url)

    temp_dir = create_temp_dir()

    downloaded_files = []

    try:

        for link in queue:

            ytb = YouTube(link)

            vid = (
                ytb.streams
                .get_highest_resolution()
            )

            if not vid:
                raise Exception(
                    "Nenhum stream de vídeo encontrado."
                )

            file_path = vid.download(
                output_path=temp_dir
            )

            downloaded_files.append(
                file_path
            )

    except Exception as e:


        shutil.rmtree(
            temp_dir,
            ignore_errors=True
        )

        raise HTTPException(
            status_code=400,
            detail=f"Erro ao baixar vídeo: {e}"
        )

    # =========================
    # UM VÍDEO
    # =========================

    if len(downloaded_files) == 1:

        file = downloaded_files[0]

        background_tasks.add_task(
            shutil.rmtree,
            temp_dir,
            ignore_errors=True
        )

        return FileResponse(
            file,
            media_type="video/mp4",
            filename=os.path.basename(file)
        )

    # =========================
    # VÁRIOS VÍDEOS
    # =========================

    zip_path = os.path.join(
        temp_dir,
        "videos.zip"
    )

    try:

        create_zip(
            downloaded_files,
            zip_path
        )

    except Exception as e:

        shutil.rmtree(
            temp_dir,
            ignore_errors=True
        )

        raise HTTPException(
            status_code=500,
            detail=f"Erro ao criar zip: {e}"
        )

    background_tasks.add_task(
        shutil.rmtree,
        temp_dir,
        ignore_errors=True
    )

    return FileResponse(
        zip_path,
        media_type="application/zip",
        filename="videos.zip"
    )


# =========================
# AUDIOS
# =========================

@app.post("/audios")
async def post_audio(
    urls: Item,
    background_tasks: BackgroundTasks
):

    queue = Queue()

    for url in urls.urls_vid:
        queue.push(url)

    temp_dir = create_temp_dir()

    downloaded_files = []

    try:

        for link in queue:

            ytb = YouTube(link)

            audio = (
                ytb.streams
                .get_audio_only()
            )

            if not audio:
                raise Exception(
                    "Nenhum stream de áudio encontrado."
                )

            audio_file = audio.download(
                output_path=temp_dir
            )

      

            base, _ = os.path.splitext(
                audio_file
            )

            mp3_file = base + ".mp3"

            os.rename(
                audio_file,
                mp3_file
            )

           

            downloaded_files.append(
                mp3_file
            )

    except Exception as e:


        shutil.rmtree(
            temp_dir,
            ignore_errors=True
        )

        raise HTTPException(
            status_code=400,
            detail=f"Erro ao baixar áudio: {e}"
        )

    if len(downloaded_files) == 1:

        file = downloaded_files[0]
  


        background_tasks.add_task(
            shutil.rmtree,
            temp_dir,
            ignore_errors=True
        )

        return FileResponse(
            path=file,
            media_type="audio/mpeg",
            filename=os.path.basename(file)
        )


    zip_path = os.path.join(
        temp_dir,
        "audios.zip"
    )

    try:

        create_zip(
            downloaded_files,
            zip_path
        )

    except Exception as e:

        shutil.rmtree(
            temp_dir,
            ignore_errors=True
        )

        raise HTTPException(
            status_code=500,
            detail=f"Erro ao criar zip: {e}"
        )

    background_tasks.add_task(
        shutil.rmtree,
        temp_dir,
        ignore_errors=True
    )

    return FileResponse(
        zip_path,
        media_type="application/zip",
        filename="audios.zip"
    )


# =========================
# RUN
# =========================

if __name__ == "__main__":

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
