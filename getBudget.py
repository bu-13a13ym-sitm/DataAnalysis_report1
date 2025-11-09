import requests as rq
import pandas as pd
from time import sleep
import re
from account import user_agent, api_key

#global settings:
header = {'User-Agent': user_agent}
url = 'http://webservice.recruit.co.jp/hotpepper/gourmet/v1/'
output_file = "budget.csv"
columns = ("店舗名", "予算テキスト", "予算")
en_columns = ("name", "budget")

def min_value(th=1000):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if result is None:
                return None
            try:
                if float(result) < th:
                    return None
            except(TypeError, ValueError):
                return None
            return result
        return  wrapper
    return decorator

@min_value(1000)
def extract_price(value):
    if pd.isna(value):
        return None

    text = str(value).replace(',', '').replace('円', '').replace('￥', '').replace('¥', '').replace('〜', '-').replace('～', '-').replace('－', '-')
    nums = re.findall(r'\d+', text)

    if len(nums) == 0:
        return None
    elif len(nums) == 1:
        return int(nums[0])
    else:
        if num_range := re.findall(r'\d+-\d+', text):
            nums = re.findall(r'\d+', num_range[0])
            return (int(nums[0]) + int(nums[-1])) / 2
        else:
            return(int(nums[0]))

if __name__ == "__main__":
    results = {column: [] for column in columns[:2]}
    prefecture = input("prefecture: ")
    keyword = prefecture
    params = {
        'keyword': keyword,
        'key': api_key,
        'range': '5',
        'count': '100',
        'format': 'json'
        }
    response = rq.get(url, headers=header, params=params)
    sleep(3.0)

    data = response.json()
    if 'results' not in data:
        print("failed to fetch data")
        exit(1)
    print("---response received---")
    print(f"num hit: {data['results']['results_returned']}")
    print("-----------------------")

    shops = data['results']['shop']
    for shop in shops:
        results[columns[0]].append(shop[en_columns[0]])
        results[columns[1]].append(shop[en_columns[1]]['average'])

    print(len(results[columns[0]]))
    df = pd.DataFrame(results)
    df[columns[2]] = df[columns[1]].apply(extract_price)
    df.to_csv(output_file, index=False, encoding='utf-8')
    print("file saved")