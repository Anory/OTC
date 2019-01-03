import json
import re
import requests
import random
import threading
from otc import add_data
from otc import url
import time

# 数据列表
time_lists = []
token_lists = []


# 创建线程类
class ThreadTest(threading.Thread):
    def __init__(self, name_id, name_headers, name_sql):
        threading.Thread.__init__(self)
        self.n_list = add_data.get_name_list(name_sql)
        self.user_id = name_id
        self.headers = name_headers

    # 获取用户token和id
    def get_token(self):
        count = 1
        for username in self.n_list:
            count += 1
            data = {
                "password": "YGB423542",
                "userAccount": username
            }
            header = {
                "Content-Type": "application/json",
                "keyId": "5d12c14d64da4904931f751cd7504fe4"
            }
            res = requests.post(url="http://172.16.2.22:16010/api/user/front/userSign/doSignIn", data=json.dumps(data),
                                headers=header).json()
            name_token = res["data"]["loginSuccessModel"]["rememberPasswordToken"]
            token_lists.append(name_token)
        return count

    # 多用户交易
    def trade(self):
        count = 1
        for token in token_lists:
            count += 1
            header = {
                "Content-Type": "application/json",
                "Access-Token": token,
                "keyId": "5d12c14d64da4904931f751cd7504fe4"
            }
            price = random.randint(1, 30)
            amount = random.randint(1, 50)
            data = {
                "counterId": "528568795921543168",
                "entrustPrice": price,
                "entrustTotalAmount": amount,
                "entrustType": 1,
                "tradePwd": "Y123456"
            }
            # 限价交易买
            price_deal_buy = requests.post(url=url.buy, data=json.dumps(data), headers=header).json()
            print("限价交易（买）：", price_deal_buy)
            # 限价交易卖
            # price_deal_sell = requests.post(url=url.sell, data=json.dumps(data), headers=headers).json()
            # print("限价交易===（卖）：", price_deal_sell)
        return count

    # 单用户买卖
    def buy_or_sell(self):
        data = {
            "counterId": "528568795921543168",
            "entrustPrice": "1",
            "entrustTotalAmount": "1",
            "entrustType": 1,
            "tradePwd": "Y123456",
            "userId": self.user_id
        }
        # 限价交易买
        # price_deal_buy = requests.post(url=url.buy, data=json.dumps(data), headers=headers).json()
        # code = price_deal_buy["code"]
        # if code != 200:
        #     print("错误！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！")
        # print("限价交易（买）：", price_deal_buy)
        # 限价交易卖
        price_deal_sell = requests.post(url=url.sell, data=json.dumps(data), headers=self.headers).json()
        print("限价交易===（卖）：", price_deal_sell)
        return price_deal_sell

    # 法币提取/充值
    def usd_extract(self):
        data = {
            "assetUserBankId": "527090031777693697",
            "tradePwd": "Y123456",
            "usdAmount": 10
        }
        start_time = time.time()
        extract = requests.post(url=url.usd_extract, data=json.dumps(data), headers=self.headers).json()
        # recharge = requests.post(url=url.asset_recharge, data=json.dumps(data), headers=headers).json()
        end_time = time.time()
        time_lists.append(end_time-start_time)
        print("用户提取：", extract)
        return extract

    # 用户虚拟币提取
    def coin_extract(self):
        data = {
          "amount": 10,
          "coinAddressId": 526068429162168328,
          "coinCode": "BTC",
          "tradePwd": "Y123456"
        }
        extract = requests.post(url=url.coin_extract, data=json.dumps(data), headers=self.headers).json()
        print("用户虚拟币提取：", extract)
        return extract


if __name__ == '__main__':
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyQWNjb3VudCI6IjM0Njk4OTYxNjEzQHFxLmNvbSIsInR5cGUiOjEsIm" \
            "V4cCI6MTU0NjQyMDgyMCwidXNlcklkIjo1Mjg1MjUzNzYxNTkzNjMwNzJ9.88T9dMQgvDtYlaN5Okmwv4Nu8DDE70hBXvXJqLr9XbE"
    user_id = "528525376159363072"
    headers = {
        "Content-Type": "application/json",
        "userAccount": "34698961613@qq.com",
        "userId": "528525376159363072",
        "Access-Token": token,
        "keyId": "5d12c14d64da4904931f751cd7504fe4"
    }
    # 获取用户名
    sql = "SELECT useraccount FROM user_info WHERE id LIKE '528%' LIMIT 100;"
    run = ThreadTest(user_id, headers, sql)
    # get_token = run.get_token()
    # run_trade = run.trade()
    t_list = []
    for i in range(0, 150):
        t1 = threading.Thread(target=run.usd_extract)
        t_list.append(t1)
    for t in t_list:
        t.start()
    for t in t_list:
        t.join()

    # sum_time = sum(time_lists)/len(time_lists)
    # print(sum_time)


