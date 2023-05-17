from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import csv
import time


class instamining():
    def __init__(self, search_hashtag):
        chrome_options = Options()
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        chrome_options.add_experimental_option("detach", True)
        self.browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        self.search_hashtag = search_hashtag
        self.browser.get(f"https://www.instagram.com/explore/tags/{search_hashtag}")
        self.browser.maximize_window()
        time.sleep(3)

    def login(self):
        self.browser.find_element(By.CLASS_NAME, "_aade").click()
        time.sleep(1)
        self.browser.find_element(By.CLASS_NAME, "_ab37").click()
        self.browser.find_element(By.ID, "email").send_keys(input("이메일 또는 전화번호: "))
        self.browser.find_element(By.ID, "pass").send_keys(input("비밀번호: "))
        self.browser.find_element(By.ID, "loginbutton").click()
        time.sleep(15)

    def scrape(self):
        WebDriverWait(self.browser, 50).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "_aa9_")))
        WebDriverWait(self.browser, 50).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "_aaqe")))
        WebDriverWait(self.browser, 50).until(EC.presence_of_all_elements_located((By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/section[2]/div/div/span/a/span/span")))
        hashtags = self.browser.find_elements(By.CLASS_NAME, "_aa9_")
        date = self.browser.find_element(By.CLASS_NAME, "_aaqe")
        like = self.browser.find_element(By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/section[2]/div/div/span/a/span/span")
        result = []
        result.append(date.text)
        result.append(int(like.text))
        for hashtag in hashtags:
            result.append(hashtag.text[1:])
        time.sleep(1)
        return result
    
    def check_next(self):
        WebDriverWait(self.browser, 50).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "x1lliihq")))
        check_list = self.browser.find_elements(By.CLASS_NAME, "x1lliihq")
        result = False
        for check in check_list:
            if check.get_attribute("aria-label") == "다음":
                result = True
        return result


    def start(self):
        self.login()
        WebDriverWait(self.browser, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "_aagu")))
        self.browser.find_element(By.XPATH, "/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/article/div[1]/div/div/div[1]/div[1]/a/div").click()
        repeat = True
        results = []

        while repeat == True:
            if self.check_next() == False:
                repeat = False
            results.append(self.scrape())
            action = ActionChains(self.browser)
            action.key_down(Keys.ARROW_RIGHT).perform()

        file = open(f"{self.search_hashtag}-report.csv", "w", encoding="utf-8")
        writer = csv.writer(file)
        for result in results:
            writer.writerow(result)

instamining("문화재보존과학회").start()