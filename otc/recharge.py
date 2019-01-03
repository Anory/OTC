import pymysql
import requests
import json
import random
import threading
import re
from otc import add_data


# 链接otc开发数据库
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
    # print(name)
    lists = []
    for i in name:
        lists.append(",".join(list(i)))
    return lists


# 获取钱包ID
# def get_wallet_id(username_list):
#     for name in username_list:
#         otc_cursor = otc_connect.cursor()
#         wallet_sql = "SELECT id FROM asset_wallet WHERE user_id in(SELECT id FROM user_info WHERE useraccount = '%s' AND coin_id = 510140379664744449);" %(name)
#         otc_cursor.execute(wallet_sql)
#         wallet_id = otc_cursor.fetchall()
#         print(type(wallet_id))
#         id_lists = []
#         for i in wallet_id:
#             id_lists.append("".join(list(i)))
#         print(id_lists)
#     return id_lists


# 生成用户交易流水号
def add_number(username_list):
    count = 0
    for name in username_list:
        count += 1
        otc_cursor = otc_connect.cursor()
        wallet_sql = "SELECT id FROM asset_wallet WHERE user_id in(SELECT id FROM user_info WHERE useraccount = '%s') AND coin_id = 510140379664744449;" %(name)
        otc_cursor.execute(wallet_sql)
        result = str(otc_cursor.fetchall())
        wallet_num = re.findall('\d+', result)
        wallet_id = wallet_num[0]
        recharge_id = random.randint(527456174950400000, 527456174950499999)
        tx_id = random.randint(2018122600010000, 2018122600099999)
        add_sql = "INSERT INTO `asset_currency_recharge`(`id`, `tx_id`, `wallet_id`, `type`, `price`, `usd_amount`, `rmb_amount`, `status`, `sign_code`, `user_bank_account`, `platform_bank_account`, `remark`, `admin_user_id`, `sync_status`, `create_time`, `update_time`) VALUES ('%s', '%s', '%s', 2, 6.60000000, 222.50000000, 666.00000000, 0, '429uE36y', NULL, '6222202 1234 1234 0001', '工商银行', NULL, 0, '2018-12-17 18:15:11.521', '2018-12-17 18:16:24.232');"
        data = (recharge_id, tx_id, wallet_id)
        otc_cursor.execute(add_sql % data)
        otc_connect.commit()
        print('成功修改', otc_cursor.rowcount, '条数据')
    print("添加流水号数量:", count)
    return count


# 用户充值
def asset_recharge(n_lists, header):
    count = 0
    for name in n_lists:
        count += 1
        otc_cursor = otc_connect.cursor()
        tx_id_sql = "SELECT tx_id FROM asset_currency_recharge WHERE wallet_id in (SELECT id FROM asset_wallet WHERE user_id in(SELECT id FROM user_info WHERE useraccount = '%s') AND coin_id = 510140379664744449);" % name
        otc_cursor.execute(tx_id_sql)
        result = str(otc_cursor.fetchall())
        tx_id_num = re.findall('\d+', result)
        tx_id = tx_id_num[0]
        print("tx_id:", tx_id)
        token = add_data.get_token(n_lists, header)
        print("用户token：", token)
        data = {
            "operationTxId": tx_id,
            "status": '1'
        }
        headers = {
            "Access-Token": token,
            "keyId": "5d12c14d64da4904931f751cd7504fe4"
        }
        res = requests.post(url="http://172.16.2.22:16010/api/trade/response/recharge", data=data, headers=headers).json()
        print("充值返回：", res)
    print("成功修改数据数量：", count)
    return count

# 虚拟币充值
# def coin_recharge(n_list):
#     for name in n_list:
#
#     res = requests.post(url="http://172.16.2.22:16010/api/trade/testAsset/addCoinRecharge", data=data).json()
#     return res


if __name__ == '__main__':
    header = {
        "Content-Type": "application/json",
        "keyId": "5d12c14d64da4904931f751cd7504fe4"
    }
    user_sql = "SELECT useraccount FROM user_info WHERE id LIKE '528%';"
    name_list = get_name_list(user_sql)
    print("用户名列表：", name_list)
    run_add_number = add_number(name_list)
    run_recharge = asset_recharge(name_list, header)



