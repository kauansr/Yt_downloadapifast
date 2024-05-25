from main import app
from fastapi.testclient import TestClient


client = TestClient(app)


def test_post_list_return_str():
    urls = {
        "urls_vid": ["https://youtube.com/shorts/2W488FPia54?si=vBRCOqJ0kXdeKUg8","https://youtu.be/jrOnBkyjH_s?si=xMvz4fo8rSj_p47m"]
    }

    response = client.post('/videos', json=urls)

    assert response.json() == {"Baixado por ultimo": "Como NÃO jogar Slendytubbies 3"}


def test_post_str_return_str():

    data_json = {
        "urls_vid": ["https://youtu.be/Pa0_US5QZBY?si=zeyT8LvhVHUymrNx"]
    }

    response = client.post('/videos', json=data_json)


    assert response.json() == {"Baixado": "Alansoca REFERENCE?"}


def test_post_audios_list_return_str():
    urls = {
        "urls_vid": ["https://youtube.com/shorts/2W488FPia54?si=vBRCOqJ0kXdeKUg8","https://youtu.be/jrOnBkyjH_s?si=xMvz4fo8rSj_p47m"]
    }

    response = client.post('/audios', json=urls)

    assert response.json() == {"Baixado por ultimo": "Como NÃO jogar Slendytubbies 3"}


def test_post_audios_str_return_str():

    data_json = {
        "urls_vid": ["https://youtu.be/hCyC4z9xXjM?si=C6hbt4krgx8Zb-17"]
    }

    response = client.post('/audios', json=data_json)


    assert response.json() == {"Baixado": "ESSE FOI O GRITO CORTADO MAIS PERFEITO DOS ULTIMOS TEMPOS"}