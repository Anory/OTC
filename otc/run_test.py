from otc.trade import ThreadTest
from send import send_mailpy3
import time


class Run():
    def __init__(self, name_headers, name_sql):
        self.run = ThreadTest(name_headers, name_sql)
        self.sendmail = send_mailpy3.SendMail()

    # 长时间
    def run_trade(self):
        self.run.aic_send()
        originTime = int(round(time.time() * 1000))
        for i in range(0, 1):
            run_trade = self.run.buy_or_sell()
            if run_trade != "200":
                result = "测试异常"
                send_message = "程序执行异常，返回结果：" + run_trade + ", 执行到第" + (str(i + 1)) + "条记录。"
                self.sendmail.sendMessage(send_message, result)
                break
            if int((int(round(time.time() * 1000)) - originTime) / 1000) == 60:
                print("originTime:", originTime)
                print('程序每分钟执行：%d' % int(i + 1))
                break