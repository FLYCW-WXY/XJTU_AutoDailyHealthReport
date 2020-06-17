import time
from selenium import webdriver
import datetime
import traceback

netid = ""  # 在这里填入你的netid
pwd = ""  # 在这里填入你的密码


def reportHealth(netid, pwd):
    option = webdriver.ChromeOptions()
    option.add_argument('--start-maximized')
    option.add_argument("--window-size=1920,1080")
    option.add_argument('--no-sandbox')
    option.add_argument('--disable-dev-shm-usage')
    option.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=option)
    try:
        print("开始自动登录...")
        driver.get('http://jkrb.xjtu.edu.cn/')  # 办事中心

        time.sleep(2)

        # driver.find_element_by_link_text('登录 / SIGN IN').click() #点击登录按钮

        # time.sleep(2)
        windows = driver.window_handles
        driver.switch_to.window(windows[-1])

        # 输入用户名
        driver.find_element_by_xpath('//*[@id="form1"]/input[1]').click()
        driver.find_element_by_xpath('//*[@id="form1"]/input[1]').clear()
        driver.find_element_by_xpath('//*[@id="form1"]/input[1]').send_keys(netid)

        # 输入密码
        driver.find_element_by_name('pwd').click()
        driver.find_element_by_name('pwd').clear()
        driver.find_element_by_name('pwd').send_keys(pwd)
        # 点击登陆
        driver.find_element_by_xpath('//*[@id="account_login"]').click()

        time.sleep(2)

        print("自动登录成功")
    except Exception as e:
        print("登录失败！")
        print(e)
        traceback.print_exc()
        driver.quit()
        return 1
    try:
        print("跳转至填写页面...")
        driver.get(
            'http://jkrb.xjtu.edu.cn/EIP/cooperative/openCooperative.htm?flowId=4af591a272b0df2a0172b31acbce66f1')
        time.sleep(3)
        windows = driver.window_handles
        driver.switch_to.window(windows[-1])
        print("开始自动填写...")
        driver.switch_to.frame(
            driver.find_element_by_xpath("/html/body/div[2]/div[2]/table/tbody/tr/td[2]/div[2]/div/iframe"))

        driver.find_element_by_xpath(
            '/html/body/div/div/p[4]/div/table/tbody/tr/td/div[1]/div[3]/input').click()  # 选中“绿码”

        driver.find_element_by_xpath('/html/body/div/div/table/tbody/tr[14]/td[2]/span/span/input').click()  # 点击体温栏
        driver.find_element_by_xpath('/html/body/div/div/table/tbody/tr[14]/td[2]/span/span/input').clear()
        driver.find_element_by_xpath('/html/body/div/div/table/tbody/tr[14]/td[2]/span/span/input').send_keys(
            '36.8')  # 填报体温

        driver.find_element_by_xpath(
            '/html/body/div/div/table/tbody/tr[21]/td[2]/div/table/tbody/tr/td/div[1]/div[2]/input').click()  # 6月17日新版 点击近14日内本人或家属去过中高风险地区？
        driver.find_element_by_xpath(
            '/html/body/div/div/table/tbody/tr[23]/td[2]/div/table/tbody/tr/td/div[1]/div[2]/input').click()  # 6月17日新版 点击近14日内本人或家属是否同中高风险地区地区返回人员接触过？

        driver.find_element_by_xpath('/html/body/div/div/table/tbody/tr[11]/td[2]/span/span/input').click()  # 点击时段
        driver.find_element_by_xpath('/html/body/div/div/table/tbody/tr[11]/td[2]/span/span/input').clear()
        if datetime.datetime.now().strftime('%p') == "AM":
            print("当前时段为上午")
            driver.find_element_by_xpath('/html/body/div/div/table/tbody/tr[11]/td[2]/span/span/input').send_keys(
                '上午')  # 填报时段
        else:
            print("当前时段为下午")
            driver.find_element_by_xpath('/html/body/div/div/table/tbody/tr[11]/td[2]/span/span/input').send_keys(
                '下午')  # 填报时段

        driver.switch_to.default_content()
        driver.find_element_by_id('sendBtn').click()
    except Exception as e:
        print("填写失败！可能是已经完成填报或已超过填写时间段")
        print(e)
        traceback.print_exc()
        driver.quit()
        return 1
    try:
        driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div[2]/div[2]/a[1]/span').click()
        print("提交成功！")
    except Exception as e:
        print("提交失败！可能是已经进行过填报")
        print(e)
        traceback.print_exc()
        driver.quit()
        return 1
    driver.quit()


i = 1
print("第%i次尝试" % i)
while (reportHealth(netid, pwd) == 1) and i < 20:
    i = i + 1
    print("第%i次尝试" % i)
