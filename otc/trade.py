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


# 获取单用户token
class LoginToken():
    # 获取交易平台用户登录token
    def top_token(self):
        data = {
            "password": url.login_password,
            "userAccount": "876522068@qq.com"
        }
        header = {
            "Content-Type": "application/json",
            "keyId": url.keyid
        }
        res = requests.post(url=url.login, data=json.dumps(data), headers=header).json()
        user_token = res["data"]["loginSuccessModel"]["rememberPasswordToken"]
        # print(user_token)
        return user_token

    # 登录AIC钱包，获取用户token
    def aic_login(self):
        data = {
            "email": "876522068@qq.com",
            "password": "ygb123456"
        }
        header = {
            "Content-Type": "application/json",
            "keyId": "5d12c14d64da4904931f751cd7504fe4"
        }
        login = requests.post(url=url.aic_login, data=json.dumps(data), headers=header).json()
        login_token = login["data"]["token"]
        return login_token


# 创建线程类
class ThreadTest(threading.Thread):
    def __init__(self, name_headers, name_sql):
        threading.Thread.__init__(self)
        self.n_list = add_data.get_name_list(name_sql)
        self.headers = name_headers

    # 获取用户token列表
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

    # 多用户买卖
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
            "tradePwd": url.trade_password,   # Y123456
            "userId": 547713774845571072
        }
        # 限价交易买
        price_deal_buy = requests.post(url=url.buy, data=json.dumps(data), headers=self.headers).json()
        print("限价交易（买）：", price_deal_buy)
        # 限价交易卖
        price_deal_sell = requests.post(url=url.sell, data=json.dumps(data), headers=self.headers).json()
        print("限价交易===（卖）：", price_deal_sell)
        return price_deal_buy

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

    # AIC钱包发送墨晶
    def aic_send(self, data, header):
        msg = requests.post(url=url.aic_send, data=json.dumps(data), headers=header).json()
        print(msg["code"])
        return msg

    def send_aic(self):
        msg = requests.get(url=url.aic_send_test).json()
        print(msg)
        return msg


if __name__ == '__main__':
    user_token = LoginToken()
    # 交易平台接口都不信息
    topex_headers = {
        "Content-Type": "application/json",
        "Access-Token": user_token.top_token(),
        "keyId": url.keyid
    }

    # AIC钱包接口头部信息
    data = {
        "coinId": 1,
        "coinName": "AIC",
        "toLabel": "测试性能",
        "toAddress": "BBktkXy19J7EAEFBBpQbWF8xSWSFX3BgFR",  # BGeLDFoNKoAGecETkDZPvf3xkArpXRGK7e
        "amount": 0.001
    }
    header = {
        "Content-Type": "application/json",
        "keyId": "5d12c14d64da4904931f751cd7504fe4",
        "Access-Token": user_token.aic_login()
    }

    # 获取用户名
    # sql = "SELECT useraccount FROM user_info WHERE id LIKE '536%' LIMIT 1;"
    sql = "SELECT useraccount FROM user_info WHERE id = 530335383058264064;"
    run = ThreadTest(topex_headers, sql)
    # get_token = run.get_token()
    sendmail = send_mailpy3.SendMail()
    originTime = int(round(time.time() * 1000))
    # 撮合交易长时间稳定测试
    # for i in range(0, 1):
    #     run_trade = run.buy_or_sell()
    #     if run_trade != "200":
    #         result = "测试异常"
    #         send_message = "程序执行异常，返回结果：" + run_trade + ", 执行到第" + (str(i + 1)) + "条记录。"
    #         sendmail.sendMessage(send_message, result)
    #         break
    #     if int((int(round(time.time() * 1000)) - originTime) / 1000) == 60:
    #         print("originTime:", originTime)
    #         print('程序每分钟执行：%d' % int(i + 1))
    #         break

    # 写一个循环运行指定方法，再添加多线程运行该方法，程序出现异常或完成的时候发送邮件通知并跳出循环
    # for count in range(0, 1):
    #     count += 1
    #     t_list = []
    #     for i in range(0, 0):
    #         t1 = threading.Thread(target=run.buy_or_sell)
    #         t_list.append(t1)
    #     for t in t_list:
    #         t.start()
    #     for t in t_list:
    #         t.join()
    #     if str(run.buy_or_sell()["code"]) != "200":
    #         result = "测试异常"
    #         sendmail.sendMessage(str(run.buy_or_sell()), result)
    #         break
    # else:
    #     result = "测试结果"
    #     sendmail.sendMessage("测试完成，程序执行结束，无异常返回！", result)

    # AIC钱包转账长时间稳定性测试
    for i in range(0, 100):
        print("第{0}条".format(i + 1))
        run_aic = run.send_aic()
        time.sleep(0.5)
        if str(run_aic["code"]) != "200":
            print(run_aic)
            result = "测试异常"
            send_message = "程序执行异常，返回结果：" + str(run_aic) + ", 执行到第" + (str(i + 1)) + "条记录。"
            sendmail.sendMessage(send_message, result)
            break
    # else:
    #     result = "测试结果"
    #     sendmail.sendMessage("测试完成，程序执行结束，无异常返回！", result)





