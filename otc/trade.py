import json
import re
import requests
import random
import threading
from otc import add_data
from otc import url
import time
from send import send_mailpy3

# 数据列表
time_lists = []
token_lists = []


# 创建线程类
class ThreadTest(threading.Thread):
    def __init__(self, name_headers, name_sql):
        threading.Thread.__init__(self)
        self.n_list = add_data.get_name_list(name_sql)
        self.headers = name_headers

    # 获取用户token
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
            res = requests.post(url=url.user_login, data=json.dumps(data),
                                headers=header).json()
            name_token = res["data"]["loginSuccessModel"]["rememberPasswordToken"]
            token_lists.append(name_token)
        return count

    # 多用户交易
    def trade(self):
        count = 0
        for token in token_lists:
            count += 1
            header = {
                "Content-Type": "application/json",
                "Access-Token": token,
                "keyId": "5d12c14d64da4904931f751cd7504fe4"
            }
            # price = random.randint(6, 10)
            amount = random.randint(1, 10)
            price = round(random.uniform(0.1, 1), 2)
            data = {
                "counterId": "520259173401755648",   # 开发环境用 512948910692499456   性能测试用 520259173401755648
                "entrustPrice": 1,
                "entrustTotalAmount": 1,
                "entrustType": 1,
                "tradePwd": "Y123456"
            }
            # 限价交易买
            price_deal_buy = requests.post(url=url.buy, data=json.dumps(data), headers=header).json()
            print("限价交易（买）：", price_deal_buy)
            # 限价交易卖
            price_deal_sell = requests.post(url=url.sell, data=json.dumps(data), headers=header).json()
            print("限价交易===（卖）：", price_deal_sell)
            # print("++++++++++++++++++++++++++++++++++++++", count)

        print("次数：", count)
        return count

    # 单用户买卖
    def buy_or_sell(self):
        data = {
            "counterId": "520259173401755648",
            "entrustPrice": 1,
            "entrustTotalAmount": 1,
            "entrustType": 1,
            "tradePwd": "Y123456",
            "userId": 530335383058264064
        }
        # 限价交易买
        for i in range(0, 10):
            price_deal_buy = requests.post(url=url.buy, data=json.dumps(data), headers=self.headers).json()
            print("限价交易（买）：", price_deal_buy)
            code = str(price_deal_buy["code"])
            # 限价交易卖
            price_deal_sell = requests.post(url=url.sell, data=json.dumps(data), headers=self.headers).json()
            print("限价交易===（卖）：", price_deal_sell)
            return code

    # 法币提取/充值
    def usd_extract(self):
        data = {
            "assetUserBankId": "527090031777693697",
            "tradePwd": "Y123456",
            "usdAmount": 100
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
          "coinCode": "AIC",
          "tradePwd": "Y123456"
        }
        extract = requests.post(url=url.coin_extract, data=json.dumps(data), headers=self.headers).json()
        print("用户虚拟币提取：", extract)
        return extract

    # 登录AIC钱包，获取用户token
    def aic_login(self):
        data = {
            "email": "694298407@qq.com",
            "password": "ygb123456"
        }
        header = {
            "Content-Type": "application/json",
            "keyId": "5d12c14d64da4904931f751cd7504fe4"
        }
        login = requests.post(url=url.login, data=json.dumps(data), headers=header).json()
        login_token = login["data"]["token"]
        return login_token

    # AIC钱包发送墨晶
    def aic_send(self):
        data = {
            "coinId": 1,
            "coinName": "AIC",
            "toLabel": "测试并发",
            "toAddress": "BDFfB9R7pWCARtjzcfhEf6ikeA34GmFZLK",
            "amount": 0.001
        }
        header = {
            "Content-Type": "application/json",
            "keyId": "5d12c14d64da4904931f751cd7504fe4",
            "Access-Token": self.aic_login()
        }
        send = requests.post(url=url.aic_send, data=json.dumps(data), headers=header).json()
        print(send)


if __name__ == '__main__':
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyQWNjb3VudCI6IjE4OTgxMjIxMDM3QHFxLmNvbSIsInR5cGUiOjEsImV4cCI6MTU0ODY0NDc2OCwidXNlcklkIjo1MzYyMzAwOTMyMjAwOTgwNDh9.o7Swu3hcVe9fmmuZH1tZNTYZzzWtvpV2pWffqGLm-ck"
    topex_headers = {
        "Content-Type": "application/json",
        "userAccount": "18981221037@qq.com",  # 性能测试 68068214905@qq.com  开发环境  28436519733@qq.com
        "userId": "536230093220098048",
        "Access-Token": token,
        "keyId": "5d12c14d64da4904931f751cd7504fe4"
    }

    # 获取用户名
    # sql = "SELECT useraccount FROM user_info WHERE id LIKE '536%' LIMIT 1;"
    sql = "SELECT useraccount FROM user_info WHERE id = 530335383058264064;"
    run = ThreadTest(topex_headers, sql)
    sendmail = send_mailpy3.SendMail()
    # run.aic_send()  # 运行AIC钱包转账
    # get_token = run.get_token()
    for i in range(0, 1):
        run_trade = run.buy_or_sell()
        if run_trade != "200":
            result = "测试异常"
            sendmail.sendMessage(run_trade, result)
            break
    # t_list = []
    # for i in range(0, 9):
    #     t1 = threading.Thread(target=run.aic_send)
    #     t_list.append(t1)
    # for t in t_list:
    #     t.start()
    # for t in t_list:
    #     t.join()

    # sum_time = sum(time_lists)/len(time_lists)
    # print(sum_time)


