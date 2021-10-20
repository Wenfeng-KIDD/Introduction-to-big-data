from selenium.webdriver import Edge
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import sqlite3
import time

webdriver = Edge()
webdriver.get('https://sz.58.com/')
time.sleep(1)
webdriver.find_element(By.XPATH, '//*[@id="keyword"]').send_keys('电子信息', Keys.ENTER)
time.sleep(1)

data = []


def search():
    each_info = webdriver.find_elements(By.XPATH, '//*[@id="list_con"]/li')
    counter = 0
    for row in each_info:
        info = row.find_element(By.XPATH, './div[1]/div[1]/a').text
        split_info = info.split('|')
        for i in range(0, 2):
            try:
                data.append(split_info[i])
            except TypeError:
                data.append('*')
        # data.append(info)
        work_salary = row.find_element(By.XPATH, './div[1]/p').text
        data.append(work_salary)
        work_education = row.find_element(By.XPATH, './div[2]/p/span[2]').text
        data.append(work_education)
        work_experience = row.find_element(By.XPATH, './div[2]/p/span[3]').text
        data.append(work_experience)
        counter = counter + 1
    print(data)
    print(counter)


def create_database():
    conn = sqlite3.connect('web.db')
    cursor = conn.cursor()

    sql = '''CREATE TABLE web2
        (
         WORK_PLACE TEXT NOT NULL,
         WORK_NAME TEXT NOT NULL,
         WORK_SALARY TEXT NOT NULL,
         WORK_EDUCATION TEXT NOT NULL,
         WORK_EXPERIENCE TEXT NOT NULL
        )'''

    cursor.execute(sql)
    conn.commit()
    conn.close()
    print('table has been created successfully!')


def increase_database(data1):
    conn = sqlite3.connect('web.db')
    cursor = conn.cursor()

    for j in range(0, 48):
        sql1 = '''INSERT INTO web2(WORK_PLACE, WORK_NAME, WORK_SALARY, WORK_EDUCATION, WORK_EXPERIENCE)
                VALUES(?, ?, ?, ?, ?)
                '''

        doc = (data1[5 * j], data1[5 * j + 1], data1[5 * j + 2], data1[5 * j + 3], data1[5 * j + 4])
        cursor.execute(sql1, doc)
        conn.commit()
    conn.close()
    print('data has been loaded successfully!')


search()
create_database()
increase_database(data)
