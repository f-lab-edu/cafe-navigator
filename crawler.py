import requests, json
import os
import collections


def get_places(keyword, start_x, start_y, end_x, end_y):
    page_num = 1
    all_data_list=[]

    params = {'query': keyword, 'page': page_num, 'rect': f'{start_x},{start_y},{end_x},{end_y}'}
    headers = {"Authorization": f"KakaoAK {os.environ['KAKAO_API_KEY']}"}
    
    while True:
        url = 'https://dapi.kakao.com/v2/local/search/keyword.json'
        res = json.loads(str(requests.get(url, params=params, headers=headers).text))
        search_count = res['meta']['total_count']

        if search_count > 15:
            dividing_x = (start_x + end_x) / 2
            dividing_y = (start_y + end_y) / 2
            all_data_list.extend(get_places(keyword, start_x, start_y, dividing_x, dividing_y))
            all_data_list.extend(get_places(keyword, dividing_x, start_y, end_x, dividing_y))
            all_data_list.extend(get_places(keyword, start_x, dividing_y, dividing_x, end_y))
            all_data_list.extend(get_places(keyword, dividing_x, dividing_y, end_x, end_y))
            return all_data_list
        else:
            if res['meta']['is_end']:
                all_data_list.extend(res['documents'])
                return all_data_list
            else:
                page_num += 1
                all_data_list.extend(res['documents'])
        

def overlapped_data(keyword, start_x, start_y, next_x, next_y, num_x, num_y):
    overlapped_result = []

    # 지도를 사각형으로 나누면서 데이터 받아옴
    for i in range(1, num_x+1):   ## 1,10
        end_x = start_x + next_x
        initial_start_y = start_y
        for j in range(1, num_y+1):  ## 1,6
            end_y = initial_start_y + next_y
            each_result = get_places(keyword, start_x, initial_start_y, end_x, end_y)
            overlapped_result.extend(each_result)
            initial_start_y = end_y
        start_x = end_x
    
    return overlapped_result

# 서울 위도 경도
start_x = 126.8
start_y = 37.4
next_x = 0.01
next_y = 0.01
num_x = 12
num_y = 6
# end_x = 127.2
# end_y = 37.7

overlapped_result = overlapped_data("카페", start_x, start_y, next_x, next_y, num_x, num_y)
results = list(map(dict, collections.OrderedDict.fromkeys(tuple(sorted(d.items())) for d in overlapped_result)))
print(len(results), results[0])