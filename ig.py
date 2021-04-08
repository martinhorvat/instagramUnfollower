from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from datetime import datetime

class Unfollower:
    url = "https://www.instagram.com/"

    def __init__(self, email, username, password, n=0, headless=False, N=50):
        self.email = email
        self.password = password
        self.username = username
        
        try:
            if headless:
                print("Startam headless...")

                options = Options()
                options.headless = True

                self.browser = webdriver.Firefox(options=options)
            else:
                print("Startam windowed...")
                self.browser = webdriver.Firefox()

            self.browser.implicitly_wait(5)
            self.browser.maximize_window()

            self.browser.get(self.url)

            self.n = n
            self.N = N
        except:
            msg = "TEZAVA PRI ODPIRANJU BROWSERJA"
            self.zapis(msg)

    def find_xpath(self, xpath, click=True):
        element = self.browser.find_element_by_xpath(xpath)

        if click:
            sleep(0.5)
            element.click()

        return element

    def find_css(self, css, click=True):
        element = self.browser.find_element_by_css_selector(css)

        if click:
            sleep(0.5)
            element.click()

        return element

    def __del__(self):
        self.browser.close()

    def login(self):
        try:
            self.find_xpath("//button[text()='Accept']")
            sleep(0.5)
        except:
            print("piskotki ze sprejeti")
        try:
            u_in = self.find_css("input[name='username']", click=False)
            p_in = self.find_css("input[name='password']", click=False)

            u_in.send_keys(self.email)
            sleep(0.5)
            p_in.send_keys(self.password)
            sleep(0.5)

            self.find_xpath("//button[@type='submit']")
            sleep(0.5)

            print("Login uspesen")
        except:
            print("Exception pri loginu")
            msg = "NAPAKA PRI LOGINU"
            self.zapis(msg)

            return -1

        try:
            for _ in range(2):
                self.find_xpath("//button[text()='Not Now']")
                sleep(0.5)
        except:
            print("not now se ni pokazal")

        self.browser.get(self.url+self.username+'/')
        sleep(0.5)

    def remove(self):
        flags = 0

        button = self.find_xpath("//a[@href='/"+self.username+"/following/']")
        sleep(0.5)
        button = button.find_element_by_xpath(".//*")

        self.zac = button.get_attribute('innerHTML')

        while self.n < self.N and flags <= 5:
            button = self.browser.find_elements_by_xpath("//button[text()='Following']")

            try:
                for i in button:
                    i.click()
                    sleep(0.5)

                    self.find_xpath("//button[text()='Unfollow']")
                    sleep(0.5)

                    self.n += 1

                    if self.n >= self.N:
                        break

            except:
                flags += 1
                print("Exception pri unfollowanju...retryjam")

        self.log()

        return self.n

    def log(self):
        try:
            button = self.find_xpath("//a[@href='/"+self.username+"/following/']", click=False)
            sleep(0.5)
            button = button.find_element_by_xpath(".//*")

            self.kon = button.get_attribute('innerHTML')
        except:
            print("Tezava pri belezenju followanih...")

            msg = "NAPAKA PRI LOGGANJU"
            self.zapis(msg)

            return -1

        msg = "Zac: " + self.zac + "      Kon: " + self.kon
        self.zapis(msg)

    def zapis(self, msg):
        with open("instagram_log.log", "a") as f:
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

            f.write(dt_string + "      " + msg + "\n")
