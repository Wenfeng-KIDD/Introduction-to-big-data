from selenium.webdriver import Edge
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import sqlite3
import time

webdriver = Edge()
webdriver.get('http://job.mohrss.gov.cn/')
time.sleep(1)
webdriver.find_element(By.XPATH, '//*[@id="textfield"]').send_keys('电子信息', Keys.ENTER)
time.sleep(1)

data = []


def search():
    each_info = webdriver.find_elements(By.XPATH, '//*[@id="findjobTable"]/li')
    count = 0
    for row in each_info:
        work_name = row.find_element(By.XPATH, './div[1]/ul[1]/li[1]/a[1]/span').text
        data.append(work_name)
        work_salary = row.find_element(By.XPATH, './div[1]/ul[1]/li[2]/span').text
        data.append(work_salary)
        work_company = row.find_element(By.XPATH, './div[1]/ul[1]/li[1]/a[2]').text
        data.append(work_company)
        work_people = row.find_element(By.XPATH, './div[1]/ul[1]/li[3]').text
        data.append(work_people)
        work_place = row.find_element(By.XPATH, './div[1]/ul[1]/li[4]').text
        data.append(work_place)
        count = count + 1
    print(data)
    print(count)


def create_database():
    conn = sqlite3.connect('web.db')
    cursor = conn.cursor()

    sql = '''CREATE TABLE web3
        (
         WORK_NAME TEXT NOT NULL,
         WORK_SALARY TEXT NOT NULL,
         WORK_COMPANY TEXT NOT NULL,
         WORK_PEOPLE TEXT NOT NULL,
         WORK_PLACE TEXT NOT NULL 
        )'''

    cursor.execute(sql)
    conn.commit()
    conn.close()
    print('table has been created successfully!')


def increase_database(data1):
    conn = sqlite3.connect('web.db')
    cursor = conn.cursor()

    for j in range(0, 30):
        sql1 = '''INSERT INTO web3(WORK_NAME, WORK_SALARY, WORK_COMPANY, WORK_PEOPLE, WORK_PLACE)
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