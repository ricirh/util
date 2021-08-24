import time

def getInform():
    keys = ["抗疫","含羞草","奥运会"]
    from selenium import webdriver
    browser = webdriver.Chrome()
    for key in keys:
        dataes = []
        try:
            browser.get("https://www.baidu.com")
            browser.find_element_by_id('kw').send_keys(key)
            browser.find_element_by_id('su').click()
            for i in range(1,5000):
                time.sleep(1)
                blank = browser.find_element_by_xpath('//*[@id="content_left"]')
                for each in blank.find_elements_by_xpath('//div[@srcid="1599"]'):
                    keyword, contents = each.text.split('\n')[0:2]
                    data = (keyword,contents)
                    dataes.append(data)
                i += 1
                flag = True
                for page in browser.find_elements_by_xpath('//span[@class="pc"]'):
                    if(page.text == str(i)):
                        flag = False
                        page.click()
                        break
                if flag:
                    break
        except Exception as e:
            print("出错")
        save(dataes)


def save(dataes):
    import pymysql
    conn = pymysql.connect(host="localhost", user ="root", password ="root", database ="data", charset ="utf8")
    cursor = conn.cursor()

    sql = "INSERT INTO INFORM(keyword, contents) VALUES (%s, %s);"
    try:
        cursor.executemany(sql, dataes)
        conn.commit()

    except Exception as e:
        # 有异常，回滚事务
        print(e)
        conn.rollback()

    cursor.close()
    conn.close()



if __name__ == '__main__':
    data = getInform()

