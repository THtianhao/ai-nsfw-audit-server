import requests
import json
import hashlib
import time
import re
import argparse
# 请求的 URL
url = "https://api.actpass.com/nft-api/api/nft/search"

# 请求头
headers = {
    "Host": "api.actpass.com",
    "Content-Length": "172",
    "Sec-Ch-Ua": '"Chromium";v="105", "Not)A;Brand";v="8"',
    "X-Timezone": "UTC-7:00",
    "X-Language": "zh",
    "Sec-Ch-Ua-Mobile": "?0",
    "X-Platform": "1",
    "Content-Type": "application/json",
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.54 Safari/537.36",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Origin": "https://app.actpass.com",
    "Sec-Fetch-Site": "same-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://app.actpass.com/",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.9"
}

SIGN_SECRET = "actpass@2022"

def obj_key_sort(d):
    """
    对字典的键进行排序，并返回一个新的按键排序的字典
    """
    sorted_keys = sorted(d.keys())
    return {key: d[key] for key in sorted_keys}

def get_signs(d):
    """
    生成用于签名的字符串，通过将排序后的键值对连接起来
    """
    sorted_dict = obj_key_sort(d)
    sign_str = ""
    for key, value in sorted_dict.items():
        sign_str += str(key) + str(value)
    return sign_str

def md5_hexdigest(value):
    """
    计算给定字符串的 MD5 哈希值，并返回其十六进制表示
    """
    return hashlib.md5(value.encode('utf-8')).hexdigest()

def get_date(dr):
    """
    根据输入字典生成包含时间戳和签名的新字典
    """
    # 获取当前 Unix 时间戳（秒）
    current_time = int(time.time())
    dr['time'] = current_time
    
    # 生成签名
    sign = md5_hexdigest(get_signs(dr) + SIGN_SECRET)
    
    # 返回更新后的字典
    dr['sign'] = sign
    return dr

def infonl(item):
    replacement = "zh"
    url=item['attribute_url'] % replacement
    response=requests.get(url)
    data = json.loads(response.text)

    # 查找 attribute_name 为 "混沌能量" 的 attribute_value
    for item2 in data:
        if item2['attribute_name'] == "混沌能量":
            attribute_value = item2['attribute_value']
            return attribute_value
            break
def infocb(item):
    replacement = "zh"
    url=item['attribute_url'] % replacement
    response=requests.get(url)
    data = json.loads(response.text)

    # 查找 attribute_name 为 "混沌能量" 的 attribute_value
    for item2 in data:
        if item2['attribute_name'] == "财宝值":
            attribute_value = item2['attribute_value']
            return attribute_value
            break

dr = {
    "title": "",
    "symbol": "MIS",
    "sort": 1,
    "page": 2,
    "page_size": 20,
    "version": "",
    "filter": "{\"category_two\":[\"73\"]}",  
}
def getnengliang(postdata):

    data = get_date(postdata)
    # 发送 POST 请求
    response = requests.post(url, headers=headers, json=data)
    # 检查响应状态
    if response.status_code == 200:
        # 解析 JSON 响应
        result = response.text

        data = json.loads(result)
        print(data["data"]["count"])
        # 输出解析后的结果
        if data["code"] == 0:
            print("Response Message:", data["msg"])
        
            items = data["data"]["list"]
            for item in items:

                attribute_value=''
                nengliangmun=item['title']
                match = re.search(r'\d+', nengliangmun)
                if match:
                    attribute_value = match.group(0)
                    
                else:
                    attribute_value =infonl(item)
                
                jiage=float(item['price'])/int(attribute_value)
                
                print(f"ID: {item['id']}, 类型: {item['symbol']}, 价格: {item['unit_price']}, 名称: {item['title']}, 能量:{attribute_value}, 单价:{round(jiage, 5)} ETH")
        else:
            print("Error:", data["msg"])
            
    else:
        print(f"Request failed with status code {response.status_code}")

