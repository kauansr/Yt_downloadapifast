import os
import zipfile
from pathlib import Path

from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


VIDEO_URL_1 = "https://youtube.com/shorts/2W488FPia54"
VIDEO_URL_2 = "https://youtu.be/jrOnBkyjH_s"
VIDEO_URL_3 = "https://youtu.be/Pa0_US5QZBY"
AUDIO_URL_1 = "https://youtu.be/hCyC4z9xXjM"


def test_post_videos_multiple():
    data = {
        "urls_vid": [
            VIDEO_URL_1,
            VIDEO_URL_2,
        ]
    }

    response = client.post("/videos", json=data)

    assert response.status_code == 200
    assert response.headers["content-type"] in {
        "application/zip",
        "video/mp4",
    }

    content_disposition = response.headers.get("content-disposition", "")

    assert "filename=" in content_disposition
    assert len(response.content) > 0


def test_post_video_single():
    data = {
        "urls_vid": [
            VIDEO_URL_3,
        ]
    }

    response = client.post("/videos", json=data)

    content_disposition = response.headers.get(
        "content-disposition",
        "",
    )

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("video/")
    assert (
        "filename=" in content_disposition
        or "filename*=" in content_disposition
    )
    assert len(response.content) > 0


def test_post_audios_multiple():
    data = {
        "urls_vid": [
            VIDEO_URL_1,
            VIDEO_URL_2,
        ]
    }

    response = client.post("/audios", json=data)

    assert response.status_code == 200
    assert response.headers["content-type"] in {
        "application/zip",
        "audio/mpeg",
    }

    content_disposition = response.headers.get(
        "content-disposition",
        "",
    )

    assert "filename=" in content_disposition
    assert len(response.content) > 0


def test_post_audio_single():
    data = {
        "urls_vid": [
            AUDIO_URL_1,
        ]
    }

    response = client.post("/audios", json=data)

    content_disposition = response.headers.get(
        "content-disposition",
        "",
    )

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("audio/")
    assert (
        "filename=" in content_disposition
        or "filename*=" in content_disposition
    )
    assert len(response.content) > 0


def test_temp_folder_cleanup():
    project_dir = Path(__file__).resolve().parent.parent
    temp_dir = project_dir / "temp"

    assert temp_dir.exists()
    assert not any(temp_dir.iterdir())


def test_zip_creation_on_videos(tmp_path):
    data = {
        "urls_vid": [
            VIDEO_URL_2,
            VIDEO_URL_1,
        ]
    }

    response = client.post("/videos", json=data)

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/zip"

    temp_zip_path = tmp_path / "test_downloaded_videos.zip"
    temp_zip_path.write_bytes(response.content)

    with zipfile.ZipFile(temp_zip_path, "r") as zip_ref:
        zip_files = zip_ref.namelist()

        print("Arquivos dentro do zip:", zip_files)

        assert len(zip_files) == 2


def test_zip_creation_on_audios(tmp_path):
    data = {
        "urls_vid": [
            VIDEO_URL_2,
            VIDEO_URL_1,
        ]
    }

    response = client.post("/audios", json=data)

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/zip"

    temp_zip_path = tmp_path / "test_downloaded_audios.zip"
    temp_zip_path.write_bytes(response.content)

    with zipfile.ZipFile(temp_zip_path, "r") as zip_ref:
        zip_files = zip_ref.namelist()

        print("Arquivos dentro do zip:", zip_files)

        assert len(zip_files) == 2
        assert all(file.endswith(".mp3") for file in zip_files)