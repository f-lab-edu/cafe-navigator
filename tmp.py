import requests, json
import os


def get_places(keyword):
    url = 'https://dapi.kakao.com/v2/local/search/keyword.json?query=' + keyword
    headers = {"Authorization": f"KakaoAK {os.environ['KAKAO_API_KEY']}"}
    api_json = json.loads(str(requests.get(url, headers=headers).text))
    return api_json


crd = get_places("정자동 카페")

