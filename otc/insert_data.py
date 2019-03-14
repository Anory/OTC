import pymysql
import threading
import random
import time


otc_103 = pymysql.Connect(
    host='172.16.3.103',
    port=3306,
    user='topex',
    passwd='topex123456',
    db='topex',
    charset='utf8'
)


class ThreadTest(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def insert_data(self, sql):
        otc_cursor = otc_103.cursor()
        id = random.randint(1, 99999999)
        otc_cursor.execute(sql % id)
        otc_103.commit()
        print('成功修改', otc_cursor.rowcount, '条数据')
        otc_cursor.close()


if __name__ == "__main__":
    run = ThreadTest()
    sql = "INSERT INTO `user_level`(`id`, `name`, `code`, `remark`, `trade_weight`, `trade_fee_ratio`, " \
          "`market_data_show_number`, `market_data_show_delay`, `upgrade_trade_amount`, `status`," \
          " `create_time`, `update_time`) VALUES ('%s', '机器人', 'ROBOT_LEVEL', '', " \
          "9, 0.00000000, 0, 0, 0, 1, '2018-11-22 09:55:40.000', '2019-01-15 18:00:55.378');"
    t_list = []
    for i in range(0, 2000):
        t1 = threading.Thread(target=run.insert_data(sql,))
        t_list.append(t1)
        originTime = int(round(time.time() * 1000))
        if int((int(round(time.time() * 1000)) - originTime) / 1000) == 1:
            print('程序每秒钟执行：%d' % int(i + 1))
            break
    for t in t_list:
        t.start()
    for t in t_list:
        t.join()
