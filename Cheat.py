import time
import random

import selenium.common.exceptions
from selenium.webdriver.common.by import By
from selenium import webdriver

main_options, sub_options = webdriver.ChromeOptions(), webdriver.ChromeOptions()

sub_options.add_argument('--headless')


class PdfLeaker:
    def __init__(self, url, log, pas):
        self.driver = webdriver.Chrome(options=main_options)
        self.leaker = None
        self.url = url
        self.login = log
        self.password = pas
        self.links = []
        self.answers = []
        self.time = (random.randrange(15, 22) * 60) + random.randrange(0, 60)
        self.correct = random.randrange(0, 3)

    def log(self):
        self.driver.get("https://ege.sdamgia.ru")
        time.sleep(3)
        while True:
            try:
                email_field = self.driver.find_element(By.ID, "email")
                email_field.send_keys(self.login)
                password_field = self.driver.find_element(By.ID, "current-password")
                password_field.send_keys(self.password)
                time.sleep(1)
                password_field.submit()
                time.sleep(2)
                return
            except selenium.common.exceptions.NoSuchElementException:
                print("Can`t login. ")

    def get_tasks(self):
        self.driver.get(self.url)
        time.sleep(1)

        elems = self.driver.find_elements(By.XPATH, "//a[@href]")
        for elem in elems:

            if "https://math-ege.sdamgia.ru/problem?id=" in str(elem.get_attribute("href")):
                self.links.append(str(elem.get_attribute("href")))

    def leak_answers(self):
        self.leaker = webdriver.Chrome(options=sub_options)
        for i in self.links:
            self.leaker.get(i)
            time.sleep(1)
            s = self.leaker.find_element(By.XPATH, "/html/body").text
            try:
                k = (s.index("Ответ: "))
                m = s[k + 7: k + 15].split("\n")[0].replace('.', '')
            except Exception as e:
                try:
                    k = (s.index("Ответ:"))
                    m = s[k + 6: k + 15].split("\n")[0].replace('.', '')
                except:
                    m = random.randrange(0,15)

            print(m)
            self.answers.append(m)
            time.sleep(0.1)

    def do(self):
        answer_forms = self.driver.find_elements(By.XPATH,
                                                 '//input[not(@type="hidden") and(contains(@class, "test_inp"))]')
        wrong = random.choices([i for i in range(len(self.answers))], k=self.correct)
        for form in range(len(answer_forms)):
            if form in wrong:
                answer_forms[form].send_keys(f"{random.randrange(0, 10)}")
            else:
                answer_forms[form].send_keys(f"{self.answers[form]}")
            time.sleep(1)
        time.sleep(3)

        link = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[5]/div[5]/input')
        time.sleep(self.time)
        link.click()
        time.sleep(10)

    def run(self):
        self.log()
        time.sleep(1)
        self.get_tasks()
        self.leak_answers()
        self.do()
        print(f'Test completed, time = {self.time / 60} min, with {12 - self.correct} correct answers.')


if __name__ == "__main__":
    N = 7
    for _ in range(N):
        login = ''
        password = ''
        url = ""
        solver = PdfLeaker(url, login, password)
        solver.run()
        del solver
