from otc import url
import requests
import json
import pymysql


# 链接性能测试数据库
otc_connect = pymysql.Connect(
    host='172.16.3.103',
    port=3306,
    user='topex',
    passwd='topex123456',
    db='topex',
    charset='utf8'
)


# 获取用户数据
class GetData():
    # 获取交易平台用户登录token
    def top_token(self):
        data = {
            "password": url.login_password,
            "userAccount": "56740725@qq.com"  # 63443647@qq.com
        }
        header = {
            "Content-Type": "application/json",
            "keyId": url.keyid
        }
        res = requests.post(url=url.login, data=json.dumps(data), headers=header).json()
        # print(res)
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

    # 获取用户账号列表
    def get_name_list(self, sql):
        otc_cursor = otc_connect.cursor()
        otc_cursor.execute(sql)
        name = otc_cursor.fetchall()
        name_lists = []
        for i in name:
            name_lists.append(",".join(list(i)))
        return name_lists

    # 获取用户地址
    def get_user_address(self, sql):
        otc_cursor = otc_connect.cursor()
        otc_cursor.execute(sql)
        name = otc_cursor.fetchall()
        address_lists = []
        for i in name:
            address_lists.append(",".join(list(i)))
        return address_lists

    # 获取用户name， id， token 并合并成一个新的列表
    def get_user_info_list(self, sql):
        token_list = []
        id_list = []
        name_list = []
        for username in self.get_name_list(sql):
            data = {
                "password": "YGB423542",
                "userAccount": username
            }
            header = {
                "Content-Type": "application/json",
                "keyId": "0f7b2e4919dd47578aa54a20621660cd"
            }
            res = requests.post(url=url.login, data=json.dumps(data),
                                headers=header).json()
            # print(res)
            name_token = res["data"]["loginSuccessModel"]["rememberPasswordToken"]
            id = res["data"]["userBasic"]["id"]
            name = res["data"]["userBasic"]["userName"]
            id_list.append(id)
            name_list.append(name)
            token_list.append(name_token)
        user_info_list = list(zip(token_list, id_list, name_list))
        return user_info_list


if __name__ == "__main__":
    name_sql = "SELECT useraccount FROM user_info WHERE useraccount != '876522068@qq.com';"
    addr_sql = "SELECT t3.addr FROM user_info t1 INNER JOIN asset t2 on t1.id = t2.user_id INNER JOIN address t3 " \
               "on t2.id = t3.asset_id WHERE t1.username != '876522068@qq.com'  AND t3.is_contact = 0;"
    run = GetData()
    t_token = run.get_user_info_list(name_sql)
    # print(run.get_user_address(addr_sql))
    print(t_token)

