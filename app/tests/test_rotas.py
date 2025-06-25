from main import app
from fastapi.testclient import TestClient
import zipfile
import os

client = TestClient(app)


def test_post_videos_multiple():
    urls = {
        "urls_vid": [
            "https://youtube.com/shorts/2W488FPia54?si=vBRCOqJ0kXdeKUg8",
            "https://youtu.be/jrOnBkyjH_s?si=xMvz4fo8rSj_p47m",
        ]
    }

    response = client.post("/videos", json=urls)

    assert response.status_code == 200
    assert response.headers["content-type"] in ["application/zip", "video/mp4"]
    assert "filename=" in response.headers["content-disposition"]
    assert len(response.content) > 0


def test_post_video_single():
    data_json = {"urls_vid": ["https://youtu.be/Pa0_US5QZBY?si=zeyT8LvhVHUymrNx"]}

    response = client.post("/videos", json=data_json)

    content_disp = response.headers.get("content-disposition", "")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("video/")
    assert "filename=" in content_disp or "filename*=" in content_disp
    assert len(response.content) > 0


def test_post_audios_multiple():
    urls = {
        "urls_vid": [
            "https://youtube.com/shorts/2W488FPia54?si=vBRCOqJ0kXdeKUg8",
            "https://youtu.be/jrOnBkyjH_s?si=xMvz4fo8rSj_p47m",
        ]
    }

    response = client.post("/audios", json=urls)

    assert response.status_code == 200
    assert response.headers["content-type"] in ["application/zip", "audio/mpeg"]
    assert "filename=" in response.headers["content-disposition"]
    assert len(response.content) > 0


def test_post_audio_single():
    data_json = {"urls_vid": ["https://youtu.be/hCyC4z9xXjM?si=C6hbt4krgx8Zb-17"]}

    response = client.post("/audios", json=data_json)

    content_disp = response.headers.get("content-disposition", "")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("audio/")
    assert "filename=" in content_disp or "filename*=" in content_disp
    assert len(response.content) > 0


def test_temp_folder_cleanup():
    temp_dir = os.path.join(os.path.dirname(__file__), "..", "temp")
    temp_dir = os.path.abspath(temp_dir)
    assert os.path.exists(temp_dir)
    assert len(os.listdir(temp_dir)) == 0


def test_zip_creation_on_videos():
    data = {
        "urls_vid": [
            "https://youtu.be/jrOnBkyjH_s?si=xMvz4fo8rSj_p47m",
            "https://youtube.com/shorts/2W488FPia54?si=vBRCOqJ0kXdeKUg8",
        ]
    }

    response = client.post("/videos", json=data)

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/zip"

    temp_zip_path = "test_downloaded_videos.zip"
    with open(temp_zip_path, "wb") as f:
        f.write(response.content)

    with zipfile.ZipFile(temp_zip_path, "r") as zip_ref:

        zip_files = zip_ref.namelist()
        print("Arquivos dentro do zip:", zip_files)

        assert len(zip_files) == 2

    import os

    os.remove(temp_zip_path)


def test_zip_creation_on_audios():
    data = {
        "urls_vid": [
            "https://youtu.be/jrOnBkyjH_s?si=xMvz4fo8rSj_p47m",
            "https://youtube.com/shorts/2W488FPia54?si=vBRCOqJ0kXdeKUg8",
        ]
    }

    response = client.post("/audios", json=data)

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/zip"

    temp_zip_path = "test_downloaded_audios.zip"
    with open(temp_zip_path, "wb") as f:
        f.write(response.content)

    with zipfile.ZipFile(temp_zip_path, "r") as zip_ref:
        zip_files = zip_ref.namelist()
        print("Arquivos dentro do zip:", zip_files)

        assert len(zip_files) == 2

        assert all(file.endswith(".mp3") for file in zip_files)

    os.remove(temp_zip_path)
