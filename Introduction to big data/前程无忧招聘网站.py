from selenium.webdriver import Edge
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import sqlite3
import time

webdriver = Edge()
webdriver.get('https://www.51job.com/')
time.sleep(1)
webdriver.find_element(By.XPATH, '//*[@id="kwdselectid"]').send_keys('电子信息', Keys.ENTER)
time.sleep(1)

# 用来存储数据，方便存入数据库
data = []


# 定义函数难道要与上一行代码相隔两行吗？不然的话就会警告？
def search():
    # TypeError: 'WebElement' object is not iterable //each_info中查询的元素应该要包括复数s，这样才可实现对象迭代
    each_info = webdriver.find_elements(By.XPATH, '/html/body/div[2]/div[3]/div/div[2]/div[4]/div[1]/div')

    # 计数器的作用是记录这一页一共有多少组数据
    counter = 0

    for row in each_info:
        work_name = row.find_element(By.XPATH, './a/p[1]/span[1]').text
        data.append(work_name)
        work_salary = row.find_element(By.XPATH, './a/p[2]/span[1]').text
        data.append(work_salary)
        work_info = row.find_element(By.XPATH, './a/p[2]/span[2]').text

        split_info = work_info.split('|')
        for i in range(0, 4):
            try:
                data.append(split_info[i])
            except IndexError:
                data.append('*')
            # 有一组数据只有三项，导致字段的对应关系发生了错误.目前尚且不需要在这里修改
            # 在数据库中修改也许会更好

        counter = counter + 1
    # 事实证明一个页面总共有50组
    print(counter)
    # print(data)


def create_database():
    conn = sqlite3.connect('web.db')
    cursor = conn.cursor()

    sql = '''CREATE TABLE web1
        (
         WORK_NAME TEXT NOT NULL,
         WORK_SALARY TEXT NOT NULL,
         WORK_PLACE TEXT NOT NULL,
         WORK_EXPERIENCE TEXT NOT NULL,
         WORK_EDUCATION TEXT NOT NULL,
         WORK_PEOPLE TEXT NOT NULL
        )'''

    cursor.execute(sql)
    conn.commit()
    conn.close()


def increase_database(data1):
    conn = sqlite3.connect('web.db')
    cursor = conn.cursor()

    for j in range(0, 50):
        sql1 = '''INSERT INTO web1(WORK_NAME, WORK_SALARY, WORK_PLACE, WORK_EXPERIENCE, WORK_EDUCATION,WORK_PEOPLE)
                VALUES(?, ?, ?, ?, ?, ?)
                '''

        doc = (data1[6 * j], data1[6 * j + 1], data1[6 * j + 2], data1[6 * j + 3], data1[6 * j + 4], data1[6 * j + 5])
        cursor.execute(sql1, doc)
        conn.commit()
    conn.close()

visible = []

def get_data(data2):
    for k in range(0, 50):
        visible.append(data2[6 * k + 2])
    print(visible)


# stupid function
def count(visible):
    huangpu = 0
    tianhe = 0
    panyu = 0
    baiyun = 0
    yuexiu = 0
    haizhu = 0
    huadu = 0
    zengchen = 0
    conghua = 0
    others = 0
    for i in range(0, 50):
        if '黄埔区' in visible[i]:
            huangpu += 1
        elif '天河区' in visible[i]:
            tianhe += 1
        elif '番禺区' in visible[i]:
            panyu += 1
        elif '白云区' in visible[i]:
            baiyun += 1
        elif '越秀区' in visible[i]:
            yuexiu += 1
        elif '海珠区' in visible[i]:
            haizhu += 1
        elif '花都区' in visible[i]:
            huadu += 1
        elif '增城区' in visible[i]:
            zengchen += 1
        elif '从化区' in visible[i]:
            conghua += 1
        else:
            others += 1
    print('黄埔区出现了%d' % huangpu + '次')
    print('天河区出现了%d' % tianhe + '次')
    print('番禺区出现了%d' % panyu + '次')
    print('白云区出现了%d' % baiyun + '次')
    print('越秀区出现了%d' % yuexiu + '次')
    print('海珠区出现了%d' % haizhu + '次')
    print('花都区出现了%d' % huadu + '次')
    print('增城区出现了%d' % zengchen + '次')
    print('从化区出现了%d' % conghua + '次')
    print('其他出现了%d' % others + '次')


# 搞了这么久，才发现现在这里并不需要用到句柄，只需要点击页面就好了
# webdriver.minimize_window()
# # 输出当前的窗口句柄
# handle = webdriver.current_window_handle
# print(handle)
# # 点击新的链接，然后创建新的窗口句柄
# webdriver.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div[2]/div[4]/div[2]/div/div/div/ul/li[3]/a').click()
# all_handles = webdriver.window_handles
# print(all_handles)
# # 在上一步获取全部的句柄中，返回的是一个句柄列表，现在选择列表最后一个句柄作为新窗口
# webdriver.switch_to.window(all_handles[-1])
# now_handle = webdriver.current_window_handle  # 查看现在的句柄
# print(now_handle)

search()
# try:
#     create_database()
# except AttributeError:
#     print('database has been set.')
# else:
#     print('just now I have create the database!')

# increase_database(data)
get_data(data)
count(visible)

# 下面本来是我想尝试存储多组数据的，但是因为代码运行的时候时不时得不到正确的结果，担心IP被封，所以只选取了一个页面的五十组数据
# 还有一个问题无法解决是，同一个函数，本来可以在其他页面上截取数据，但是不知道为什么到了其他页面就开始报错

# for line in range(3, 7):
# webdriver.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div[2]/div[4]/div[2]/div/div/div/ul/li[3]/a').click()
# search()
# one = webdriver.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div[2]/div[4]/div[1]/div[1]/a/p[1]/span[1]').text
# print(one)

# if __name__ == '__main__':
#     main()
