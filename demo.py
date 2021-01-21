# coding = utf-8

from selenium import webdriver
import time
from threading import Thread

ACCOUNTS = {
    "15664886029": "5211314hh"
}
chrome_driver = "D:\\chromedriver_win32\\chromedriver.exe"  # Win32_76.0.3809.126

# Mate 20 X(5G)
BUY_URL = 'https://www.vmall.com/product/10086726905036.html'
# 测试P30 Pro
# BUY_URL = 'https://www.vmall.com/product/10086951150635.html'
# 登录url
LOGIN_URL = 'https://hwid1.vmall.com/CAS/portal/login.html?validated=true&themeName=red&service=https%3A%2F%2Fwww.vmall.com%2Faccount%2Facaslogin%3Furl%3Dhttps%253A%252F%252Fwww.vmall.com%252F&loginChannel=26000000&reqClientType=26&lang=zh-cn'
# 登录成功手动确认URL
LOGIN_SUCCESS_CONFIRM = 'https://www.vmall.com/'
# 开始自动刷新等待抢购按钮出现的时间点,提前3分钟
BEGIN_GO = '2021-01-22 10:08:00'


# 进到购买页面后提交订单
def submitOrder(driver, user):
    time.sleep(1)
    while BUY_URL == driver.current_url:
        print(user + ':当前页面还在商品详情！！！')
        time.sleep(3)

    while True:
        try:
            submitOrder = driver.find_element_by_link_text('提交订单')
            submitOrder.click()
            print(user + ':成功提交订单')
            break
        except:
            print(user + ':提交不了订单！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！')
            time.sleep(1)  # 到了订单提交页面提交不了订单一直等待
            pass
    while True:
        time.sleep(3000)
        print(user + ':进入睡眠3000s')
        pass


# 排队中
def onQueue(driver, user):
    time.sleep(1)
    nowUrl = driver.current_url
    while True:
        try:
            # 如果有返回活动页面并且可用则表示失败了，需要跳转回购买页面
            errorbutton = driver.find_element_by_link_text('返回活动页面')  # 出现这个一般是失败了。。
            if errorbutton.is_enabled():
                print(user + "：出现返回活动页面，可能抢购失败。。。")
                goToBuy(driver, user)

            pass
        except:
            print(user + ':排队中')
            time.sleep(0.3)  # 排队中
            pass
        if nowUrl != driver.current_url and nowUrl != BUY_URL:
            print(user + ':排队页面跳转了!!!!!!!!!!!!!!')
            break
    submitOrder(driver, user)


# 登录成功去到购买页面
def goToBuy(driver, user):
    driver.get(BUY_URL)
    print(user + '打开购买页面')
    # 转换成抢购时间戳
    timeArray = time.strptime(BEGIN_GO, "%Y-%m-%d %H:%M:%S")
    timestamp = time.mktime(timeArray)
    # 结束标志位
    over = False
    while True:
        if time.time() >= timestamp:  # 到了抢购时间
            button = driver.find_elements_by_xpath('//*[@id="pro-operation"]/a')[0]
            xpath = driver.find_elements_by_xpath('//*[@id="pro-operation"]/a/span')
            if len(xpath):
                text = xpath[0].text
            else:
                text = button.text
            if text == '已售完':
                over = True
                print(user + text)
                break
            if text == '立即申购' and button.get_attribute('class') != 'product-button02 disabled':
                # buyButton = driver.find_element_by_link_text('立即申购')
                print(user + '立即申购按钮出现了！！！')
                button.click()
                print(user + '立即申购')
                break
            else:
                qirihuyang = driver.find_element_by_xpath('//*[@id="pro-skus"]/dl[1]/div/ul/li[5]')
                qirihuyang.click()
            time.sleep(0.2)
        else:
            button = driver.find_elements_by_xpath('//*[@id="pro-operation"]/a')[0]
            xpath = driver.find_elements_by_xpath('//*[@id="pro-operation"]/a/span')
            if len(xpath):
                text = xpath[0].text
            else:
                text = button.text
            #  如果未到抢购时间，但是是提前登陆状态，则先点击提前登陆
            if text == '提前登录':
                button.click()
                qirihuyang = driver.find_element_by_xpath('//*[@id="pro-skus"]/dl[1]/div/ul/li[5]')
                qirihuyang.click()
                print(user + text)
                time.sleep(3)
            if timestamp - time.time() >= 2:
                time.sleep(1)
                print(user + '睡眠1s，未到脚本开启时间：' + BEGIN_GO + '，还有' + str(timestamp - time.time()) + '开始')
            else:
                print(user + '还有2秒开始抢购，起来嗨~')
    if over:
        print("很遗憾，抢购结束。。。")
        exit(0)
    else:
        onQueue(driver, user)


# 登录商城,登陆成功后至商城首页然后跳转至抢购页面
def loginMall(user, pwd):
    driver = webdriver.Chrome(executable_path=chrome_driver)
    driver.get(LOGIN_URL)
    try:
        time.sleep(5)  # 等待页面加载完成
        account = driver.find_element_by_xpath(
            '/html/body/div[1]/div[2]/div/div/div[1]/div[3]/span[3]/div[1]/span/div[3]/div[1]/div/div/input')
        account.send_keys(user)
        time.sleep(1)
        password = driver.find_element_by_xpath(
            '/html/body/div[1]/div[2]/div/div/div[1]/div[3]/span[3]/div[1]/span/div[4]/div/div/div/input')
        password.send_keys(pwd)
        print(user + '输入了账号密码，等待手动登录')
    except:
        print(user + '账号密码不能输入')

    while True:
        time.sleep(3)
        if LOGIN_SUCCESS_CONFIRM == driver.current_url:
            print(user + '登录成功！')
            break
    goToBuy(driver, user)


if __name__ == "__main__":
    # 账号密码
    data = ACCOUNTS
    # 构建线程
    threads = []
    for account, pwd in data.items():
        t = Thread(target=loginMall, args=(account, pwd,))
        threads.append(t)
        # 启动所有线程
    for thr in threads:
        time.sleep(2)
        thr.start()
