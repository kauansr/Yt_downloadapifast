from typing import Annotated
from fastapi import FastAPI, Depends
from pytubefix import YouTube
from models.urlmodels import Item
import uvicorn
from utils.fila_low_level import Queue
import os

app = FastAPI()

queue = Queue()


@app.post("/videos")
async def post_vid(urls: Item):

    if len(urls.urls_vid) > 1:
        for url in urls.urls_vid:
            queue.push(url)

        for item in queue:
            ytb = YouTube(str(item))
            vid = ytb.streams.get_highest_resolution()
            vid.download("downloads/videos")
        return {"Baixado por ultimo": ytb.title}

    ytb = YouTube(urls.urls_vid[0])
    vid = ytb.streams.get_highest_resolution()
    vid.download("downloads/videos")

    return {"Baixado": ytb.title}


@app.post("/audios")
async def post_audio(urls: Item):

    if len(urls.urls_vid) > 1:
        for url in urls.urls_vid:
            queue.push(url)

        for item in queue:
            ytb = YouTube(str(item))
            audio = ytb.streams.get_audio_only()
            audio_downl = audio.download("downloads/audios")
            base, ext = os.path.splitext(audio_downl)
            novo_arquivo = base + ".mp3"
            os.rename(audio_downl, novo_arquivo)
        return {"Baixado por ultimo": ytb.title}

    ytb = YouTube(urls.urls_vid[0])
    audio = ytb.streams.get_audio_only()
    audio_downl = audio.download("downloads/audios")
    base, ext = os.path.splitext(audio_downl)
    novo_arquivo = base + ".mp3"
    os.rename(audio_downl, novo_arquivo)

    return {"Baixado": ytb.title}


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
