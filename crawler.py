import asyncio
import aiohttp
import json
import datetime
import collections
import os

def make_url(keyword, start_x, start_y, end_x, end_y):
    return {
        "url": 'https://dapi.kakao.com/v2/local/search/keyword.json',
        "headers": {"Authorization": f"KakaoAK {os.environ['KAKAO_API_KEY']}"},
        "params": {
            'query': keyword,
            'page': 1,
            'rect': f'{start_x},{start_y},{end_x},{end_y}'
        }
    }


async def fetch_places(session, requests_condition, all_data_list):
    while True:
        async with session.get(**requests_condition) as response:
            data = await response.text()
            res = json.loads(data)
            search_count = res['meta']['total_count']
            pageable_count = res['meta']['pageable_count']
            print(search_count, pageable_count)
            if search_count <= 45:
                if res['meta']['is_end']:
                    all_data_list.extend(res['documents'])
                    return
                else:
                    all_data_list.extend(res['documents'])
                    requests_condition["params"]["page"] += 1
            else:
                tasks = []
                keyword = requests_condition["params"]["query"]
                end_x = float(requests_condition["params"]["rect"].split(',')[-2])
                end_y = float(requests_condition["params"]["rect"].split(',')[-1])

                dividing_x = (start_x + end_x) / 2
                dividing_y = (start_y + end_y) / 2
                t1 = get_places(keyword, start_x, start_y, dividing_x, dividing_y, all_data_list=all_data_list)
                t2 = get_places(keyword, dividing_x, start_y, end_x, dividing_y, all_data_list=all_data_list)
                t3 = get_places(keyword, start_x, dividing_y, dividing_x, end_y, all_data_list=all_data_list)
                t4 = get_places(keyword, dividing_x, dividing_y, end_x, end_y, all_data_list=all_data_list)
                tasks.extend([t1, t2, t3, t4])
                await asyncio.gather(*tasks)
                return all_data_list

async def get_places(keyword, start_x, start_y, end_x, end_y, all_data_list=[]):
    requests_condition = make_url(keyword, start_x, start_y, end_x, end_y)
    
    async with aiohttp.ClientSession() as session:
        await fetch_places(session, requests_condition, all_data_list)

async def overlapped_data(keyword, start_x, start_y, next_x, next_y, num_x, num_y):
    start_time = datetime.datetime.now()
    overlapped_result = []

    tasks = []
    for i in range(1, num_x + 1):
        end_x = start_x + next_x
        initial_start_y = start_y

        for j in range(1, num_y + 1):
            end_y = initial_start_y + next_y
            task = get_places(keyword, start_x, initial_start_y, end_x, end_y, all_data_list=overlapped_result)
            tasks.append(task)
            initial_start_y = end_y
        start_x = end_x
    
    await asyncio.gather(*tasks)

    end_time = datetime.datetime.now()
    print(f"speed: {end_time - start_time}")

    return overlapped_result

# 서울 위도 경도
start_x = 126.8
start_y = 37.4
next_x = 0.01
next_y = 0.01
num_x = 4
num_y = 4

async def main():
    overlapped_result = await overlapped_data("카페", start_x, start_y, next_x, next_y, num_x, num_y)
    results = list(map(dict, collections.OrderedDict.fromkeys(tuple(sorted(d.items())) for d in overlapped_result)))
    print(len(results))

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
