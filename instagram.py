# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from datetime import datetime


# %%
email = ""
password = ""
username = ""
N = 50

n = 0

url = "https://www.instagram.com/"


# %%
options = Options()
options.headless = True

browser = webdriver.Firefox(options=options)
browser.implicitly_wait(5)


# %%
browser.get(url)


# %%
button = browser.find_element_by_xpath("//button[text()='Accept']")
button.click()
sleep(1)


# %%
username_input = browser.find_element_by_css_selector("input[name='username']")
password_input = browser.find_element_by_css_selector("input[name='password']")

username_input.send_keys(email)
sleep(0.5)
password_input.send_keys(password)
sleep(0.5)

button = browser.find_element_by_xpath("//button[@type='submit']")
button.click()
sleep(0.5)


# %%
button = browser.find_element_by_xpath("//button[text()='Not Now']")
button.click()
sleep(0.5)

button = browser.find_element_by_xpath("//button[text()='Not Now']")
button.click()

sleep(0.5)


# %%
browser.get(url+username+'/')
sleep(0.5)

button = browser.find_element_by_xpath("//a[@href='/"+username+"/following/']")
button.click()
sleep(0.5)


# %%
flag = 0

while n < N:

    button = browser.find_elements_by_xpath("//button[text()='Following']")

    try:
        for i in range(len(button)):
            if i < len(button):

                tmp = button[i]

                tmp.click()

                tmp = browser.find_element_by_xpath("//button[text()='Unfollow']")
                tmp.click()

                n += 1

                sleep(0.5)
            
            else:
                break
    except:
        print("Tezava pri unfollowanju... ")
        if flag == 5:
            break


# %%
browser.close()


# %%
now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

with open("instagram_log.log", "a") as f:
    f.write(dt_string+"      Unfollovanih "+str(n)+" ljudi.-------------Začetno stanje: ")

