import requests
import re
from bs4 import BeautifulSoup
import json

import requests
import re
from bs4 import BeautifulSoup
import json
import time
import pandas as pd

url = "https://www.sce.pccu.edu.tw/api_handler/menu.ashx"
r = requests.get(url).text
data = json.loads(r)
count = 0
c = ["課程名稱", "課程時數", "課程訂價", "課程售價", "早鳥價格", "開課時間", "課程狀態", "課程期數", "上課地點", "課程講師", "合作單位", "課程分類", "線上課程", "實體課程"]
df = pd.DataFrame(columns=c)

typelist = []
typechinese = []

for i in range(0, len(data)-10):
    typelist.append(data[i]['mainCata']['cataId'])
    typechinese.append(data[i]['mainCata']['cataName'])


# time.sleep(2)

for webcode in typelist:
        url = "https://www.sce.pccu.edu.tw/class_list.aspx?cataid=" + str(webcode)
        try:
            r = requests.get(url)
            soup = BeautifulSoup(r.text, "html5lib")
        except:
            time.sleep(100)
            continue
        # time.sleep(2)
        # find_all結果為list,可用來計算長度
        for i in range(1, len(soup.find('ul', class_='pagination').find_all('li')) + 1):
            search_url = "https://www.sce.pccu.edu.tw/class_list.aspx?cataid=" + str(webcode) + "&p=" + str(i)

            print('---------------------------------------------------------------------------')
            r = requests.get(search_url)
            soup = BeautifulSoup(r.text, "html5lib")

            # time.sleep(4)

            class_links = soup.find_all('tbody')[1].find_all('a')
            for link in class_links:
                r = requests.get("https://www.sce.pccu.edu.tw/" + link['href'])
                print("web:", link['href'])
                class_num = re.split('cataid=|&id', link['href'])[1]
                indexx = typelist.index(class_num)
                typeee = typechinese[indexx]
                r.encoding = 'utf8'
                soup = BeautifulSoup(r.text, 'html5lib')

                # 內容抓取
                try:
                    class_name = soup.find('div', id="clasName").text
                    class_loc = soup.find('div', id="location").text
                    if class_loc == " ":
                        class_loc = "線上課程"
                        online_class = 1
                        real_class = 0
                    else:
                        online_class = 0
                        real_class = 1
                    class_begin = soup.find('div', id="beginDate").text

                    class_hour = soup.find('div', class_="totaltime").text
                    if class_hour == " ":
                        class_hour = 0
                    if "hr" in class_hour:
                        class_hour = int(class_hour.replace("hr", '')) * 60

                    class_ori_price = soup.find('div', id="div_original_price").text

                    if "原價" in class_ori_price:
                        class_ori_price = class_ori_price.replace("原價 ", '').replace('元', '').replace(",", '')
                    if "原價NT" in class_ori_price:
                        class_ori_price = 0

                    class_better_price = soup.find('div', id="div_price_row").text

                    if "元" in class_better_price:
                        class_better_price = class_better_price.replace("NT$", '').replace(" 元", '').replace(",", '')
                    if "免費" in class_better_price:
                        class_better_price = 0

                    class_state = soup.find('div', class_="statusbtn_div").text.replace('\n', '').replace(' ', '')
                    if class_state == "加入購物車":
                        class_state = "尚有名額"
                    if class_state == "臨櫃報名各分館地圖資訊":
                        class_state = "臨櫃報名"

                    if soup.find('div', id='teacherTitle').find(class_="tab_list"):
                        for teacher in soup.find('div', id="teacherTitle").find(class_="tab_list").find_all('div'):
                            class_teacher = teacher.text
                    else:
                        class_teacher = soup.find('h1', class_="teacher_name").text
                    print('typeee:', typeee)
                    print('class_name:', class_name)
                    print('class_loc:', class_loc)
                    print('class_begin:', class_begin)
                    print('class_hour:', class_hour)
                    print('online_class:', online_class)
                    print('real_class:', real_class)
                    print('class_ori_price:', class_ori_price)
                    print('class_better_price:', class_better_price)
                    print('class_teacher:', class_teacher)
                    print('class_state:', class_state)

                    xxx = pd.Series(
                        [class_name, class_hour, class_ori_price, class_ori_price, class_better_price, class_begin,
                         class_state
                            , " ", class_loc, class_teacher, " ", typeee, online_class, real_class], index=c)
                    df = df.append(xxx, ignore_index=True)
                    count += 1
                    print(count)
                except:
                    continue


print(count)
df.to_csv("pccu_class.csv", encoding="utf-8", index=False)
a = 2
def johney():
    global a
    a+=1
    return a
@johney
def amy(a):
    b = a+1
    return b