def getcaibao(postdata):

    data = get_date(postdata)
    # 发送 POST 请求
    response = requests.post(url, headers=headers, json=data)
    # 检查响应状态
    if response.status_code == 200:
        # 解析 JSON 响应
        result = response.text

        data = json.loads(result)
        print(data["data"]["count"])
        # 输出解析后的结果
        if data["code"] == 0:
            print("Response Message:", data["msg"])
        
            items = data["data"]["list"]
            for item in items:

                attribute_value =infocb(item)
                
                jiage=float(item['price'])/int(attribute_value)
                
                print(f"ID: {item['id']}, 价格: {item['unit_price']}, 名称: {item['title']}, 财报值:{attribute_value}, 单价:{round(jiage, 5)} ETH")
        else:
            print("Error:", data["msg"])
            
    else:
        print(f"Request failed with status code {response.status_code}")



def getnft(postdata):

    data = get_date(postdata)
    # 发送 POST 请求
    response = requests.post(url, headers=headers, json=data)
    # 检查响应状态
    if response.status_code == 200:
        # 解析 JSON 响应
        result = response.text

        data = json.loads(result)
        print(data["data"]["count"])
        # 输出解析后的结果
        if data["code"] == 0:
            print("Response Message:", data["msg"])
        
            items = data["data"]["list"]
            for item in items:

                    replacement = "zh"
                    url2=item['attribute_url'] % replacement
                    response=requests.get(url2)
                    data2 = json.loads(response.text)
                    date3 =json.dumps(data2,ensure_ascii=False, indent=4)
                    
                    if date3.find("未鉴定") != -1:
                        for item2 in data2:
                            if  item2['attribute_name'] == "物品等级":
                                attribute_level = item2['attribute_value']
                        print(f"ID: {item['id']}, 价格: {item['unit_price']}, 名称: {item['title']},等级:\033[32m {attribute_level}\033[0m, 为鉴定")
                    else:
                        # 查找 attribute_name 为 "混沌能量" 的 attribute_value
                        for item2 in data2:
                            if  item2['attribute_name'] == "物品等级":
                                attribute_level = item2['attribute_value']
                            if  item2['attribute_name'] == "财宝值":   
                                attribute_caibao = item2['attribute_value']
                            if  item2['attribute_name'] == "混沌能量":   
                                attribute_nengliang= item2['attribute_value']
                            if  item2['attribute_name'] == "混沌属性":   
                                attribute_shuxing = item2['attribute_value']
                            if  item2['attribute_name'] == "混沌词缀":   
                                attribute_cizhui = item2['attribute_value']
                        
                        jiage=float(item['price'])/int(attribute_caibao)
                    
                        print(f"ID: {item['id']}, 价格: {item['unit_price']}, 名称: {item['title']},等级:\033[32m {attribute_level}\033[0m, 财宝值: \033[32m {attribute_caibao}\033[0m,能量: {attribute_nengliang},单价:{round(jiage, 5)} ETH,混沌属性: {attribute_shuxing},混沌词缀: {attribute_cizhui}")
        else:
            print("Error:", data["msg"])
            
    else:
        print(f"Request failed with status code {response.status_code}")


if __name__ == "__main__":

 parser = argparse.ArgumentParser(description="Update filter in dictionary")

# Add command-line arguments
parser.add_argument('--type', type=str, help='Type of update', required=True)
parser.add_argument('--page', type=int, help='Page number', required=True)
parser.add_argument('--level', type=str, help='Item level for filter')
parser.add_argument('--info', type=str, help='Category two values for filter')

# Parse command-line arguments
args = parser.parse_args()

# Update the filter and other fields based on arguments
filter_dict = json.loads(dr["filter"])

if args.level is not None:
    filter_dict={}
    filter_dict["item_level"] = [args.level]

if args.info:
    filter_dict["category_two"] = [value.strip() for value in args.info.split(',')]



# Perform actions based on the type argument
if args.type == "nl":
    filter_dict["category_two"] = ["73"]
    dr["filter"] = json.dumps(filter_dict)
    dr["page"] = args.page
    getnengliang(dr)
elif args.type == "cb":
    filter_dict["category_two"] = ["82"]
    dr["filter"] = json.dumps(filter_dict)
    dr["page"] = args.page
    getcaibao(dr)
elif args.type == "nft":
    dr["filter"] = json.dumps(filter_dict)
    dr["symbol"] = "SRF"
    dr["page"] = args.page
    print(dr)
    getnft(dr)
else:
    print("Unknown type specified. Please use 'nl', 'cb', or 'nft'.")