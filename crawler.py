import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options

# 设置 Chrome 无头模式
chrome_options = Options()
chrome_options.add_argument("--headless")  # 启用无头模式
chrome_options.add_argument("--disable-gpu")  # 禁用 GPU 加速（可选）
chrome_options.add_argument("--no-sandbox")  # 禁用沙盒（可选）
chrome_options.add_argument("--disable-dev-shm-usage")  # 禁用 /dev/shm 使用（可选）

# Open a new Chrome browser
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://dawn.tw/119/")

# Fetch data function
def fetch_data(): 
    try:
        wait = WebDriverWait(driver, 10)
        table_wrapper = wait.until(EC.presence_of_element_located((By.ID, "dataTable_wrapper")))
        
        # 如果找到了元素，輸出成功信息
        print("成功抓到 dataTable_wrapper 元素!")
    except:
        # 如果未找到元素，輸出錯誤信息
        print("未能找到 dataTable_wrapper 元素")

    try:
        bigTable = WebDriverWait(table_wrapper, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "table"))
        )
        
        # 如果找到了元素，輸出成功信息
        print("成功抓到 table 元素!")
    except:
        # 如果未找到元素，輸出錯誤信息
        print("未能找到 table 元素")

    try:
        smallTable = WebDriverWait(table_wrapper, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "tbody"))
        )
        
        # 如果找到了元素，輸出成功信息
        print("成功抓到 tbody 元素!")
    except:
        # 如果未找到元素，輸出錯誤信息
        print("未能找到 tbody 元素")

    # 華到底部
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3) 

    # 等待30毫秒
    WebDriverWait(driver, 30).until(
        lambda driver: driver.execute_script("return document.readyState") == "complete" and
                    len(driver.find_elements(By.TAG_NAME, "tr")) > 0
    )

    click_100_button(10)

    try:
        # 獲取所有的 tr 元素
        rows = WebDriverWait(smallTable, 30).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "tr"))
        )
        # rows = smallTable.find_elements(By.TAG_NAME, "tr")

        data = []

        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            for cell in cells:
                print(cell.text)
                timeStamp = cells[0].text
                caseType = cells[1].text
                caseName = cells[2].text
                position = cells[3].text
                status = cells[4].text
                
                links = cells[5].find_elements(By.TAG_NAME, "a")
                first_link_href = links[0].get_attribute("href") if links else "没有链接"

                if first_link_href.startswith("https://www.google.com/maps/search/?api=1&query="):
                    coord_part = first_link_href[len("https://www.google.com/maps/search/?api=1&query="):]
                    # 使用逗号分隔经度和纬度
                    coords = coord_part.split(",")
                    if len(coords) == 2:
                        latitude = coords[0]
                        longitude = coords[1]
                    else:
                        latitude = "未知"
                        longitude = "未知"
                else:
                    latitude = "未知"
                    longitude = "未知"

                data.append([timeStamp, caseType, caseName, position, status, first_link_href, latitude, longitude])
                # print(cell.text)

        print(f"成功抓到 {len(rows)} 個 tr 元素!")

    except Exception as e:
        print(f"錯誤1: {e}")

    filtered_data = [item for index, item in enumerate(data) if index % 6 == 0]

    # for index, row_filtered_data in enumerate(filtered_data):
    #     print(f"第 {index+1} 行的内容: {row_filtered_data}")

    # 将数据保存到 JSON 文件
    try:
        with open('coordinate.json', 'w', encoding='utf-8') as json_file:
            json.dump(filtered_data, json_file, ensure_ascii=False, indent=4)
        print(f"数据已保存到 {'coordinate.json'}")
    except Exception as e:
        print(f"保存 JSON 文件时发生错误: {e}")

def click_100_button(dataLength):
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        select_element = driver.find_element(By.NAME, "dataTable_length")
        select_element.click()
        dropdown = Select(select_element)
        dropdown.select_by_visible_text("${dataLength}")
        print("每页显示 100 条记录")
        driver.execute_script("window.scrollTo(0, 0);")

    except Exception as e:
        print(f"错误3: {e}")

def start_function(waitingSeconds):
    try:
        wait = WebDriverWait(driver, 10)

        # 等待按钮出现
        button = wait.until(EC.presence_of_element_located((By.ID, "updateButton")))

        while True:
            driver.execute_script("window.scrollTo(0, 0);")
            # 点击按钮
            button.click()
            print("按钮已点击!")
            fetch_data()
            
            time.sleep(waitingSeconds)
    except Exception as e:
        print(f"错误2: {e}")
    

if __name__ == '__main__':
    start_function(10)

# start_function(10)
# driver.quit()
