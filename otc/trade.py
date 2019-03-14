import json
import re
import requests
import random
import threading
from otc import url
import time, datetime
from send import send_mailpy3
from otc import get_data


# 数据列表
time_lists = []
token_lists = []


# 创建线程类
class ThreadTest(threading.Thread):
    def __init__(self, data, name_headers, sql):
        threading.Thread.__init__(self)
        self.get_data = get_data.GetData()
        self.sql = sql
        self.headers = name_headers
        self.data = data

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
        amount = random.randint(30, 80)
        price = round(random.uniform(4, 8), 3)
        data = {
            "counterId": "520259173401755648",
            "entrustPrice": price,
            "entrustTotalAmount": amount,
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

    # 多用户法币充值检查用户识别码是否会出现重复
    def usd_extract(self):
        endtime = datetime.datetime(2019, 3, 14, 17, 0)
        num = 0
        sign_list = []
        user_info_list = self.get_data.get_user_info_list(self.sql)
        for i in range(0, 11000):
            for token, id, useraccount in user_info_list:
                num += 1
                data = {
                    "assetUserBankId": "527090031777693697",
                    "tradePwd": url.trade_password,
                    "usdAmount": 1000
                }
                headers = {
                    "userAccount": useraccount + "@qq.com",
                    "userId": id,
                    "Content-Type": "application/json",
                    "Access-Token": token,
                    "keyId": url.keyid
                }
                # r = requests.post(url=url.usd_extract, data=json.dumps(data), headers=self.headers).json()
                r = requests.post(url=url.asset_recharge, data=json.dumps(data), headers=headers).json()
                # print("用户充值：", r)
                sign = r["data"]["signCode"]
                sign_list.append(sign)
                print(sign, "====================》", num)
                time.sleep(0.3)
            if datetime.datetime.now() > endtime:
                print("停止时间：", datetime.datetime.now())
                break
        # 将列表中重复的识别码提取出来存放到一个新的列表里面
        repeat_code = []
        for i in sign_list:
            if sign_list.count(i) > 1:
                repeat_code.append(i)
        print(repeat_code, len(repeat_code))
        return repeat_code



    # 用户虚拟币提取
    def coin_extract(self):
        data = {
          "amount": 0.001,
          "coinAddressId": 554603725084311552,
          "coinCode": "AIC",
          "tradePwd": "Y123456"
        }
        r = requests.post(url=url.coin_extract, data=json.dumps(data), headers=self.headers).json()
        print("用户虚拟币提取：", r)
        return r

    # AIC钱包转账
    def aic_send(self):
        r = requests.post(url=url.aic_send, data=json.dumps(self.data), headers=self.headers)
        print("请求响应时间：", r.elapsed.total_seconds())  # 获取响应时间
        msg = r.json()
        print(msg)
        return msg

    # 通过江宗越提供的接口测试转账
    def send_aic(self):
        r = requests.get(url=url.aic_send_test)
        print("请求响应时间：", r.elapsed.total_seconds())  # 获取响应时间
        msg = r.json()
        return msg

    # 新旧AIC兑换（需求已改）
    def aic_exchange(self):
        r = requests.post(url=url.aic_exchange, data=json.dumps(self.data), headers=self.headers)
        print("请求响应时间：", r.elapsed.total_seconds())  # 获取响应时间
        msg = r.json()
        print(msg)
        return msg

    # 多个用户往同一个地址转账或同一个账号向多个地址转账
    def aic_transfer(self):
        num = 0
        token_list = self.get_data.get_token_list(self.sql)
        # address_list = self.get_data.get_user_address(self.sql)
        for i in range(0, 2):
            for token in token_list:
                data = {
                    "coinId": 3,
                    "coinName": "AIC2",
                    "toLabel": "测试性能",
                    "toAddress": "375T6FPAizNPkxo7m87iHEiEsy9b8bAezk",
                    "amount": 0.0001
                }
                aic_header = {
                    "Content-Type": "application/json",
                    "keyId": "5d12c14d64da4904931f751cd7504fe4",
                    "Access-Token": token
                }
                r = requests.post(url=url.aic_send, data=json.dumps(data), headers=aic_header)
                print("请求响应时间：", r.elapsed.total_seconds())  # 获取响应时间
                num += 1
                print(r.json(), "======>", num, "----", i)
        return


if __name__ == '__main__':
    user_token = get_data.GetData()
    # 交易平台接口头部信息
    topex_headers = {
        "userAccount": "56740725@qq.com",
        "userId": "547076226666344448",
        "Content-Type": "application/json",
        "Access-Token": user_token.top_token(),
        "keyId": url.keyid
    }

    # AIC钱包转账data
    data = {
        "coinId": 3,
        "coinName": "AIC2",
        "toLabel": "测试性能",
        "toAddress": "37TEPdfoRAx6h9Cq887iBo8E4xvzEFv5a7",  # BGeLDFoNKoAGecETkDZPvf3xkArpXRGK7e
        "amount": 0.02
    }

    # AIC钱包兑换data（已没用）
    exchange_data = {
          "coinId": 1,
          "coinName": "AIC",
          "newCoinId": 3,
          "amount": 0.0001
    }
    # aic_header = {
    #     "Content-Type": "application/json",
    #     "keyId": "5d12c14d64da4904931f751cd7504fe4",
    #     "Access-Token": user_token.aic_login()
    # }

    # 获取用户名
    name_sql = "SELECT useraccount FROM user_info WHERE useraccount = '11682852@qq.com';"
    addr_sql = "SELECT t3.addr FROM user_info t1 INNER JOIN asset t2 on t1.id = t2.user_id INNER JOIN address " \
               "t3 on t2.id = t3.asset_id WHERE t1.username != '876522068@qq.com' AND t1.username != '694298407@qq.com'" \
               " AND t3.is_contact = 0;"
    run = ThreadTest(data, topex_headers, name_sql)
    # run.aic_transfer()  # AIC轻钱包多用转账
    run.usd_extract()
    sendmail = send_mailpy3.SendMail()
    originTime = int(round(time.time() * 1000))
    # 撮合交易长时间稳定测试
    # for i in range(0, 1000):
    #     run_trade = run.buy_or_sell()
    #     time.sleep(5)
    #     if str(run_trade["code"]) != "200":
    #         result = "测试异常"
    #         send_message = "程序执行异常，返回结果：" + run_trade + ", 执行到第" + (str(i + 1)) + "条记录。"
    #         sendmail.sendMessage(send_message, result)
    #         break
    #     if int((int(round(time.time() * 1000)) - originTime) / 1000) == 60:
    #         print("originTime:", originTime)
    #         print('程序每分钟执行：%d' % int(i + 1))
    #         break

    # 写一个循环运行指定方法，再添加多线程运行该方法，程序出现异常或完成的时候发送邮件通知并跳出循环
    # for count in range(0, 5):
    #     t_list = []
    #     for i in range(0, 300):
    #         t = threading.Thread(target=run.aic_send())
    #         t_list.append(t)
    #     for t in t_list:
    #         t.start()
    #     for t in t_list:
    #         t.join()
    #     if str(run.aic_send()["code"]) != "200":
    #         result = "测试异常"
    #         send_message = "程序执行异常，返回结果：" + str(run.aic_send())
    #         sendmail.sendMessage(send_message, result)
    #         break
    # else:
    #     result = "测试结果"
    #     sendmail.sendMessage("测试完成，程序执行结束，无异常返回！", result)

    # AIC钱包转账长时间稳定性测试
    # for i in range(0, 1):
    #     print("第{0}条".format(i + 1))
    #     run_aic = run.aic_send()
    #     if str(run_aic["code"]) != "200":
    #         print(run_aic)
    #         result = "测试异常"
    #         send_message = "程序执行异常，返回结果：" + str(run_aic) + ", 执行到第" + (str(i + 1)) + "条记录。"
    #         sendmail.sendMessage(send_message, result)
    #         break
    # else:
    #     result = "测试结果"
    #     sendmail.sendMessage("测试完成，程序执行结束，无异常返回！", result)






