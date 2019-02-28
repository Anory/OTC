import pymysql
import requests
import json
import random
from otc import url
import threading


# 链接性能测试数据库
otc_connect = pymysql.Connect(
    host='172.16.3.103',
    port=3306,
    user='topex',
    passwd='topex123456',
    db='topex',
    charset='utf8'
)

# 链接开发环境数据库
# otc_connect = pymysql.Connect(
#     host='172.16.2.23',
#     port=3306,
#     user='rddb',
#     passwd='mozi123456',
#     db='topex',
#     charset='utf8'
# )


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
    email = random.randint(9999999, 100000000)
    data = {
        "confirmPassword": "154988818ww",
        "countryCode": "zh",
        "email": "{0}@qq.com".format(email),
        "othersInvitationCode": "string",
        "password": "YGB423542",
        "userName": email,
        "verificationCode": "123456"
    }
    res = requests.post(url="http://172.16.3.102:16010/api/user/front/userRegister/register", data=json.dumps(data), headers=headers).json()
    print(res)
    return res


# 获取用户token
def get_token(username_list, headers):
    for username in username_list:
        data = {
            "password": "YGB423542",
            "userAccount": username
        }
        res = requests.post(url=url.user_login, data=json.dumps(data), headers=headers).json()
        token = res["data"]["loginSuccessModel"]["rememberPasswordToken"]
        print("用户登录token：", token)
        # print(json.loads(res))
        print("用户登录返回：", res)
        return res


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
    for i in range(0, 5):
        run = register(header)









