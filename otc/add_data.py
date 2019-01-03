import pymysql
import requests
import json
import random
import threading


# 链接otc测试数据库
otc_connect = pymysql.Connect(
    host='172.16.2.23',
    port=3306,
    user='rddb',
    passwd='mozi123456',
    db='topex',
    charset='utf8'
)


# 获取用户账号列表
def get_name_list(sql):
    otc_cursor = otc_connect.cursor()
    otc_cursor.execute(sql)
    name = otc_cursor.fetchall()
    lists = []
    for i in name:
        lists.append(",".join(list(i)))
    return lists


# 用户注册
def register(headers):
    email = random.randint(100000, 99999999999)
    data = {
        "confirmPassword": "154988818ww",
        "countryCode": "zh",
        "email": "{0}@qq.com".format(email),
        "othersInvitationCode": "string",
        "password": "YGB423542",
        "userName": email,
        "verificationCode": "123456"
    }
    res = requests.post(url="http://172.16.2.22:16010/api/user/front/userRegister/register", data=json.dumps(data), headers=headers).json()
    print(res)
    return res


# 获取用户token
def get_token(username_list, headers):
    for username in username_list:
        data = {
            "password": "YGB423542",
            "userAccount": username
        }
        res = requests.post(url="http://172.16.2.22:16010/api/user/front/userSign/doSignIn", data=json.dumps(data), headers=headers).json()
        token = res["data"]["loginSuccessModel"]["rememberPasswordToken"]
        print("用户登录token：", token)
        # print(json.loads(res))
        print("用户登录返回：", res)
        return res


# 用户交易
def trade(username_list):
    count = 0
    for username in username_list:
        data = {
            "password": "YGB423542",
            "userAccount": username
        }
        header = {
            "Content-Type": "application/json",
            "keyId": "5d12c14d64da4904931f751cd7504fe4"
        }
        res = requests.post(url="http://172.16.2.22:16010/api/user/front/userSign/doSignIn", data=json.dumps(data), headers=header).json()
        token = res["data"]["loginSuccessModel"]["rememberPasswordToken"]
        user_id = res["data"]["userBasic"]["id"]
        print("用户ID:", user_id)
        headers = {
            "Content-Type": "application/json",
            "Access-Token": token,
            "keyId": "5d12c14d64da4904931f751cd7504fe4"
        }
        price = random.randint(1, 30)
        amount = random.randint(10000, 50)
        data = {
            "counterId": "528568795921543168",
            "entrustPrice": price,
            "entrustTotalAmount": amount,
            "entrustType": 1,
            "tradePwd": "Y123456",
            "userId": user_id
        }
        # 限价交易买
        price_deal_buy = requests.post(url="http://172.16.2.22:16010/api/trade/tradeEntrust/buyEntrust",
                                       data=json.dumps(data), headers=headers).json()
        print("限价交易（买）：", price_deal_buy)
        # 限价交易卖
        # price_deal_sell = requests.post(url="http://172.16.2.22:16010/api/trade/tradeEntrust/sellEntrust",
        # data=json.dumps(data), headers=headers).json()
        # print("限价交易===（卖）：", price_deal_sell)
    return count


# 单个用户买卖
def buy_or_sell(user_id, token):
    headers = {
        "Content-Type": "application/json",
        "Access-Token": token,
        "keyId": "5d12c14d64da4904931f751cd7504fe4"
    }
    price = 1
    amount = 1
    data = {
        "counterId": "528568795921543168",
        "entrustPrice": price,
        "entrustTotalAmount": amount,
        "entrustType": 1,
        "tradePwd": "Y123456",
        "userId": user_id
    }
    # 限价交易买
    # price_deal_buy = requests.post(url="http://172.16.2.22:16010/api/trade/tradeEntrust/buyEntrust",
    #                                data=json.dumps(data), headers=headers).json()
    # code = price_deal_buy["code"]
    # if code != 200:
    #     print("错误！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！")
    # print("限价交易（买）：", price_deal_buy)
    # 限价交易卖
    price_deal_sell = requests.post(url="http://172.16.2.22:16010/api/trade/tradeEntrust/sellEntrust",
                                    data=json.dumps(data), headers=headers).json()
    print("限价交易===（卖）：", price_deal_sell)


if __name__ == '__main__':
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyQWNjb3VudCI6IjM0Njk4OTYxNjEzQHFxLmNvbSIsInR5cGUiOj" \
            "EsImV4cCI6MTU0NjA3MTkwNSwidXNlcklkIjo1Mjg1MjUzNzYxNTkzNjMwNzJ9.wKVMEjl-nE_cyfTwbXGoNTbM2yApHBjoJ8cfKXp76F0"
    user_id = "528525376159363072"
    header = {
        "Content-Type": "application/json",
        "keyId": "5d12c14d64da4904931f751cd7504fe4"
    }
    sql = "SELECT useraccount FROM user_info WHERE id LIKE '528%' LIMIT 100;"
    name_list = get_name_list(sql)
    # print(name_list)
    # run_login = get_token(name_list, header)
    # run_trade = trader(name_list)
    t_list = []
    for i in range(200):
        t1 = threading.Thread(target=buy_or_sell, args=(user_id, token))
        t_list.append(t1)
    for t in t_list:
        t.start()
    for t in t_list:
        t.join()









